# Sticky Notes Application — Part 1

A small modular Django web application for creating, viewing, editing and deleting sticky notes. The project uses Django templates, a `ModelForm`, SQLite for local development, static CSS, migrations and automated test

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
│   ├── tests.py                  # Automated tests
│   ├── migrations/               # Database schema history
│   ├── templates/notes/          # HTML pages
│   └── static/notes/styles.css   # Styling
└── diagrams/                     # Editable sources and exported diagrams
    ├── *.mmd
    ├── *_diagram.pdf
    ├── README.md
    └── images/                   # PNG and SVG exports
```

## Design diagrams

The diagrams are available in formats suitable for viewing and submission. Start with the combined PDF or the diagram images:

- [Combined design diagrams (PDF)](diagrams/sticky_notes_diagrams.pdf)
- [Use-case diagram (PNG)](diagrams/images/use_case_diagram.png)
- [Class diagram (PNG)](diagrams/images/class_diagram.png)
- [Sequence diagram (PNG)](diagrams/images/sequence_diagram.png)
- [Diagram documentation and all formats](diagrams/README.md) 
