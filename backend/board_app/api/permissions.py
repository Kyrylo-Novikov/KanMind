from rest_framework import permissions
from board_app.models import Board


class IsOwner(permissions.BasePermission):
    """
    Allows access only to the owner of the object.
    """

    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'owner'):
            return obj.owner == request.user
        if hasattr(obj, 'board'):
            return obj.board.owner == request.user
        return False


class IsMember(permissions.BasePermission):
    """
    Allows access only to the members of the board.
    """

    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'board'):
            return obj.board.members.filter(id=request.user.id).exists()
        if hasattr(obj, 'members'):
            return obj.members.filter(id=request.user.id).exists()
        return False


class IsMemberOrOwnerOfTheBoard(permissions.BasePermission):
    """
    Permission to controle read and write access to the boards
    """

    def has_permission(self, request, view):
        """
        Allows safe read methods for the user.
        For write methods, grants permission if the user is owner or member of the board.

        Args:
            request (Request): The incoming HTTP Request.
            view (APIView) : The view being accessed.

        Returns:
            bool: True if  permissions is granted, False otherwise .
        """
        if request.method in permissions.SAFE_METHODS:
            return True
        board_id = request.data.get('board')
        if not board_id:
            return True
        try:
            board = Board.objects.get(id=board_id)
        except (Board.DoesNotExist, ValueError, TypeError):
            return False
        return board.owner == request.user or board.members.filter(id=request.user.id).exists()


class IsAuthor(permissions.BasePermission):
    """
        Allows access only to the author of comment.
    """

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user
