# from django.db import models
# from django.contrib.auth.models import User
# from django.dispatch import receiver
# from django.db.models.signals import post_save

# DEPARTMENT = (
#     (None), ('Department'),
#     ('Math'), ('Math'),
#     ('Science'), ('Science'),
#     ('English'), ('English'),
#     ('Filipino'), ('Filipino'),

# )
# GENDER = (
#     (None, 'Choose your gender'),
#     ('MALE', 'male'),
#     ('FEMALE', 'female')
# )


# class TeacherProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     age = models.CharField(max_length=100)
#     gender = models.CharField(
#         max_length=50, choices=GENDER, verbose_name="gender", blank=True)
#     address = models.TextField(max_length=500, blank=True)
#     department = models.CharField(
#         max_length=50, choices=DEPARTMENT, verbose_name="grade level", blank=True)

#     def __str__(self):
#         self.full_name = self.user.first_name + " " + self.user.last_name
#         return self.full_name


# # <!-- @receiver(post_save, sender=User)
# # def update_profile_signal(sender, instance, created, **kwargs):
# #     if created:
# #         TeacherProfile.objects.create(user=instance)
