import json
import requests
from django.shortcuts import render
from cryptography.fernet import Fernet, InvalidToken
from django.db.models import Q
from userapp.models import UserDetails, MatchingProfiles

key = b'1xucvqDtuKscCT-iymt4piuTsVQ3tnoI-vdufsUQ2P0='
GUN_SERVER_URL = 'http://localhost:8765/gun'  # Gun server URL

def decrypt_message(encrypted_message):
    try:
        cipher_suite = Fernet(key)
        decrypted_message = cipher_suite.decrypt(encrypted_message.encode()).decode()
        return decrypted_message
    except InvalidToken:
        print("Decryption failed: Invalid token")
        return "Decryption failed"

def fetch_messages_from_gun(thread_name):
    response = requests.get(f'{GUN_SERVER_URL}/{thread_name}')
    if response.status_code == 200:
        return response.json()
    else:
        print(f'Failed to retrieve messages: {response.text}')
        return []

def personalchat(request):
    user_email = request.user.email
    userinchat_id = request.GET['userinchat_id']
    print('userinchat_id--', userinchat_id)
    user_details = UserDetails.objects.get(email=user_email)
    user_in_chat = UserDetails.objects.get(id=userinchat_id)
    
    if int(user_details.id) > int(userinchat_id):
        room_name = f'{user_details.id}-{userinchat_id}'
    else:
        room_name = f'{userinchat_id}-{user_details.id}'
    
    thread_name = f'chat_{room_name}'
    print('thread_name :', thread_name)

    encrypted_messages = fetch_messages_from_gun(thread_name)
    decrypted_messages = []
    for message in encrypted_messages:
        print('message --=',message)
        # decrypted_message = decrypt_message(message.get('message'))
        # decrypted_messages.append((decrypted_message, message.get('username'), message.get('timestamp')))
    
    user_in_match_profiles = MatchingProfiles.objects.filter(
        Q(user_who_got_match=user_details) | Q(user_who_swipe_to_match=user_details)
    ).exclude(
        Q(user_who_got_match_for_post=False, user_who_swipe_to_match_for_post=False) |
        Q(user_who_got_match_for_post=True, user_who_swipe_to_match_for_post=False) |
        Q(user_who_got_match_for_post=False, user_who_swipe_to_match_for_post=True)
    )
    print('user_in_match_profiles :', user_in_match_profiles)

    chat_users = []
    for current_user in user_in_match_profiles:
        if current_user.user_who_got_match == user_details:
            chat_users.append(current_user.user_who_swipe_to_match)
        elif current_user.user_who_swipe_to_match == user_details:
            chat_users.append(current_user.user_who_got_match)
    
    context = {
        'user_in_chat': user_in_chat,
        'decrypted_messages': decrypted_messages,
        'matched_users': chat_users,
    }

    return render(request, "user_chat_page.html", context)










# from django.shortcuts import render
# from cryptography.fernet import Fernet, InvalidToken
# from django.db.models import Q


# from userapp.models import UserDetails, MatchingProfiles
# from .models import UserChatdetails

# key = b'1xucvqDtuKscCT-iymt4piuTsVQ3tnoI-vdufsUQ2P0='

# def decrypt_message(encrypted_message):
#     try:
#         cipher_suite = Fernet(key)
#         decrypted_message = cipher_suite.decrypt(encrypted_message).decode()
#         return decrypted_message
#     except InvalidToken:
#         print("Decryption failed: Invalid token")
#         return "Decryption failed"

# def personalchat(request):
#     # userinchat_id - it the user who is chatting with the logged in user
#     # user_email = request.session.get('user_email')
#     user_email = request.user.email
#     userinchat_id = request.GET['userinchat_id']
#     user_details = UserDetails.objects.get(email = user_email)
#     user_in_chat =   UserDetails.objects.get(id = userinchat_id) # the user who is chattinging with the logged in user
#     if userinchat_id:
#         id = userinchat_id
#     if int(user_details.id) > int(userinchat_id):
#         room_name = f'{user_details.id}-{userinchat_id}'        
#     else:
#         room_name = f'{userinchat_id}-{user_details.id}'
#     thread_name = 'chat_%s' % room_name
#     print('thread_name :',thread_name)

#     room_chats_messages = UserChatdetails.objects.filter(thread_name=thread_name)
#     decrypted_messages = []
#     for message in room_chats_messages:
#         if message.message:  # Ensure message is not None
#             decrypted_message = decrypt_message(message.message)
#             decrypted_messages.append((decrypted_message, message.username, message.timestamp))
#     print(decrypted_messages)
#     user_in_chat = UserDetails.objects.get(id=id)
#     user_in_match_profiles = MatchingProfiles.objects.filter(Q(user_who_got_match =user_details) 
#                                                                 |Q(user_who_swipe_to_match = user_details)).exclude(Q(user_who_got_match_for_post = False, user_who_swipe_to_match_for_post = False) |Q(user_who_got_match_for_post = True, user_who_swipe_to_match_for_post = False) | Q(user_who_got_match_for_post = False, user_who_swipe_to_match_for_post = True))
#     print('user_in_match_profiles :', user_in_match_profiles)
#     chat_users = []
#     for current_user in user_in_match_profiles: 
#         if current_user.user_who_got_match == user_details:
#             print('first', current_user.user_who_got_match)
#             chat_users.append(current_user.user_who_swipe_to_match)
#             print('first1', current_user.user_who_swipe_to_match)
#         if current_user.user_who_swipe_to_match == user_details:
#             print('elif second', current_user.user_who_swipe_to_match)
#             # if current_user.user_who_got_match == user_details:
#             chat_users.append(current_user.user_who_got_match)
#             print('elif second2', current_user.user_who_got_match)
#     user_in_matched_profiles_list = chat_users
#     print(user_in_matched_profiles_list)
#     context={
#         'user_in_chat': user_in_chat,
#         'decrypted_messages' : decrypted_messages, 
#         'matched_users' : user_in_matched_profiles_list,
#         }

#     return render(request, "user_chat_page.html", {'context' : context}) 


