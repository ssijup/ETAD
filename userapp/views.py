from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.hashers import check_password
from django.urls import reverse
from cryptography.fernet import Fernet, InvalidToken
from urllib.parse import quote_plus
from urllib.parse import unquote_plus




from .models import UserDetails, UserPosts, MatchingProfiles, UserInterstes, UserDislikedProfiles,UserLikedProfiles
from chat.models import UserChatdetails


#Al  model code 

from django.http import JsonResponse
from django.db.models import Count
from .models import UserInterstes

GUN_SERVER_URL = "http://localhost:8765/gun"  # Replace with your Gun server URL
import requests

def guntest(request):
    return render(request, 'guntest.html')



def jaccard_similarity(list1, list2):
    intersection = len(list(set(list1).intersection(list2)))
    union = len(set(list1).union(list2))
    return float(intersection) / union if union else 0

def match_users(request, primary_user_id):
    # Get interests of the primary user
    primary_user_interests = list(UserInterstes.objects.filter(user_id=primary_user_id).values_list('interested_in', flat=True))

    # Get interests of all other users
    other_users_interests = UserInterstes.objects.exclude(user_id=primary_user_id).values('user_id').annotate(interests=Count('interested_in'))

    matches = []
    for user_interests in other_users_interests:
        interests = list(UserInterstes.objects.filter(user_id=user_interests['user_id']).values_list('interested_in', flat=True))
        similarity_score = jaccard_similarity(primary_user_interests, interests)
        matches.append({'user_id': user_interests['user_id'], 'score': similarity_score})

    return matches
    # return JsonResponse(matches, safe=False)



# def jaccard_similarity(list1, list2):
#     intersection = len(set(list1).intersection(list2))
#     union = len(set(list1).union(list2))
#     return float(intersection) / union if union else 0

# def match_users(primary_user_id, primary_user_interests):
#     # Fetch all users and their interests from Gun.js
#     response = requests.get(f"{GUN_SERVER_URL}/users")
#     if response.status_code != 200:
#         return []

#     users_data = response.json()
#     matches = []

#     for user_email, user_data in users_data.items():
#         if user_data['id'] == primary_user_id:
#             continue

#         interests = user_data.get('interests', [])
#         similarity_score = jaccard_similarity(primary_user_interests, interests)
#         matches.append({'user_id': user_data['id'], 'score': similarity_score})

#     return sorted(matches, key=lambda x: x['score'], reverse=True)


from collections import defaultdict
# @login_required
# def user_dashboard(request):
#     email = request.session.get('user_email', request.user.email)
#     primary_user_id = request.user.id

#     # Fetch the primary user details from Gun.js
#     response = requests.get(f"{GUN_SERVER_URL}/users/{email}")
#     if response.status_code != 200:
#         return render(request, 'user_dashboard.html', {'error': 'Failed to fetch user data'})

#     primary_user_data = response.json()
#     primary_user_interests = primary_user_data.get('interests', [])

#     # Get matched users
#     matched_users = match_users(primary_user_id, primary_user_interests)

#     # Get liked and disliked profiles from Gun.js
#     liked_profiles_response = requests.get(f"{GUN_SERVER_URL}/users/{email}/liked_profiles")
#     disliked_profiles_response = requests.get(f"{GUN_SERVER_URL}/users/{email}/disliked_profiles")

#     liked_profiles_ids = liked_profiles_response.json() if liked_profiles_response.status_code == 200 else []
#     disliked_profile_ids = disliked_profiles_response.json() if disliked_profiles_response.status_code == 200 else []

#     liked_count = len(liked_profiles_ids)
#     current_user_details = primary_user_data
#     matched_user_ids = [user['user_id'] for user in matched_users]

#     if current_user_details['interested_gender'] == "both":
#         user_details_in_match = [user for user in matched_users if user['gender'] in ['male', 'female']]
#     else:
#         user_details_in_match = [user for user in matched_users if user['gender'] == current_user_details['interested_gender']]

#     user_details = [user for user in user_details_in_match if user['id'] not in liked_profiles_ids and user['email'] != email and user['id'] not in disliked_profile_ids]

#     current_user_interests = current_user_interests
#     users_with_interests = defaultdict(list)
    
#     for user in user_details:
#         users_with_interests[user['id']] = user.get('interests', [])

#     user_in_match_profiles_response = requests.get(f"{GUN_SERVER_URL}/users/{email}/match_profiles")
#     user_in_match_profiles = user_in_match_profiles_response.json() if user_in_match_profiles_response.status_code == 200 else []

#     chat_users = []
#     for current_user in user_in_match_profiles:
#         if current_user['user_who_got_match']['email'] == email:
#             chat_users.append(current_user['user_who_swipe_to_match'])
#         if current_user['user_who_swipe_to_match']['email'] == email:
#             chat_users.append(current_user['user_who_got_match'])

#     user_in_matched_profiles_list = chat_users
#     matched_count = len(user_in_matched_profiles_list)

#     context = {
#         'user_details': user_details,
#         'current_user': current_user_details,
#         'current_user_interests': current_user_interests,
#         'users_with_interests': users_with_interests,
#         'liked_count': liked_count,
#         'matched_count': matched_count
#     }

#     return render(request, 'user_dashboard.html', {'context': context})

# #Redirecting to the user dashboard, showing the details that are related to the logged in user
def user_dashboard(request):
    if request.GET.get('message'):
        encoded_message = request.GET.get('message')
        message_text = unquote_plus(encoded_message)  # Decode the message
        # messages.success(request, message_text)
    email = request.user.email
    if email :
        email = request.user.email
    else :
        email = request.GET.get('user_email')
    primary_user_id = request.user.id
    matched_users = match_users(request, primary_user_id)
    print('matched_users: ' ,matched_users)
    liked_profiles_ids = UserLikedProfiles.objects.filter(user__email = email).values_list('liked_profiles_id', flat = True)
    disliked_profile_ids = UserDislikedProfiles.objects.filter(user__email = email).values_list('disliked_user_id', flat = True)
    liked_count = liked_profiles_ids.count()
    current_user_details = UserDetails.objects.get(email = email)
    #Al analysis of user matching based on the interest score
    matched_user_ids = [user['user_id'] for user in matched_users] if matched_users else []
    print('user user interseted gender :',current_user_details.interested_gender)
    if current_user_details.interested_gender == "both":
    # Filter both male and female users
        user_details_in_match = UserDetails.objects.filter(
            Q(id__in=matched_user_ids) &
            (Q(gender="male") | Q(gender="female"))
        )
    else:
        # Filter based on the interested gender in the instance
        user_details_in_match = UserDetails.objects.filter(
        id__in=matched_user_ids,
        gender=current_user_details.interested_gender
        )
    print(user_details_in_match)
    user_details = user_details_in_match.exclude(Q(id__in = liked_profiles_ids) |
                                               Q(email = email) |
                                               Q(id__in = disliked_profile_ids) |
                                               Q(is_superuser = True)
                                                )
    current_user_interests = UserInterstes.objects.filter(user__email = email)
    users_with_interests = {}
    for user in user_details:
        interest = UserInterstes.objects.filter(user = user)
        users_with_interests[user] = interest
    user_in_match_profiles = MatchingProfiles.objects.filter(Q(user_who_got_match__email =email) 
                                                                |Q(user_who_swipe_to_match__email = email)).exclude(Q(user_who_got_match_for_post = False, user_who_swipe_to_match_for_post = False) |Q(user_who_got_match_for_post = True, user_who_swipe_to_match_for_post = False) | Q(user_who_got_match_for_post = False, user_who_swipe_to_match_for_post = True))
    chat_users = []
    for current_user in user_in_match_profiles: 
        if current_user.user_who_got_match.email == email:
            chat_users.append(current_user.user_who_swipe_to_match)
        if current_user.user_who_swipe_to_match.email == email:
            chat_users.append(current_user.user_who_got_match)
    user_in_matched_profiles_list = chat_users
    matched_count = len(user_in_matched_profiles_list)
    context = {
        'user_details': user_details,
        'current_user' : current_user_details,
        'current_user_interests' : current_user_interests,
        'users_with_interests' : users_with_interests,
        'liked_count' : liked_count,
        'matched_count' : matched_count
            }
    return render(request,'user_dashboard.html',{'context' : context})




# User signups
def user_signup(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        # Create user data to store in Gun.js
        user_data = {
            "name": name,
            "email": email,
            "password": password
        }
        # Store user data in Gun.js
        response = requests.put(f"{GUN_SERVER_URL}/users/{email}", json=user_data)
        print('response', response, "--",response.content)
        if response.status_code == 200:
            request.session['signup_password'] = password
            return redirect(reverse('user_signup_details_tellus1')+'?email=' + email)
        else:
            return render(request, 'signup.html', {"error": "Error signing up user"})
    
    return render(request, 'signup.html')








#usersignups
# def user_signup(request):
#     if request.method == 'POST':
#         name = request.POST['name']
#         email = request.POST['email']
#         password = request.POST['password']
#         UserDetails.objects.create_user(name = name , email = email , password = password)
#         request.session['signup_password'] = password
#         return redirect(reverse('user_signup_details_tellus1')+'?email=' + email)
#     return render(request, 'signup.html')






# First page details getting from user
def user_signup_details_tellus1(request):
    if request.method == 'POST':
        user_email = request.GET.get('email')
        gender = request.POST.get('gender')
        interested_gender = request.POST.get('interested_gender')

        # Log the received data
        print(user_email, gender)

        # Retrieve existing user data from Gun.js
        response = requests.get(f"{GUN_SERVER_URL}/users/{user_email}")
        print(response.content, '-----','response', response)
        if response.status_code == 200 and response.json():
            user_details = response.json()

            # Update user details
            user_details['gender'] = gender
            user_details['interested_gender'] = interested_gender

            # Save updated user data to Gun.js
            update_response = requests.put(f"{GUN_SERVER_URL}/users/{user_email}", json=user_details)
            if update_response.status_code == 200:
                return redirect(reverse('user_signup_details_tellus2') + f'?user_email={user_email}')
            else:
                context = {
                    'error': 'Error updating user details in Gun.js'
                }
                return render(request, 'tellus1.html', context)
        else:
            context = {
                'error': 'User does not exist'
            }
            return render(request, 'tellus1.html', context)
    
    return render(request, 'tellus1.html')



# #first page details getting from user
# def user_signup_details_tellus1(request):
#     if request.method == 'POST':
#         user_email = request.GET.get('email')
#         gender = request.POST.get('gender')
#         print(user_email, gender)
#         interested_gender = request.POST['interested_gender']
#         try:
#             user_details = UserDetails.objects.get(email = user_email)
#             user_details.gender = gender
#             user_details.interested_gender = interested_gender
#             user_details.save()
#             return redirect(reverse('user_signup_details_tellus2')+'?user_email=' + user_email)
#         except UserDetails.DoesNotExist:
#             context= {
#                 'error' : 'user doest not exit'
#             }
#             return render(request,'tellus1.html', {'context': context})
#     return render(request, 'tellus1.html')





def user_signup_details_tellus2(request):
    if request.method == 'POST':
        print("ENTERED POST METHOD")
        user_email = request.GET.get('user_email')
        user_height = request.POST.get('user_height')
        user_education = request.POST.get('user_education')

        # Prepare user data to store in Gun.js
        user_data = {
            "height": user_height,
            "education": user_education
        }

        # Store user data in Gun.js
        response = requests.put(f"{GUN_SERVER_URL}/users/{user_email}", json=user_data)
        print('response', response)

        if response.status_code == 200:
            return redirect(reverse('user_signup_details_likes') + '?user_email=' + user_email)
        else:
            context = {'error': 'Failed to save user details to Gun.js'}
            return render(request, 'tellus2.html', {'context': context})

    return render(request, 'tellus2.html')

# def user_signup_details_tellus2(request):
#     if request.method == 'POST':
#         print("ENTERED POST METHOD")
#         user_email = request.GET.get('user_email')
#         user_height = request.POST.get('user_height')
#         user_education = request.POST.get('user_education')
#         try:
#             user_details = UserDetails.objects.get(email = user_email)
#             user_details.user_height = user_height
#             user_details.user_education = user_education
#             user_details.save()
#             return redirect(reverse('user_signup_details_likes')+'?user_email=' + user_email)
#         except UserDetails.DoesNotExist:
#             context= {
#                 'error' : 'user doest not exists'
#             }
#             return render(request,'tellus2.html', {'context': context})
#     return render(request, 'tellus2.html')



import requests

GUN_SERVER_URL = "http://localhost:8765/gun"  # Replace with your Gun server URL

def user_signup_details_likes(request):
    if request.method == 'POST':
        user_email = request.GET.get('user_email')
        selected_interests = request.POST.getlist('interested_in')
        try:
            # Store user interests in Gun.js
            user_interests_data = {"interests": selected_interests}
            response = requests.put(f"{GUN_SERVER_URL}/users/{user_email}/interests", json=user_interests_data)
            if response.status_code == 200:
                # Proceed to upload profile image
                return redirect(reverse('upload_profileimage') + '?user_email=' + user_email)
            else:
                context = {'error': 'Failed to save user interests to Gun.js'}
                return render(request, 'userlikes.html', {'context': context})
        except Exception as e:
            context = {'error': str(e)}
            return render(request, 'userlikes.html', {'context': context})
    return render(request, 'userlikes.html')

def upload_profileimage(request):
    if request.method == 'POST':
        user_email = request.GET.get('user_email')
        description = request.POST.get('description')
        image = request.FILES.get('image')

        # Prepare user profile image data to store in Gun.js
        profile_image_data = {"description": description, "image": image}

        # Store user profile image in Gun.js
        response = requests.put(f"{GUN_SERVER_URL}/users/{user_email}/profile_image", data=profile_image_data)
        if response.status_code == 200:
            return redirect(reverse('user_dashboard') + '?user_email=' + user_email)
        else:
            context = {'error': 'Failed to save user profile image to Gun.js'}
            return render(request, 'upload_image.html', {'context': context})
    return render(request, 'upload_image.html')

# #This function will be used to create the user interest
# def user_signup_details_likes(request):
#     if request.method == 'POST':
#         # user_email = request.user.email
#         user_email = request.GET.get('user_email')
#         selected_interests = request.POST.getlist('interested_in')
#         try:
#             user_details = UserDetails.objects.get(email = user_email)
#             for each in selected_interests:
#                 UserInterstes.objects.create(interested_in = each , user = user_details)

#             password = request.session['signup_password']
#             user = authenticate(email = user_email, password = password)
#             if user :
#                 request.session['user_email'] = user_email  
#                 login(request, user)

#                 return redirect(reverse('upload_profileimage')+'?user_email=' + user_email)
#         except UserDetails.DoesNotExist:
#             context= {
#                 'error' : 'user doest not exists'
#             }
#             return render(request,'userlikes.html', {'context': context})
#     return render(request, 'userlikes.html')


# def upload_profileimage(request):
#     if request.method == 'POST':
#         user_email =  request.GET.get('user_email')
#         description = request.POST.get('description')
#         image = request.FILES.get('image')
#         user_details = UserDetails.objects.get(email = user_email)
#         user_details.profile_image = image
#         user_details.description = description
#         user_details.save()
#         return redirect(reverse('user_dashboard')+'?user_email=' + user_email)
#     return render(request, 'upload_image.html')




def password_validation(upassword1):
    if len(upassword1)<5:
        error="Password must be at least 8 characters long..."
        return error
    return None





# def user_login(request):
#     if request.method == 'POST':
#         if 'user_email' in request.session:
#             return redirect('user_dashboard')
        
#         uemail = request.POST.get('user_email')
#         upassword = request.POST.get('user_password')
        
#         # Retrieve user data from Gun.js
#         response = requests.get(f"{GUN_SERVER_URL}/users/{uemail}")
#         if response.status_code == 200:
#             user_data = response.json()
#             if user_data and user_data.get('password') == upassword:
#                 # Set user session
#                 request.session['user_email'] = uemail
#                 return redirect('user_dashboard')
#             else:
#                 return render(request, 'signin.html', {'message': 'Incorrect email or password'})
#         else:
#             return render(request, 'signin.html', {'message': 'User not found'})
    
#     return render(request, 'signin.html')

# #User login 
def user_login(request):
    if request.method == 'POST' :
        if 'user_email' in request.session:
            return redirect('user_dashboard')
        if request.method == "POST":
            if request.POST.get('user_email')=='':
                user_nameerror="Enter Your email"
                return render(request,'user_login.html',{'user_nameerror':user_nameerror})
            uemail=request.POST['user_email']
            upassword=request.POST['user_password']
            try:
                user1=UserDetails.objects.filter(email=uemail).first()
                user = authenticate(email=uemail,password=upassword)
            except UserDetails.DoesNotExist:
                user=None
            if user is not None:
                if check_password(upassword , user.password):
                    request.session['user_email'] = uemail  
                    login(request, user)                        
                    return redirect('user_dashboard') #Redirecting to the user dashboard                      
                return render(request,'signin.html', {'message' : 'Incorrect Password'})
            else:
                messages.error(request,'Incorrect Password....')
    return render(request,'signin.html')



def user_logout(request):
    if 'user_email' in request.session:
        del request.session['user_email']
        logout(request)
    return redirect('user_login')



#Creating the POST of a user with the details like description , image and the others
def create_user_post(request):
    if request.method == 'POST':
        user_id = request.user.id
        try:
            user = UserDetails.objects.get(id = user_id)
        except UserDetails.DoesNotExist:
            context= {
                'error' : 'user doest not exists'
            }
            return render(request,'create_post.html', {'context': context})
        description = request.POST.get('description')
        image = request.POST.Files('image')
        post = UserPosts.objects.create(user = user, description = description, image = image)
        return render(request, 'user_dashboard.html', {'message' : 'Post created sucessfully'})
    return render(request, 'create_post.html')


#User liking(here matching the post of a user) post of a user 
def user_liking_the_post(request):
    user_who_got_like_id = request.GET['user_who_got_like_id']
    user_email = request.user.email
    try:
        user_who_swipe_to_match_details = UserDetails.objects.get(email = user_email)
        user_who_got_match_details = UserDetails.objects.get(id = user_who_got_like_id)

        matching_profile =MatchingProfiles.objects.filter( 
            Q(user_who_got_match=user_who_got_match_details, user_who_swipe_to_match=user_who_swipe_to_match_details) |
            Q(user_who_swipe_to_match=user_who_got_match_details, user_who_got_match=user_who_swipe_to_match_details)
            ).first()
        if matching_profile:
            if matching_profile.user_who_got_match_for_post:
                matching_profile.user_who_swipe_to_match_for_post = True
                matching_profile.save()
                UserLikedProfiles.objects.create(user = user_who_got_match_details,liked_profiles = user_who_swipe_to_match_details )
                return redirect('user_dashboard')
            else :
                matching_profile.user_who_got_match_for_post = True
                matching_profile.save()
                UserLikedProfiles.objects.create(user = user_who_swipe_to_match_details,liked_profiles = user_who_got_match_details)
                return redirect('user_dashboard')
    except:
        return render(request, 'user_dashboard.html' ,{'message' : 'User doest mot exixts'})
    MatchingProfiles.objects.create(user_who_got_match =user_who_got_match_details,
                                    user_who_swipe_to_match= user_who_swipe_to_match_details,
                                    user_who_swipe_to_match_for_post = True,
                                    user_who_got_match_for_post= False,
                                    )
    UserLikedProfiles.objects.create(user = user_who_swipe_to_match_details,liked_profiles = user_who_got_match_details)
    print('redirect')
    return redirect('user_dashboard')



#User then accecpting the matching request from another request
def user_accecpting_match_request(request, user_who_got_match_requested_approved_id):
    if request.method == 'POST':
        user_who_got_accepted_id = request.user.id
        try:
            user_who_got_accept_match_details = UserDetails.objects.get(id = user_who_got_accepted_id)
            user_who_got_match_requested_approved_details= UserDetails.objects.get(id = user_who_got_match_requested_approved_id)
        except UserDetails.DoesNotExist:
            return render(request, 'user_dashboard.html', {'message' : 'User does not exixts'})
        user_who_got_accepted_details = MatchingProfiles.objects.filter(user_who_got_match = user_who_got_match_requested_approved_details,
                                                                      user_who_swipe_to_match = user_who_got_accept_match_details
                                                                      ).update(
                                                                        user_who_got_match_for_post = True,
                                                                        user_who_swipe_to_match_for_post= True)
        return render(request, 'user_dashboard.html', {'message' : 'You bth are not matched and now can chat with each other'})
    
        
key = b'1xucvqDtuKscCT-iymt4piuTsVQ3tnoI-vdufsUQ2P0='
def decrypt_message(encrypted_message):
    try:
        cipher_suite = Fernet(key)
        decrypted_message = cipher_suite.decrypt(encrypted_message).decode()
        return decrypted_message
    except InvalidToken:
        print("Decryption failed: Invalid token")
        return "Decryption failed"
    

#Getting the user list where the user can chat with eachother.The user who got matched only will be listted in therir chat pages
#It will retrive the matched users of a specfic users
def user_list_for_chat(request):     
    if request.method == 'GET':
        user_email = request.user.email
        print('user_email :', user_email)
        try:
            user_details = UserDetails.objects.get(email = user_email)
            print('user_details :', user_details)
        except UserDetails.DoesNotExist:
            return render(request, 'user_dashboard.html', {'message': 'user does not exixts'})
        user_in_match_profiles = MatchingProfiles.objects.filter(Q(user_who_got_match =user_details) 
                                                                |Q(user_who_swipe_to_match = user_details)).exclude(Q(user_who_got_match_for_post = False, user_who_swipe_to_match_for_post = False) |Q(user_who_got_match_for_post = True, user_who_swipe_to_match_for_post = False) | Q(user_who_got_match_for_post = False, user_who_swipe_to_match_for_post = True))
        print('user_in_match_profiles :', user_in_match_profiles)
        chat_users = []
        for current_user in user_in_match_profiles: 
            if current_user.user_who_got_match == user_details:
                chat_users.append(current_user.user_who_swipe_to_match)
            if current_user.user_who_swipe_to_match == user_details:
                chat_users.append(current_user.user_who_got_match)
        user_in_matched_profiles_list = chat_users
        context = {
            'matched_users' : user_in_matched_profiles_list,
                 }
        return render(request, 'user_chat_page.html', {'context' : context})


'''It will retrive the previous chat message for the user
    This will be a 1-1 chat room '''
def user_chat_room(request, userinchat_id):
    if request.method == 'GET':
        if int(request.user.id) > int(userinchat_id):
            room_name = f'{request.user.id}-{userinchat_id}'        
        else:
            room_name = f'{userinchat_id}-{request.user.id}'
        thread_name = 'chat_%s' % room_name
        room_chats_messages = UserChatdetails.objects.filter(thread_name=thread_name)
        return render(request, 'user_chat_room.html', {'messages' :room_chats_messages })


def like_user_profiles(request):
    user_id = request.GET.get('user_id')
    current_user = UserDetails.objects.get(id =request.user.id)
    liked_profile = UserDetails.objects.get(id =user_id)
    UserLikedProfiles.objects.create(user = current_user,disliked_user = liked_profile)
    # message = f'You liked ${liked_profile.name} profile'
    # encoded_message = quote_plus(message)  # Encode the message
    # return redirect(reverse('user_dashboard') + '?message=' + encoded_message)
    return redirect('user_dashboard')
    # return redirect(reverse('user_dashboard')+'?message=' + message)


def user_disliking_profiles(request):
    user_id = request.GET.get('user_who_got_dislike_id')
    current_user = UserDetails.objects.get(id =request.user.id)
    disliked_profile = UserDetails.objects.get(id =user_id)
    print('user_disliking_profiles')
    UserDislikedProfiles.objects.create(user = current_user,disliked_user = disliked_profile )
    return redirect('user_dashboard')


def edit_user_interests(request):
    if request.method == "POST":
        email = request.user.email
        user = UserDetails.objects.get(email = email)
        user_interests = UserInterstes.objects.filter(user = user)
        for each in user_interests:
            user_interests.delete()
        selected_interests = request.POST.getlist('interested_in')
        for each in selected_interests:
            UserInterstes.objects.create(interested_in = each , user = user)
        return redirect('user_dashboard')
    return render(request, 'edit_user_interests.html')


def user_matching_profiles(request):
    email = request.user.email
    current_user_details = UserDetails.objects.get(email = email)
    user_in_match_profiles = MatchingProfiles.objects.filter(Q(user_who_got_match__email =email) 
                                        |Q(user_who_swipe_to_match__email = email)).exclude(
                                            Q(user_who_got_match_for_post = False,
                                            user_who_swipe_to_match_for_post = False) |
                                            Q(user_who_got_match_for_post = True, 
                                                user_who_swipe_to_match_for_post = False) |
                                                Q(user_who_got_match_for_post = False,
                                                    user_who_swipe_to_match_for_post = True))
    chat_users = []
    for current_user in user_in_match_profiles: 
        if current_user.user_who_got_match.email == email:
            chat_users.append(current_user.user_who_swipe_to_match)
        if current_user.user_who_swipe_to_match.email == email:
            chat_users.append(current_user.user_who_got_match)
    user_in_matched_profiles_list = chat_users
    current_user_interests = UserInterstes.objects.filter(user__email = email)
    matched_count = len(user_in_matched_profiles_list)
    liked_profiles_ids = UserLikedProfiles.objects.filter(user__email = email).values_list('liked_profiles_id', flat = True)
    liked_count = liked_profiles_ids.count()
    context = {
        'user_in_match_profiles' : user_in_matched_profiles_list,
        'current_user' : current_user_details, 
        'current_user_interests' : current_user_interests,
        'matched_count' : matched_count,
        'liked_count' : liked_count,
            }
    return render(request, 'match_list.html', {'context' : context})

 





