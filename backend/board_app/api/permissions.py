from rest_framework import permissions
from board_app.models import Board


class IsOwner(permissions.BasePermission):
    """
    Object-level permission:
    Allows access only to the owner of the object.
    """

    def has_object_permission(self, request, view, obj):
        is_owner = request.user == obj.owner
        return is_owner


class IsMember(permissions.BasePermission):
    """
    Object-level permission:
    Allows access only to the members of the board.
    """

    def has_object_permission(self, request, view, obj):
        is_member = obj.members.filter(id=request.user.id).exists()
        return is_member


class IsMemberOrOwnerOfTheBoard(permissions.BasePermission):
    """
    Object-level / relation permission:
    Checks if the authenticated user is owner or member of the board 
    referenced in request.data['board']
    """

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        board_id = request.data.get('board')
        if not board_id:
            return False
        try:
            board = Board.objects.get(id=board_id)
        except Board.DoesNotExist:
            return False
        return board.owner == request.user or board.members.filter(id=request.user.id).exists()


class IsAuthor(permissions.BasePermission):
    """
        Object-level permission:
        Allows access only to the author of comment.
    """

    def has_object_permission(self, request, view, obj):
        is_author = request.user == obj.author
        return is_author
