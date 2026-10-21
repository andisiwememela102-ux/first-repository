"""Forms for creating and editing notes."""
from django import forms
from .models import Note


class NoteForm(forms.ModelForm):
    """Form used to create and edit sticky notes."""

    class Meta:
        model = Note
        fields = ["title", "content"]
        widgets = {
            "title": forms.TextInput(
                attrs={"placeholder": "Give your note a title", "maxlength": 120}
            ),
            "content": forms.Textarea(
                attrs={"placeholder": "Write your note here...", "rows": 6}
            ),
        }
        labels = {"title": "Title", "content": "Note"}
