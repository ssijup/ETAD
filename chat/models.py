from django.db import models

from userapp.models import UserDetails

# Create your models here.

#This model will hold the data of the user chatdetails (PERSONAL CHAT)
class UserChatdetails(models.Model):
    # user = models.ForeignKey(UserDetails, on_delete=models.CASCADE)
    username = models.CharField(max_length=50, null=True, blank=True)
    thread_name = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)
    message = models.BinaryField(null=True, blank=True)

    def __str__(self):
        return self.thread_name






    






