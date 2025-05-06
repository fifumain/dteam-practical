from django.test import TestCase
from django.urls import reverse

from .models import CV


class CVViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.cv = CV.objects.create(
            first_name="Filip",
            last_name="Test",
            bio="test bio",
            contacts="123@gmail.com",
            skills="Python, Django, REST, PostgreSQL",
            projects="test project",
        )

    def test_cv_list_view_status_code(self):
        response = self.client.get(reverse("cv-list"))
        self.assertEqual(response.status_code, 200)

    def test_cv_list_view_template_used(self):
        response = self.client.get(reverse("cv-list"))
        self.assertTemplateUsed(response, "main/cv_list.html")

    def test_cv_detail_view_status_code(self):
        response = self.client.get(reverse("cv-detail", kwargs={"pk": self.cv.pk}))
        self.assertEqual(response.status_code, 200)

    def test_cv_detail_view_404(self):
        response = self.client.get(reverse("cv-detail", kwargs={"pk": 999}))
        self.assertEqual(response.status_code, 404)

    def test_cv_detail_view_template_used(self):
        response = self.client.get(reverse("cv-detail", kwargs={"pk": self.cv.pk}))
        self.assertTemplateUsed(response, "main/cv_detail.html")
