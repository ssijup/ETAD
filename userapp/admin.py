from django.contrib import admin
from .models import UserDetails, UserDislikedProfiles, UserLikedProfiles,UserInterstes, MatchingProfiles

# Register your models here.
admin.site.register(UserDetails)
admin.site.register(UserInterstes)
admin.site.register(MatchingProfiles)
admin.site.register(UserLikedProfiles)
admin.site.register(UserDislikedProfiles)



 


