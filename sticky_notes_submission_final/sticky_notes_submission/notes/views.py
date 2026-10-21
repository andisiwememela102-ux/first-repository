"""Views that handle creating, reading, updating and deleting notes."""
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from .forms import NoteForm
from .models import Note


def note_list(request):
    """Display all notes."""
    notes = Note.objects.all()
    return render(request, "notes/note_list.html", {"notes": notes})


def note_detail(request, pk):
    """Display one note."""
    note = get_object_or_404(Note, pk=pk)
    return render(request, "notes/note_detail.html", {"note": note})


def note_create(request):
    """Create a note from validated form input."""
    if request.method == "POST":
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save()
            messages.success(request, "Your note was created.")
            return redirect(note.get_absolute_url())
    else:
        form = NoteForm()
    return render(
        request,
        "notes/note_form.html",
        {"form": form, "page_heading": "Create a note"},
    )


def note_update(request, pk):
    """Update an existing note."""
    note = get_object_or_404(Note, pk=pk)
    if request.method == "POST":
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            messages.success(request, "Your note was updated.")
            return redirect(note.get_absolute_url())
    else:
        form = NoteForm(instance=note)
    return render(
        request,
        "notes/note_form.html",
        {"form": form, "page_heading": "Edit note", "note": note},
    )


def note_delete(request, pk):
    """Show a confirmation page; delete the note only when the form is posted."""
    note = get_object_or_404(Note, pk=pk)
    if request.method == "POST":
        note.delete()
        messages.success(request, "Your note was deleted.")
        return redirect("note_list")
    return render(request, "notes/note_confirm_delete.html", {"note": note})
