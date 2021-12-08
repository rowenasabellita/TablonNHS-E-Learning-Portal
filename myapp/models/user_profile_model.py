from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings

import myapp
# Create your models here.

GRADE10 = 'Grade 10'
GRADE9 = 'Grade 9'
GRADE8 = 'Grade 8'
GRADE7 = 'Grade 7'

GENDER = (
    (None, 'Choose your gender'),
    ('MALE', 'Male'),
    ('FEMALE', 'Female')
)

GRADELEVEL = (
    (None, 'Grade Level'),
    (GRADE7, GRADE7),
    (GRADE8, GRADE8),
    (GRADE9, GRADE9),
    (GRADE10, GRADE10),
)

SECTION = [
    (GRADE7, (
        ('Aguinaldo', 'Aguinaldo'),
        ('Jacinto', 'Jacinto'),
        ('Luna', 'Luna'),
        ('Mabini', 'Mabini'),
        ('Rizal', 'Rizal'),
        ('Silang', 'Silang'),
    )
    ),
    (GRADE8, (
        ('Earth', 'Earth'),
        ('Mercury', 'Mercury'),
        ('Mars', 'Mars'),
        ('Jupiter', 'Jupiter'),
        ('Saturn', 'Saturn'),
    )
    ),
    (GRADE9, (
        ('Amethyst', 'Amethyst'),
        ('Emerald', 'Emerald'),
        ('Diamond', 'Diamond'),
        ('Ruby', 'Ruby'),
        ('Sapphire', 'Sapphire'),
    )
    ),
    (GRADE10, (
        ('Curie', 'Curie'),
        ('Edison', 'Edison'),
        ('Galileo', 'Galileo'),
        ('Newton', 'Newton'),
    )
    ),
]

myapp_user = User()


class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    age = models.CharField(max_length=100)
    gender = models.CharField(
        max_length=50, choices=GENDER, verbose_name="gender", blank=True)
    address = models.CharField(max_length=500, blank=True)
    gradelevel = models.CharField(
        max_length=50, choices=GRADELEVEL, verbose_name="grade level", blank=True)
    section = models.CharField(
        max_length=50, choices=SECTION, verbose_name="section", blank=True)

    def __str__(self):
        self.full_name = self.user.first_name + " " + self.user.last_name
        return self.full_name

    def get_all_sections(self):
        levels = ['Grade 7', 'Grade 8', 'Grade 9', 'Grade 10']

        sections = {}
        for l in levels:
            section_name = []
            for i in dict(SECTION)[l]:
                section_name.append(i[0])

            sections.update({
                l: section_name
            })
        return sections


@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    # instance.userprofile.save()
