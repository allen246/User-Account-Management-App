from django.db import models
from django.contrib.auth.models import AbstractUser
from .utils import generate_uuid_with_prefix

# Create your models here.


class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ("student", "Student"),
        ("staff", "Staff"),
        ("admin", "Admin"),
        ("editor", "Editor"),
    )

    id = models.CharField(primary_key=True, max_length=60, unique=True, editable=False)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=60, choices=USER_TYPE_CHOICES, default="user")

    COUNTRY_CHOICES = [
        ("USA", "United States"),
        ("CAN", "Canada"),
        ("GBR", "United Kingdom"),
        ("AUS", "Australia"),
        ("GER", "Germany"),
        ("FRA", "France"),
        ("IND", "India"),
        ("JPN", "Japan"),
        ("BRA", "Brazil"),
        ("CHN", "China"),
        ("RUS", "Russia"),
        ("ZAF", "South Africa"),
        ("MEX", "Mexico"),
        ("ITA", "Italy"),
        ("ESP", "Spain"),
        ("ARG", "Argentina"),
        ("NLD", "Netherlands"),
        ("NZL", "New Zealand"),
        ("SWE", "Sweden"),
        ("CHE", "Switzerland"),
    ]

    NATIONALITY_CHOICES = [
        ("USA", "American"),
        ("CAN", "Canadian"),
        ("GBR", "British"),
        ("AUS", "Australian"),
        ("GER", "German"),
        ("FRA", "French"),
        ("IND", "Indian"),
        ("JPN", "Japanese"),
        ("BRA", "Brazilian"),
        ("CHN", "Chinese"),
        ("RUS", "Russian"),
        ("ZAF", "South African"),
        ("MEX", "Mexican"),
        ("ITA", "Italian"),
        ("ESP", "Spanish"),
        ("ARG", "Argentinian"),
        ("NLD", "Dutch"),
        ("NZL", "New Zealander"),
        ("SWE", "Swedish"),
        ("CHE", "Swiss"),
    ]

    country = models.CharField(max_length=100, choices=COUNTRY_CHOICES)
    nationality = models.CharField(max_length=100, choices=NATIONALITY_CHOICES)
    mobile = models.CharField(max_length=15)

    def save(self, *args, **kwargs):
        if not self.id:
            # Generate and set the UUID with a prefix only if the ID is not already set
            self.id = generate_uuid_with_prefix("usr")
        super().save(*args, **kwargs)
