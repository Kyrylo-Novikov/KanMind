# KanMind – Kanban Task Management System (Fullstack)

![Python](https://img.shields.io/badge/Python-3.x-blue?style=flat&logo=python)
![Django](https://img.shields.io/badge/Django-REST%20Framework-green?style=flat&logo=django)
![JavaScript](https://img.shields.io/badge/JavaScript-Vanilla-yellow?style=flat&logo=javascript)

KanMind ist eine interaktive Web-Anwendung zur Aufgabenverwaltung im Kanban-Stil. Das Projekt kombiniert ein eigenständig entwickeltes **Django-REST-Backend** mit einem vorgefertigten **Vanilla JavaScript Frontend**.

---

## 🛠️ Technologien

- **Backend:** Python, Django, Django REST Framework, SQLite/PostgreSQL
- **Frontend:** HTML5, CSS3, Vanilla JavaScript 
- **Tools & API:** REST API, Token-based Authentication

---

## ✨ Features

- **Task-Management:** Erstellen, Bearbeiten, Löschen und Verschieben von Aufgaben über verschiedene Status-Spalten (z. B. To-Do, In Progress, Review, Done).
- **Benutzerverwaltung:** Registrierung, Login und Authentifizierung von Benutzern.
- **RESTful API:** Saubere Schnittstelle zwischen Frontend und Backend für Daten-Endpoints (Tasks, User, Kontakte).

## 📁 Projektstruktur

```text
kanmind/
├── backend/            # Eigenständig entwickeltes Django-Backend (REST API)
├── project.KanMind/    # Vorgefertigtes Vanilla-JS Frontend
├── .gitignore          # Ignoriert sensible Dateien (.env, venv, etc.)
├── LICENSE.md          # Lizenzvereinbarung
└── README.md           # Projektdokumentation🚀 Installation & Lokaler Start
```

# 🚀 Installation & Lokaler Start

## 1. Repository klonen

```
git clone  [https://github.com/Kyrylo-Novikov/KanMind.git](https://github.com/Kyrylo-Novikov/kanmind.git)
cd kanmind
```

## 2. Backend einrichten & starten

### In den Backend-Ordner wechseln

cd backend

### Virtuelle Umgebung erstellen und aktivieren

python -m venv venv

### Windows:

venv\Scripts\activate

### Mac/Linux:

source venv/bin/activate

### Abhängigkeiten installieren

pip install -r requirements.txt

### Datenbank-Migrationen ausführen

python manage.py migrate

### Server starten

python manage.py runserver

# 📜 Lizenz & Rechtlicher Hinweis

## Entwickelt im Rahmen des Weiterbildungsprogramms der Developer Akademie GmbH.

- **Backend:** Eigenständige Entwicklungsleistung.
- **Frontend & Assets:** Bereitgestellt von der Developer Akademie GmbH unter der „Developer Akademie Lernlizenz (Nicht-kommerziell)“.

### Die vollständigen Lizenzbedingungen befinden sich in der Datei LICENSE.md.
