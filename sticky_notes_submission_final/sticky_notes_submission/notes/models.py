"""Database models for the notes app."""
from django.db import models
from django.urls import reverse


class Note(models.Model):
    """A sticky note with a title, content and timestamps."""

    title = models.CharField(max_length=120)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at", "-created_at"]

    def __str__(self):
        """Return the note title as its readable name."""
        return self.title

    def get_absolute_url(self):
        """Return the URL of this note's detail page."""
        return reverse("note_detail", kwargs={"pk": self.pk})
