from django.db import models


class CV(models.Model):
    first_name = models.CharField("First name", max_length=50)
    last_name = models.CharField("Last name", max_length=50)

    bio = models.TextField("Short bio", blank=True)
    contacts = models.TextField("Contacts (email, phone, etc.)", blank=True)
    skills = models.TextField("Skills (comma-separated)", blank=True)
    projects = models.TextField("Projects (comma-separated or free-form)", blank=True)

    created_at = models.DateTimeField("Created at", auto_now_add=True)
    updated_at = models.DateTimeField("Updated at", auto_now=True)

    class Meta:
        verbose_name = "CV"
        verbose_name_plural = "CVs"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.first_name} {self.last_name} - CV"
