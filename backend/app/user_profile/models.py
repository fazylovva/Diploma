from account.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='images/avatar/', null=True, blank=True)
    phone_number = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)

    def empty_fields(self):
        fields = [
            self.avatar,
            self.phone_number,
            self.country,
            self.user.first_name,
            self.user.email
        ]
        print(fields)
        empty_count = sum(
            field is None or (isinstance(field, str) and len(field.strip()) == 0)
            for field in fields
        )
        return empty_count

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'
        db_table = 'profile'
