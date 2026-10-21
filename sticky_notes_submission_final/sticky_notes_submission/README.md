# Sticky Notes Application — Part 1

A small modular Django web application for creating, viewing, editing and deleting sticky notes. The project uses Django templates, a `ModelForm`, SQLite for local development, static CSS, migrations and automated tests.

## Features

- List all saved notes and open an individual note.
- Create and edit notes with form validation.
- Confirm before deleting a note.
- Automatically record when notes are created and updated.
- Use Django's ORM and migrations to manage the database.
- Include automated tests and project design diagrams as images (PNG/SVG), PDFs and Markdown.

## Requirements

- Python 3.10 or newer
- pip

## Step-by-step setup (Windows)

1. **Extract the project ZIP** and open a terminal in the `sticky_notes_submission` folder (the folder containing `manage.py`).
2. **Create a virtual environment:**

   ```powershell
   py -m venv .venv
   ```

3. **Activate the environment:**

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

   If PowerShell blocks activation, use Command Prompt and run `.venv\Scripts\activate.bat` instead.

   > **macOS / Linux:** create the environment with `python3 -m venv .venv`, activate it with `source .venv/bin/activate`, and use `python3` wherever `py`/`python` appears below.

4. **Install dependencies:**

   ```powershell
   python -m pip install -r requirements.txt
   ```

5. **Apply database migrations:**

   ```powershell
   python manage.py migrate
   ```

   The project includes an initial migration, so you normally do not need to run `makemigrations` unless you change a model.

6. **Check the project and run its tests:**

   ```powershell
   python manage.py check
   python manage.py test
   ```

7. **Start the development server:**

   ```powershell
   python manage.py runserver
   ```

8. **Open the application** in a browser at `http://127.0.0.1:8000/`. Stop the server with `Ctrl+C` when finished.

## Main pages

| Page | URL | Purpose |
| --- | --- | --- |
| Notes list | `/` | View all notes |
| Create note | `/notes/new/` | Add a note |
| Note detail | `/notes/<id>/` | View one note |
| Edit note | `/notes/<id>/edit/` | Update a note |
| Delete note | `/notes/<id>/delete/` | Confirm and delete a note |

Replace `<id>` with the note's numeric ID.

## Project structure

```text
sticky_notes_submission/
├── manage.py
├── requirements.txt
├── README.md
├── SUBMISSION_CHECKLIST.md
├── research_answers.md
├── sticky_notes/                 # Django project settings and root URLs
├── notes/                        # Modular notes app
│   ├── models.py                 # Note database model
│   ├── forms.py                  # ModelForm and validation
│   ├── views.py                  # CRUD request handling
│   ├── urls.py                   # App URL routes
│   ├── admin.py                  # Admin registration
│   ├── tests.py                  # Automated tests
│   ├── migrations/               # Database schema history
│   ├── templates/                # base.html and notes/*.html pages
│   └── static/notes/styles.css   # Styling
└── diagrams/                     # Design diagrams
    ├── README.md                 # Diagrams displayed with explanations
    ├── *_diagram.pdf             # One PDF per diagram
    ├── sticky_notes_diagrams.pdf # All three diagrams in one PDF
    ├── images/                   # PNG and SVG exports
    └── source/                   # Editable Mermaid (.mmd) sources
```

## Design diagrams

The three diagrams (use-case, class and sequence) are provided as images, PDFs and a Markdown page:

- [Diagrams with explanations (Markdown)](diagrams/README.md)
- [All diagrams in one PDF](diagrams/sticky_notes_diagrams.pdf)
- [Use-case diagram (PNG)](diagrams/images/use_case_diagram.png)
- [Class diagram (PNG)](diagrams/images/class_diagram.png)
- [Sequence diagram (PNG)](diagrams/images/sequence_diagram.png)

SVG and per-diagram PDF versions are in the same folder. The `.mmd` files in `diagrams/source/` are only editable sources.

## Research notes

`research_answers.md` contains the requested research on how web applications preserve state across HTTP requests and how Django migrations can be used with a server-based database such as MariaDB.

## Before submitting

- Run `python manage.py check` and `python manage.py test`.
- Include the project source, migration files, README, research answers and the diagram images/PDFs.
- Do not include `.venv/`, secrets, or a local development database in the repository.
