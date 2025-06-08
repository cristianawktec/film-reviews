import django.db.models as dj_models
from django.contrib.auth.models import User
from django.utils import timezone  # necessário para default=timezone.now

class Review(dj_models.Model):
    class Status(dj_models.IntegerChoices):
        DRAFT = (5, "Draft")
        PUBLISHED = (10, "Published")

    class RatingChoices(dj_models.IntegerChoices):
        BAD = (0, "0 - Bad")
        POOR = (1, "1 - Poor")
        FAIR = (2, "2 - Fair")
        GOOD = (3, "3 - Good")
        EXCELLENT = (4, "4 - Excellent")
        EXCEPTIONAL = (5, "5 - Exceptional")

    title = dj_models.CharField(max_length=200)
    status = dj_models.IntegerField(choices=Status.choices, default=Status.DRAFT)
    image = dj_models.ImageField(upload_to='reviews/img/', blank=True, null=True)
    content = dj_models.TextField()
    body = dj_models.TextField()
    author = dj_models.ForeignKey(User, on_delete=dj_models.CASCADE)
    rating = dj_models.IntegerField(choices=RatingChoices.choices, default=RatingChoices.GOOD)

    created_at = dj_models.DateTimeField(auto_now_add=True)
    updated_at = dj_models.DateTimeField(auto_now=True)
    published_at = dj_models.DateTimeField(default=timezone.now)
