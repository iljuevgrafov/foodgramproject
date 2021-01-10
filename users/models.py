from django.db import models
# from django.contrib.auth.models import AbstractUser


# class UserRole(models.TextChoices):
#     ADMIN = 'admin'
#     USER = 'user'

# class User(AbstractUser):
#     username = models.CharField(
#         'Имя пользователя',
#         max_length=50,
#         blank=True,
#         null=True,
#         unique=True
#     )
#     email = models.EmailField('Электронная почта', unique=True)
#     bio = models.TextField('О себе', max_length=500, blank=True, null=True)
#     role = models.CharField(
#         'Группа доступа',
#         max_length=10,
#         choices=UserRole.choices,
#         default=UserRole.USER
#     )