from SLP.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from slp_admin.models import *
from datetime import datetime
import jwt, json
from django.core.mail import EmailMultiAlternatives, EmailMessage


# Create your views here.
@api_view(['POST'])
def change_password_user(request):
    try:
        verify_token = request.headers.get('Usertoken')
    except Exception as e:
        print(e)
        return Response("Session Expired")
    print(verify_token)
    if request.method == 'POST':
        try:
            user = UserToken.objects.get(token=verify_token)
        except:
            return Response("invalid token or user not found")
        password = request.data['password']
        old_passwrd = request.data['old_pass']
        try:
            SlpUser.objects.get(password=old_passwrd)
        except:
            return Response("Password Invalid")
        if password == old_passwrd:
            return Response("Old password same as New")
        user_pass = SlpUser.objects.get(id=user.user.id)
        user_pass.password = password
        print("idddddddd", user.user.id)
        user_pass.save()
        return Response("User password changed")


@api_view(['POST', 'GET'])
def forget_password(request):
    if request.method == 'POST':
        email = request.data['email']
        try:
            user_id = SlpUser.objects.get(email=email)
            print(user_id.id)
        except:
            return Response("Email Not registered, Enter Registerd Email")
        try:
            ids = user_id.id
            subject = 'hello'
            text_content = 'http://127.0.0.1:8000/user/reset_password/user_id.id/'
            data = 'Please Click the link to Reset your Password'
            content = '<br><a href="http://127.0.0.1:8000/user/reset_password/' + str(
                ids) + '/"><button type="button"> CLICK </button></a>'
            html_content = data + content
            # msg = send_mail(subject,message, EMAIL_HOST_USER, [email], fail_silently = False)
            # send_mail(subject,message, EMAIL_HOST_USER, [email], fail_silently = False)
            msg = EmailMessage(subject, html_content, EMAIL_HOST_USER, [email])
            msg.content_subtype = "html"  # Main content is now text/html
            msg = EmailMultiAlternatives(subject, text_content, EMAIL_HOST_USER, [email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
        except Exception as e:
            print(e)
            return Response("error")
        return Response("Email is sent")


@api_view(['POST', 'GET'])
def reset_password(request, ids):
    print("idddd", ids)
    if request.method == 'GET':
        resetPass = SlpUser.objects.get(id=ids)
        return Response(" (get) ")
    if request.method == 'POST':
        newPass = request.data['newPass']
        print("new pass", newPass)
        resetPass = SlpUser.objects.get(id=ids)
        resetPass.password = newPass
        resetPass.save()
        return Response("Your Password is RESET (post)")
