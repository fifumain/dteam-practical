from django.urls import reverse
from main.models import CV
from rest_framework import status
from rest_framework.test import APITestCase


class CVAPITestCase(APITestCase):

    def setUp(self):
        self.cv = self.create_cv()
        self.list_url = reverse("cv-list")
        self.detail_url = reverse("cv-detail", kwargs={"pk": self.cv.pk})

    def create_cv(self):
        return CV.objects.create(
            first_name="Filip",
            last_name="TEST",
            bio="Python Developer with 3 years of experience.",
            contacts="Email: test",
            skills="Python, Django, DRF",
            projects="test",
        )

    def test_create_cv(self):
        data = {
            "first_name": "Filip",
            "last_name": "TEST",
            "bio": "Python Developer with 3 years of experience.",
            "contacts": "Email: test",
            "skills": "Python, Django, DRF",
            "projects": "test",
        }
        response = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CV.objects.count(), 2)
        self.assertEqual(CV.objects.last().first_name, "Filip")

    def test_list_cvs(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), CV.objects.count())

    def test_retrieve_cv(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["first_name"], self.cv.first_name)

    def test_update_cv(self):
        data = {
            "first_name": "Filip",
            "last_name": "Updated",
            "bio": "Updated bio.",
            "contacts": "new@example.com",
            "skills": "Python, DRF, FastAPI",
            "projects": "Updated Project",
        }
        response = self.client.put(self.detail_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.cv.refresh_from_db()
        self.assertEqual(self.cv.last_name, "Updated")
        self.assertEqual(self.cv.skills, "Python, DRF, FastAPI")

    def test_delete_cv(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(CV.objects.filter(pk=self.cv.pk).exists())
