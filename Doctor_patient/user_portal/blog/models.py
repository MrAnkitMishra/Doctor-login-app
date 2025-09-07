from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Blog(models.Model):
    CATEGORY_CHOICES = [
        ('Mental Health', 'Mental Health'),
        ('Heart Disease', 'Heart Disease'),
        ('Covid19', 'Covid19'),
        ('Immunization', 'Immunization'),
    ]

    doctor = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to="blog_images/")
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    summary = models.TextField()
    content = models.TextField()
    is_draft = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def short_summary(self):
        words = self.summary.split()
        return " ".join(words[:15]) + "..." if len(words) > 15 else self.summary

    def __str__(self):
        return self.title
