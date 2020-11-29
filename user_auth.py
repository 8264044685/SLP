from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from slp_admin.models import *
from user.serializers import *
from datetime import datetime
from slp_admin import models
import jwt, json

# Contractor
def login(request):
    return render(request, 'contractor/login-page.html')

def registration(request):
    return render(request, 'contractor/registration-page.html')
# end-Contractor

@api_view(['POST'])
def register_user(request):
    if request.method == 'POST':
        address = Address.objects.create(
            add_line1=request.data['add_line1'],
            add_line2=request.data['add_line2'],
            country=request.data['country'],
            state=request.data['state'],
            city=request.data['city'],
            zip_code=request.data['zip_code']
        )
    serializers = UserSerializer(data=request.data, context=address)
    print("byyyy" , request.data['referred_by'])
    if request.data['referred_by'] != "null":
        if serializers.is_valid():
            serializers.save()
            user = SlpUser.objects.get(refer_code=request.data['referred_by'])
            user1 = SlpUser.objects.get(email=request.data['email'])
            referred_obj = ReferredUser.objects.create(
                user_id=user1
            )
            user.referred_to.append(referred_obj)
            user.save()
            return Response({
                "status_code": 200,
                "status": "success",
                "message": "User is Registered",
                "data": serializers.data
            })
    else:
        if serializers.is_valid():
            serializers.save()
            return Response({
                "status_code": 200,
                "status": "success",
                "message": "User is Registered",
                "data": serializers.data
            })
    return Response(serializers.errors)


@api_view(['POST'])
def login_user(request):
    if request.method == 'POST':
        email = request.data['email']
        password = request.data['password']
        print(email)
        print(password)
        try:
            userAuth = SlpUser.objects.get(email=email, password=password)
            print(userAuth)
        except:
            return Response("Invalid Credentials")
        current = datetime.now()
        print(current)
        userJWT = jwt.encode({'email': email, 'password': password}, str(current))
        print(userJWT)
        token_create = UserToken.objects.create(
            user=userAuth,
            token=userJWT
        )
        token_create.save()
        request.session['Usertoken'] = str(userJWT)
        return Response({
            "status_code": 200,
            "status": "success",
            "message": "Logged In",
            "token": userJWT
        })


@api_view(['GET'])
def logout_user(request):
    if request.method == 'GET':
        verify_token = request.headers['Usertoken']
        print(verify_token)
        try:
            user_obj = UserToken.objects.get(token=verify_token)
        except:
            return Response({
                "status_code": 000,
                "status": "error",
                "message": "Invalid Token",
                "data": verify_token
            })
        user_obj.delete()
        return Response({
            "status_code": 200,
            "status": "success",
            "message": "Logged Out"
        })


@api_view(['GET', 'POST'])
def login_admin(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        try:
            adminAuth = SlpAdmin.objects.get(email=email, password=password)
            print(adminAuth)
        except:
            context = {
                'message': "Invalid Username or Password!",
                'url': 'admin_login',
                'icon': 'error',
            }
            return render(request, "admin_login.html", context)
            # return redirect('admin_login')
            # return Response("Invalid Username or Password")
        current = datetime.now()
        print(current)
        adminJWT = jwt.encode({'email': email, 'password': password}, str(current))
        print(adminJWT)
        token_create = AdminToken.objects.create(
            admin=adminAuth,
            token=adminJWT
        )
        token_create.save()
        print("str token", str(adminJWT))
        request.session['Admintoken'] = str(adminJWT)
        # return Response({
        #     "status_code": 200,
        #     "status": "success",
        #     "message": "Admin Logged In",
        #     "token": adminJWT
        # })
        return redirect("slpdashboard")
    return render(request, "admin_login.html")


@api_view(['POST'])
def logout_admin(request):
    if request.method == 'POST':
        verify_token = request.session['Admintoken']
        print("token--------", verify_token)
        try:
            admin_obj = AdminToken.objects.get(token=verify_token)
            print("obj------------", admin_obj)
        except:
            context = {
                'message': "Session Expired!",
                'url': 'admin_login',
                'icon': 'error',
            }
            return render(request, "admin_login.html", context)
        admin_obj.delete()
        context = {
            'message': "Successfully Logged Out!",
            'url': 'admin_login',
            'icon': 'success',
        }
        return render(request, "admin_login.html", context)
