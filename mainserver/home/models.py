from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from datetime import datetime

GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Other'),
)

# Create your models here.
class Profile(AbstractUser):
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.username


class Feedback(models.Model):
    # user =  models.ManyToManyField(Profile,related_name='feedbackuser')
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='feedbacks')

    text =  models.TextField(default="")
    like = models.BooleanField(default=False)
    comment = models.TextField(default="")
    fid = models.UUIDField(default=uuid.uuid4(),unique=True,editable=False)
    real = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_created=True,default=datetime.now())
    
    def __str__(self):
        return self.comment
