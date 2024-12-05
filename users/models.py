from django.db import models                                                                                                    #type:ignore                                                                                                     
from django.contrib.auth.models import User                                                                                     #type:ignore                                                                                         
import uuid
from django.utils import timezone                                                                           #type:ignore

class Profile(models.Model):
    USER_ROLE_TYPE = (
        ('Satyjy', 'Satyjy'),
        ('Alyjy', 'Alyjy'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    profile_image = models.ImageField(blank=True, null=True, default='profiles/user-default.png', upload_to='profiles/')
    firstname = models.CharField(max_length=50, blank=True, null=True)
    lastname = models.CharField(max_length=50, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    address = models.CharField(max_length=255, blank = True, null = True)
    phone = models.CharField(max_length=50)
    user_role = models.CharField(max_length=50, choices=USER_ROLE_TYPE, null=True, blank=True)

    start_time = models.TimeField(null=True, blank=True, default='06:00')
    finish_time = models.TimeField(null=True, blank=True, default='22:00')
    profile_visit = models.IntegerField(default=0)

    created = models.DateTimeField(auto_now_add=True)
    id= models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)

    def __str__(self):
        return str(self.phone) 
    

class ProfileVisit(models.Model):
    visitor = models.ForeignKey(User, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    visited_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.visitor.username} visited {self.profile.user.username} on {self.visited_at}'


    

