"""Automated tests for the notes app."""
from django.test import TestCase
from django.urls import reverse

from .forms import NoteForm
from .models import Note


class NoteModelTests(TestCase):
    """Tests for the Note model."""

    def test_string_representation_is_title(self):
        note = Note.objects.create(title="Shopping", content="Milk and bread")
        self.assertEqual(str(note), "Shopping")

    def test_get_absolute_url_points_to_detail_page(self):
        note = Note.objects.create(title="Link", content="Check the URL")
        self.assertEqual(
            note.get_absolute_url(), reverse("note_detail", kwargs={"pk": note.pk})
        )

    def test_timestamps_are_set_automatically(self):
        note = Note.objects.create(title="Time", content="Stamped")
        self.assertIsNotNone(note.created_at)
        self.assertIsNotNone(note.updated_at)

    def test_most_recently_updated_note_is_listed_first(self):
        older = Note.objects.create(title="Older", content="a")
        newer = Note.objects.create(title="Newer", content="b")
        # Touch the older note so it becomes the most recently updated one.
        older.content = "a, edited"
        older.save()
        self.assertEqual(list(Note.objects.all()), [older, newer])


class NoteFormTests(TestCase):
    """Tests for NoteForm validation."""

    def test_valid_data(self):
        form = NoteForm(data={"title": "Hello", "content": "World"})
        self.assertTrue(form.is_valid())

    def test_title_is_required(self):
        form = NoteForm(data={"title": "", "content": "World"})
        self.assertFalse(form.is_valid())
        self.assertIn("title", form.errors)

    def test_content_is_required(self):
        form = NoteForm(data={"title": "Hello", "content": ""})
        self.assertFalse(form.is_valid())
        self.assertIn("content", form.errors)

    def test_whitespace_only_title_is_rejected(self):
        form = NoteForm(data={"title": "   ", "content": "World"})
        self.assertFalse(form.is_valid())

    def test_title_longer_than_120_characters_is_rejected(self):
        form = NoteForm(data={"title": "x" * 121, "content": "World"})
        self.assertFalse(form.is_valid())
        self.assertIn("title", form.errors)


class NoteViewTests(TestCase):
    """Tests for the note views."""

    def setUp(self):
        self.note = Note.objects.create(
            title="First note", content="Remember to practise Django."
        )

    def test_note_list_displays_existing_note(self):
        response = self.client.get(reverse("note_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "First note")

    def test_note_list_shows_empty_state_when_no_notes(self):
        Note.objects.all().delete()
        response = self.client.get(reverse("note_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No notes yet")

    def test_note_detail_displays_content(self):
        response = self.client.get(
            reverse("note_detail", kwargs={"pk": self.note.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Remember to practise Django.")

    def test_create_page_loads(self):
        response = self.client.get(reverse("note_create"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Create a note")

    def test_create_note(self):
        response = self.client.post(
            reverse("note_create"),
            {"title": "New note", "content": "A new reminder"},
        )
        new_note = Note.objects.get(title="New note")
        self.assertRedirects(response, reverse("note_detail", kwargs={"pk": new_note.pk}))
        self.assertEqual(new_note.content, "A new reminder")

    def test_create_note_rejects_empty_title(self):
        response = self.client.post(
            reverse("note_create"), {"title": "", "content": "Content"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Note.objects.count(), 1)
        self.assertContains(response, "This field is required.")

    def test_update_page_shows_existing_values(self):
        response = self.client.get(
            reverse("note_update", kwargs={"pk": self.note.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "First note")

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

    def test_update_note_with_invalid_data_keeps_original(self):
        response = self.client.post(
            reverse("note_update", kwargs={"pk": self.note.pk}),
            {"title": "", "content": "Changed"},
        )
        self.assertEqual(response.status_code, 200)
        self.note.refresh_from_db()
        self.assertEqual(self.note.title, "First note")

    def test_delete_page_asks_for_confirmation_without_deleting(self):
        response = self.client.get(
            reverse("note_delete", kwargs={"pk": self.note.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Delete this note?")
        self.assertTrue(Note.objects.filter(pk=self.note.pk).exists())

    def test_delete_note_after_confirmation(self):
        response = self.client.post(
            reverse("note_delete", kwargs={"pk": self.note.pk})
        )
        self.assertRedirects(response, reverse("note_list"))
        self.assertFalse(Note.objects.filter(pk=self.note.pk).exists())

    def test_missing_note_returns_404_for_every_note_page(self):
        for name in ("note_detail", "note_update", "note_delete"):
            with self.subTest(view=name):
                response = self.client.get(reverse(name, kwargs={"pk": 9999}))
                self.assertEqual(response.status_code, 404)
