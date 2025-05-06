from django.test import TestCase
from django.urls import reverse

from .models import RequestLog


class RequestLogTest(TestCase):

    def test_request_logging(self):

        response = self.client.get(reverse("cv-list"))
        self.assertEqual(response.status_code, 200)

        log = RequestLog.objects.last()
        self.assertIsNotNone(log)
        self.assertEqual(log.method, "GET")
        self.assertTrue(log.timestamp)
        self.assertEqual(log.path, "/api/cv/")
