from django.shortcuts import render , redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from slp_admin.models import *
from .serializer import *
import json
from django.http import HttpResponse, JsonResponse

@api_view(['GET'])
def list_user(request):
    try:
        print(request.session['Admintoken'])
        admin_session = request.session['Admintoken']
    except:
        context = {
                    'message': "Session Expired!",
                    'url': '/slp_admin/login/',
                    'icon': 'error',
                }
        return render(request , "admin_login.html" , context)
    if request.method == "GET":
        admin_info = AdminToken.objects.get(token = admin_session)
        print("admin_info" , admin_info)
        admin_name = SlpAdmin.objects.get(id = admin_info.admin.id)

        try:
            user_list = SlpUser.objects.all()
        except:
            return Response("Usermodel empty")
        context = {"name" : admin_name.first_name , "user_info" : user_list}
        return render(request , "admin_showUser.html" , context)

def block_user(request , id):
    user = SlpUser.objects.get(id = id)
    if user.status == "Unblock":
        user.status = "Block"
    else:
        user.status = "Unblock"
    user.save()
    return redirect("/slp_admin/view_user/" + id + "/")



@api_view(['GET' , 'POST'])
def view_user(request , id):
    try:
        print(request.session['Admintoken'])
        admin_session = request.session['Admintoken']
    except:
        return render(request , "admin_login.html" , {"context": "Session Expired!"})
    
    if request.method == 'GET':
        print("---id---" , id)
        admin = AdminToken.objects.get(token  = admin_session)
        admin_info = SlpAdmin.objects.get(id = admin.admin.id)
        print("admin_info",admin_info.first_name)
        try:
            user_info = SlpUser.objects.get(id = id)
        except:
            return Response("No user Found")
        try:
            reward_info = PointsTransaction.objects.filter(user = user_info)
        except:
            return Response("No records in Point Transaction")
        
        print(reward_info)
        context = {"user_info" : user_info , "reward_info" : reward_info , "name" : admin_info.first_name}
        return render(request , "admin_user-profile.html" , context)
    
    if request.method == 'POST':
        radioBtn = request.POST['exampleRadios']
        points = request.POST['points']
        reason = request.POST['reason']
        print(radioBtn)
        if radioBtn == "option1":
            user_info = SlpUser.objects.get(id = id)
            user_info.total_points = int(user_info.total_points) + int(points)
            user_info.available_points = int(user_info.available_points) + int(points)
            user_info.save()

            transac = PointsTransaction.objects.create(
                user = user_info,
                point = points,
                type = "Dispute Points",
                transaction_type = 'credit',
                splitted = False,
                reason = reason
            )
            transac.save()
        else:
            user_info = SlpUser.objects.get(id = id)
            user_info.available_points = int(user_info.available_points) - int(points)
            user_info.save()

            transac = PointsTransaction.objects.create(
                user = user_info,
                point = points,
                type = "Dispute Points",
                transaction_type = 'debit',
                splitted = False,
                reason = reason
            )
            transac.save() 
        try:
            reward_info = PointsTransaction.objects.filter(user = user_info)
        except:
            return Response("No records in Point Transaction")
        print(reward_info)
        context = {"user_info" : user_info , "reward_info" : reward_info}
        return render(request , "admin_user-profile.html" , context)
    


@api_view(['GET'])
def user_profile(request):
    try:
        # print(request.session['Admin_token'])
        admin_session = request.headers.get('Admintoken')
    except:
        return Response("Session Expired")
    if request.method == 'GET':
        snippets = SlpUser.objects.filter(email = "pareetaparekh@gmail.com")
        serializer = ProfileSerializer(snippets, many=True)
        print(serializer.data)
        return Response(serializer.data)





