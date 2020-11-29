from django.shortcuts import render, HttpResponse, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_protect
from passlib.hash import pbkdf2_sha256

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from django.contrib.auth.hashers import make_password, check_password

from contractor import serializers
from slp_admin.models import *
import jwt, json
from random import sample

from django.core.mail import send_mail
from SLP.settings import EMAIL_HOST_USER

import string
# import random
import urllib.parse


# Create your views here.
@csrf_protect
def checkLoginVal(request):
    contractor_email = request.POST['user_email']
    contractor_password = request.POST['password']
    try:
        contra = Contractor.objects.get(email=contractor_email)

        if (check_password(contractor_password, contra.password)):
            sequence = [i for i in range(100)]
            smple = sample(sequence, 5)
            custom_token = ''.join(map(str, smple))
            jwtToken = jwt.encode({'email': contra.email, 'jti': custom_token}, 'jwt', )
            token = jwtToken.decode("utf-8")
            request.session['contractortoken'] = token
            # print('jwt', token,"type", type(token))
            data = {"status": "success", "message": "Thank you", "data": "Login successfully...",
                    "url": "/contractor/dashboard/", 'jwtToken': token}
            return HttpResponse(json.dumps(data), content_type='application/json')
        else:
            data = {"status": "warning", "message": "Try again...", "data": "Password invalid..."}
            return HttpResponse(json.dumps(data), content_type='application/json')
    except ObjectDoesNotExist:
        data = {"status": "warning", "message": "Try again...", "data": "Email not found..."}
        return HttpResponse(json.dumps(data), content_type='application/json')
    # return render(request, 'contractor/dashboard.html')


# Signout
def signout(request):
    try:
        token = request.session['contractortoken']
        jwtToken = jwt.decode(token, 'jwt')
        try:
            contra = Contractor.objects.get(email=jwtToken['email'])
            del request.session['contractortoken']
            data = {"status": "success", "message": "Bye...", "data": "You are loggedout...",
                    "url": "/contractor/signin/"}
            return redirect('/contractor/signin/')
            # return HttpResponse(json.dumps(data), content_type='application/json')
        except ObjectDoesNotExist:
            data = {"status": "warning", "message": "Try again...",
                    "data": "You are not loggedout with other acount..."}
            return HttpResponse(json.dumps(data), content_type='application/json')
    except KeyError:
        return redirect('/contractor/signin/')


# Dashboard
def dashboard(request):
    try:
        token = request.session['contractortoken']
        jwtToken = jwt.decode(token, 'jwt')
        contra = Contractor.objects.get(email=jwtToken['email'])
        try:
            userModel = SlpUser.objects.filter(company=contra.company_name).count()
        except ObjectDoesNotExist:
            userModel = 0
        try:
            merchant = Merchant.objects.filter(company=contra.company_name).count()
        except ObjectDoesNotExist:
            merchant = 0
        try:
            prodModel = Product.objects.filter(merchant=merchant).count()
        except ObjectDoesNotExist:
            prodModel = 0
        jobCategories = Job.objects.filter(contractor=contra.id).count()
        taskModel = Task.objects.filter(contractor=contra.id).count()

        return render(request, 'contractor/dashboard.html',
                      {'users': userModel, 'products': prodModel, 'jobCategories': jobCategories, 'tasks': taskModel})
    except KeyError:
        return redirect('/contractor/signin/')


# Users
def users(request):
    try:
        token = request.session['contractortoken']
        jwtToken = jwt.decode(token, 'jwt')
        try:
            contra = Contractor.objects.get(email=jwtToken['email'])
            users = SlpUser.objects.filter(company=contra.company_name)
            return render(request, 'contractor/users.html', {'users': users})
        except ObjectDoesNotExist:
            return redirect('/contractor/signin/')
    except KeyError:
        return redirect('/contractor/signin/')


# Products
def products(request):
    try:
        token = request.session['contractortoken']
        jwtToken = jwt.decode(token, 'jwt')
        try:
            contra = Contractor.objects.get(email=jwtToken['email'])
            merchants = Merchant.objects.filter(company=contra.company_name)
            prodRewardPoints = []
            for merchantId in merchants:
                products = Product.objects.filter(merchant=merchantId.id)

            return render(request, 'contractor/products.html', {'merchants': merchants, 'products': products})
        except ObjectDoesNotExist:
            return redirect('/contractor/signin/')
    except KeyError:
        return redirect('/contractor/signin/')


# Contractor Profile
def profile(request):
    if request.method == 'GET':
        try:
            token = request.session['contractortoken']
            jwtToken = jwt.decode(token, 'jwt')
            try:
                contra = Contractor.objects.get(email=jwtToken['email'])
                return render(request, 'contractor/contractor-profile.html', {'contra': contra})
            except Exception as e:
                return HttpResponse(e)
        except KeyError:
            return redirect('/contractor/signin')

    if request.method == 'POST':
        try:
            token = request.session['contractortoken']
            jwtToken = jwt.decode(token, 'jwt')
            try:
                # print("\nPrfile photo:",request.FILES.get('contractor_image') )
                contractor_image = request.FILES.get('contractor_image')
                contra_name = request.POST['name']
                contra_contact = request.POST['contact']
                contra_add_line1 = request.POST['add_line1']
                contra_add_line2 = request.POST['add_line2']
                contra_city = request.POST['city']
                contra_state = request.POST['state']
                contra_country = request.POST['country']
                contra_zipcode = request.POST['zipcode']

                contra = Contractor.objects.get(email=jwtToken['email'])

                try:
                    contractor_add = Address.objects.get(contractor=contra.id)
                    # Insert Contractor Address

                    contractor_add.add_line1 = contra_add_line1
                    contractor_add.add_line2 = contra_add_line2
                    contractor_add.city = contra_city
                    contractor_add.state = contra_state
                    contractor_add.country = contra_country
                    contractor_add.zip_code = contra_zipcode
                    contractor_add.save()
                except ObjectDoesNotExist:
                    contractor_add = Address.objects.create(
                        contractor=contra.id,
                        add_line1=contra_add_line1,
                        add_line2=contra_add_line2,
                        city=contra_city,
                        state=contra_city,
                        country=contra_country,
                        zip_code=contra_zipcode
                    )
                    contractor_add.save()

                # Update Contractor Profile
                contra.name = contra_name
                contra.profile_photo = contractor_image
                contra.contact = contra_contact
                contra.contractor_address = contractor_add
                contra.save()
                return redirect('/contractor/profile/')
            except Exception as e:
                print(e)
                return HttpResponse(e)
        except KeyError:
            return redirect('/contractor/signin')


# Set Password
def set_password(request):
    if request.method == 'GET':
        request_token = request.GET['token']
        try:
            ResetToken.objects.get(token=request_token)

            request.session['setpassword'] = request_token
            return render(request, 'contractor/password.html')
        except ObjectDoesNotExist:
            data = {'title': 'Sorry :(', 'message': 'Link expired...', 'icon': 'error', 'url': '/contractor/signin/'}
            return render(request, 'contractor/login-page.html', data)

    if request.method == 'POST':
        try:
            request_token = request.session['setpassword']
            new_password = request.POST['password']
            resettoken = ResetToken.objects.get(token=request_token)
            contra = Contractor.objects.filter(email=resettoken.email).update(password=make_password(new_password))

            resettoken.delete()
            data = {'title': 'Thank you', 'message': 'Password setted successfully...', 'icon': 'success',
                    'url': '/contractor/signin/'}
            return render(request, 'contractor/password.html', data)
        except KeyError:
            data = {'title': 'Sorry :(', 'message': 'Session expired...', 'icon': 'error', 'url': '/contractor/signin/'}
            return render(request, 'contractor/signin.html', data)


# Change Password
def change_password(request):
    if request.method == 'GET':
        token = request.session['contractortoken']
        jwtToken = jwt.decode(token, 'jwt')
        if Contractor.objects.get(email=jwtToken['email']):

            return render(request, 'contractor/change-password.html')
        else:
            data = {'title': 'Sorry :(', 'message': 'Link expired...', 'icon': 'error', 'url': '/contractor/signin/'}
            return render(request, 'contractor/change-password.html', data)

    if request.method == 'POST':
        try:

            new_password = request.POST['password']
            token = request.session['contractortoken']
            jwtToken = jwt.decode(token, 'jwt')
            if Contractor.objects.get(email=jwtToken['email']):
                Contractor.objects.filter(email=jwtToken['email']).update(password=make_password(new_password))

                data = {'title': 'Thank you', 'message': 'Password setted successfully...', 'icon': 'success',
                        'url': '/contractor/signin/'}
                return render(request, 'contractor/password.html', data)
            else:
                data = {'title': 'Sorry :(', 'message': 'Link expired...', 'icon': 'error',
                        'url': '/contractor/signin/'}
                return render(request, 'contractor/change-password.html', data)
        except KeyError:
            data = {'title': 'Sorry :(', 'message': 'Session expired...', 'icon': 'error', 'url': '/contractor/signin/'}
            return render(request, 'contractor/change-password.html', data)


# Reset Password
import random


def reset_pass(request):
    if request.method == 'POST':
        contractor_email = request.POST['email']
        try:
            contra = Contractor.objects.get(email=contractor_email)

            # Create Token
            letters = string.digits + string.ascii_letters
            code = ''.join([random.choice(letters) for i in range(10)])
            params = {'token': code}
            # Add token and mail in ResetToken Model

            token = ResetToken(token=code, email=contractor_email)
            token.save()

            absolute_url = request.build_absolute_uri().rsplit("/", 3)[0]
            message = absolute_url + '/contractor/set_password?' + urllib.parse.urlencode(params)
            subject = "This mail for set a password just Click Below link to set a password Thank you for using our services demotestmail007@gmail.com"

            send_mail(subject, message, EMAIL_HOST_USER, [contractor_email], fail_silently=False)

            data = {"title": 'Link sent', "message": 'Please check mail for reset password...', "icon": 'success',
                    'url': '/contractor/signin/'}
            return render(request, 'contractor/login-page.html', data)

        except ObjectDoesNotExist:
            data = {'title': 'Try again', 'message': 'Email not found...', 'icon': 'error',
                    'url': '/contractor/signin/'}
            return render(request, 'contractor/login-page.html', data)
