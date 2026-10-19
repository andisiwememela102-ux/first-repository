from django.test import TestCase
from django.urls import reverse

from .models import Note


class NoteModelTests(TestCase):
    def test_string_representation_is_title(self):
        note = Note.objects.create(title="Shopping", content="Milk and bread")
        self.assertEqual(str(note), "Shopping")


class NoteViewTests(TestCase):
    def setUp(self):
        self.note = Note.objects.create(
            title="First note", content="Remember to practise Django."
        )

    def test_note_list_displays_existing_note(self):
        response = self.client.get(reverse("note_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "First note")

    def test_note_detail_displays_content(self):
        response = self.client.get(
            reverse("note_detail", kwargs={"pk": self.note.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Remember to practise Django.")

    def test_create_note(self):
        response = self.client.post(
            reverse("note_create"),
            {"title": "New note", "content": "A new reminder"},
        )
        self.assertRedirects(response, reverse("note_detail", kwargs={"pk": 2}))
        self.assertTrue(Note.objects.filter(title="New note").exists())

    def test_create_note_rejects_empty_title(self):
        response = self.client.post(
            reverse("note_create"), {"title": "", "content": "Content"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Note.objects.count(), 1)
        self.assertContains(response, "This field is required.")

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

    def test_delete_note_requires_post_to_delete(self):
        response = self.client.get(
            reverse("note_delete", kwargs={"pk": self.note.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Note.objects.filter(pk=self.note.pk).exists())

        response = self.client.post(
            reverse("note_delete", kwargs={"pk": self.note.pk})
        )
        self.assertRedirects(response, reverse("note_list"))
        self.assertFalse(Note.objects.filter(pk=self.note.pk).exists())

    def test_missing_note_returns_404(self):
        response = self.client.get(reverse("note_detail", kwargs={"pk": 9999}))
        self.assertEqual(response.status_code, 404)
