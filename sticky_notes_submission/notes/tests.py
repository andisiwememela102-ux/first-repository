"""Automated tests for the Sticky Notes application."""

from datetime import timedelta

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Note


class NoteModelTests(TestCase):
    """Tests for the Note model."""

    def test_string_representation_is_title(self):
        note = Note.objects.create(title="Shopping", content="Milk and bread")
        self.assertEqual(str(note), "Shopping")

    def test_absolute_url_points_to_detail_page(self):
        note = Note.objects.create(title="Shopping", content="Milk and bread")
        self.assertEqual(
            note.get_absolute_url(),
            reverse("note_detail", kwargs={"pk": note.pk}),
        )

    def test_notes_are_ordered_by_most_recently_updated(self):
        older = Note.objects.create(title="Older", content="First")
        newer = Note.objects.create(title="Newer", content="Second")
        Note.objects.filter(pk=older.pk).update(
            updated_at=timezone.now() - timedelta(days=1)
        )
        notes = list(Note.objects.all())
        self.assertEqual(notes[0], newer)
        self.assertEqual(notes[1], older)


class NoteViewTests(TestCase):
    """Tests for listing, reading, creating, updating and deleting notes."""

    def setUp(self):
        self.note = Note.objects.create(
            title="First note", content="Remember to practise Django."
        )

    def test_note_list_displays_existing_note(self):
        response = self.client.get(reverse("note_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "First note")

    def test_empty_note_list_loads_successfully(self):
        self.note.delete()
        response = self.client.get(reverse("note_list"))
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(response.context["notes"], [])

    def test_note_detail_displays_content(self):
        response = self.client.get(
            reverse("note_detail", kwargs={"pk": self.note.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Remember to practise Django.")

    def test_missing_note_detail_returns_404(self):
        response = self.client.get(reverse("note_detail", kwargs={"pk": 9999}))
        self.assertEqual(response.status_code, 404)

    def test_create_note(self):
        response = self.client.post(
            reverse("note_create"),
            {"title": "New note", "content": "A new reminder"},
        )
        created_note = Note.objects.get(title="New note")
        self.assertRedirects(
            response, reverse("note_detail", kwargs={"pk": created_note.pk})
        )
        self.assertEqual(created_note.content, "A new reminder")

    def test_create_note_page_loads(self):
        response = self.client.get(reverse("note_create"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Create a note")

    def test_create_note_rejects_empty_title(self):
        response = self.client.post(
            reverse("note_create"), {"title": "", "content": "Content"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Note.objects.count(), 1)
        self.assertContains(response, "This field is required.")

    def test_create_note_rejects_empty_content(self):
        response = self.client.post(
            reverse("note_create"), {"title": "A title", "content": ""}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Note.objects.count(), 1)
        self.assertContains(response, "This field is required.")

    def test_create_rejects_title_longer_than_maximum(self):
        response = self.client.post(
            reverse("note_create"),
            {"title": "x" * 121, "content": "Content"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Note.objects.count(), 1)

    def test_update_note(self):
        response = self.client.post(
            reverse("note_update", kwargs={"pk": self.note.pk}),
            {"title": "Updated title", "content": "Updated content"},
        )
        self.assertRedirects(
            response, reverse("note_detail", kwargs={"pk": self.note.pk})
        )
        self.note.refresh_from_db()
        self.assertEqual(self.note.title, "Updated title")
        self.assertEqual(self.note.content, "Updated content")

    def test_update_note_page_loads_with_existing_values(self):
        response = self.client.get(
            reverse("note_update", kwargs={"pk": self.note.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "First note")
        self.assertContains(response, "Remember to practise Django.")

    def test_update_rejects_empty_title(self):
        response = self.client.post(
            reverse("note_update", kwargs={"pk": self.note.pk}),
            {"title": "", "content": "Updated content"},
        )
        self.assertEqual(response.status_code, 200)
        self.note.refresh_from_db()
        self.assertEqual(self.note.title, "First note")
        self.assertEqual(self.note.content, "Remember to practise Django.")

    def test_edit_missing_note_returns_404(self):
        response = self.client.get(reverse("note_update", kwargs={"pk": 9999}))
        self.assertEqual(response.status_code, 404)

    def test_update_missing_note_returns_404_on_post(self):
        response = self.client.post(
            reverse("note_update", kwargs={"pk": 9999}),
            {"title": "Missing", "content": "Should not save"},
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(Note.objects.count(), 1)

    def test_delete_confirmation_does_not_delete_note(self):
        response = self.client.get(
            reverse("note_delete", kwargs={"pk": self.note.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "First note")
        self.assertTrue(Note.objects.filter(pk=self.note.pk).exists())

    def test_delete_note_on_post(self):
        response = self.client.post(
            reverse("note_delete", kwargs={"pk": self.note.pk})
        )
        self.assertRedirects(response, reverse("note_list"))
        self.assertFalse(Note.objects.filter(pk=self.note.pk).exists())

    def test_delete_missing_note_returns_404(self):
        response = self.client.post(reverse("note_delete", kwargs={"pk": 9999}))
        self.assertEqual(response.status_code, 404)
