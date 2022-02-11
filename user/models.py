from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.
GRADE = [
    ('10','10'),
    ('11','11')
]
class AskerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=20, null=True, blank=True)
    last_name = models.CharField(max_length=20, null=True, blank=True)
    photo = models.ImageField(null=True, blank=True)
    school = models.CharField(max_length=20, null=True, blank=True)
    grade = models.CharField(choices=GRADE, max_length=20, null=True, blank=True)
    city = models.CharField(max_length=20, null=True, blank=True)

    def get_absolute_url(self):
        return reverse('asker', kwargs={'pk': self.user.pk})

class FriendShip(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followings')
    date = models.DateTimeField(auto_now_add=True)