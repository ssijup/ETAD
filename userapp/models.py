from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager




class UserManager(BaseUserManager):
    use_in_migration = True

    def create_user(self, email=None,password=None, phone=None, **extra_fields):
        if email is not None:
            email = self.normalize_email(email)

        if email is not None:
            if UserDetails.objects.filter(email=email).exists():
                raise ValueError('Email must be unique.')
        user = self.model(email=email, phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff = True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser = True')
        return self.create_user(email, password, **extra_fields)

    

#This model will hold the data to the user 
class UserDetails(AbstractUser):
    username = None
    name = models.CharField(max_length=250)
    email = models.CharField(max_length=250, unique=True)
    phone = models.CharField(max_length=250 , null = True , blank = True, default ='1234567899')
    password = models.CharField(max_length=250, null = True , blank = True)
    # user_interests = models.ForeignKey(UserInterstes, on_delete= models.CASCADE)
    # user_post = models.ForeignKey( on_delete=models.CASCADE)
    profile_image = models.ImageField( upload_to='images',null=True, blank = True)
    gender = models.CharField(max_length= 100, null = True , blank = True)
    interested_gender = models.CharField(max_length= 100, null = True , blank = True)
    user_height = models.CharField(max_length= 100, null = True , blank = True)
    user_education = models.CharField(max_length= 100, null = True , blank = True)
    description = models.TextField( null = True , blank = True)
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']


    def __str__(self):
        return self.name + " " + str(self.id)+ " " + str(self.interested_gender)




    
#This model will store the data  of the users interests like drinking , smoking ,playing games
class UserInterstes(models.Model):
    user = models.ForeignKey(UserDetails, on_delete=models.CASCADE)
    interested_in = models.CharField(max_length=500)
    
    def __str__(self):
        return self.user.name

class UserDislikedProfiles(models.Model):
    user = models.ForeignKey(UserDetails, on_delete=models.CASCADE)
    disliked_user = models.ForeignKey(UserDetails, on_delete=models.CASCADE,  related_name='disliked_profiles')

    def __str__(self):
        return self.user.name


    
#This model will hold the data of the post details of each user
class UserPosts(models.Model):
    user = models.ForeignKey(UserDetails, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')
    description = models.TextField()
    posted_time = models.DateTimeField(auto_now_add=True, null = True, blank = True)

#Match of a user is confirming here with the help of the two booleans (first a user will request for the match and another one have to accept the match request)
class MatchingProfiles(models.Model):
    user_who_got_match = models.ForeignKey(UserDetails, on_delete=models.CASCADE, related_name='user_who_got_match') #the user who got the request to match 
    user_who_swipe_to_match = models.ForeignKey(UserDetails, on_delete=models.CASCADE) #This is the user who like(swipe to match) the post of the user
    user_who_got_match_for_post = models.BooleanField(default = False) 
    user_who_swipe_to_match_for_post = models.BooleanField(default = False) 
    # post = models.ForeignKey(UserPosts, on_delete=models.CASCADE)

    def __str__(self):
        return ' user_who_swipe_to_match: '+self.user_who_swipe_to_match.name + ', '+ self.user_who_got_match.name



# #Like
# class Likes(models.Model):
#     liked_user = models.ForeignKey(UserDetails, on_delete=models.CASCADE) #This is the user who like the post of the user
#     like = models.BooleanField(default = False) 
#     post = models.ForeignKey(UserPosts, on_delete=models.CASCADE)
    
#This model will hold the data of a user who like their profile of a particular user
class UserLikedProfiles(models.Model):
    user = models.ForeignKey(UserDetails, on_delete=models.CASCADE)
    liked_profiles = models.ForeignKey(UserDetails, on_delete= models.CASCADE, related_name='liked_profiles')
    both_matched = models.BooleanField(default = False)

    def __str__(self):
        return self.user.name

#   
