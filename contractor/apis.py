from django.shortcuts import render,HttpResponse,redirect
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_protect
from django.forms.models import model_to_dict

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from contractor import serializers
from slp_admin.models import *
import jwt,json

# User Details
@api_view(['GET'])
def userDetails(request,userId):
    if request.method == 'GET':
        try:
            token = request.session['contractortoken']
            jwtToken = jwt.decode(token, 'jwt')
            try:
                contra = Contractor.objects.get(email = jwtToken['email'])
                user = SlpUser.objects.get(id = userId)
                scannedQRReward = ScannedQRCode.objects.filter(user=user)
                tasks = Task.objects.filter(contractor = contra.id, is_deleted=False)
                
                return render(request, 'contractor/user-profile.html',{'user':user, 'scannedQRReward':scannedQRReward,'tasks':tasks})
            except ObjectDoesNotExist:
                return redirect('/contractor/signin/')
        except ObjectDoesNotExist:
            return redirect('/contractor/signin/')

# Product Details
@api_view(['GET'])
def productDetails(request,productid):
    if request.method == 'GET':
        try:
            token = request.session['contractortoken']
            jwtToken = jwt.decode(token, 'jwt')
            try:
                contra = Contractor.objects.get(email = jwtToken['email'])
                try:
                    product = Product.objects.get(id =productid)
                except ObjectDoesNotExist:
                    product = []
                return render(request, 'contractor/view-product.html',{'product':product})
            except Exception as e :
                return HttpResponse(e)
        except KeyError:
            return redirect('/contractor/signin/')


# Job Categories
@api_view(['GET', 'POST'])
def jobcategories(request):
        #GET
        if request.method == 'GET':
            try:
                token = request.session['contractortoken']
                jwtToken = jwt.decode(token, 'jwt')
                try:
                    contra = Contractor.objects.get(email = jwtToken['email'])
                    jobs = Job.objects.filter(contractor = contra.id)
                    choices = Job._meta.get_field('job_status').choices
                    defaultChoices = dict((x,y) for x,y in choices)
                    
                    return render(request, 'contractor/jobcategories.html',{'jobs':jobs,'defaultChoices': defaultChoices})
                except ObjectDoesNotExist:
                    return redirect('/contractor/signin/')
            except KeyError:
                return redirect('/contractor/signin/')

        # POST
        if request.method == 'POST':
            try:
                token = request.session['contractortoken']
                jwtToken = jwt.decode(token, 'jwt')
                job_name = request.POST['name']
                job_status = request.POST['category']
                try:
                    contra = Contractor.objects.get(email = jwtToken['email'])
                    job = Job.objects.create(
                        job_name =job_name,
                        job_status = job_status,
                        contractor = contra,
                    )
                    job.save()
                    data = {"status": "success", "message":"Thank you", "data": "Category Added successfuly...",'url':'/contractor/jobcategories/'}
                    return HttpResponse(json.dumps(data), content_type='application/json')
                except ObjectDoesNotExist:
                    return redirect('/contractor/signin/')
            except KeyError:
                return redirect('/contractor/signin/')

# Tasks
@api_view(['GET', 'POST','PUT'])
def tasks(request):
        #GET
        if request.method == 'GET':
            try:
                token = request.session['contractortoken']
                jwtToken = jwt.decode(token, 'jwt')
                try:
                    contra = Contractor.objects.get(email = jwtToken['email'])
                    jobs = Job.objects.filter(contractor = contra.id)
                    users = SlpUser.objects.filter(company= contra.company_name)
                    tasks = Task.objects.filter(contractor = contra.id, is_deleted=False)
                    
                    return render(request, 'contractor/tasks.html',{'jobs':jobs,'users':users,'tasks':tasks})
                except ObjectDoesNotExist:
                    return redirect('/contractor/signin/')
            except KeyError:
                return redirect('/contractor/signin/')

        # POST
        if request.method == 'POST':
            
            try:
                token = request.session['contractortoken']
                jwtToken = jwt.decode(token, 'jwt')
                title = request.POST['title']
                # print("\n Title:",title)
                userId = request.POST['user']
                # print("\n User Id:",userId)
                user_job = request.POST['job']
                # print("\n User Job:",user_job)
                description = request.POST['desc']
                # print("\n Decription:",description)
                # print("\n----Inside Try-----\n")
                try:
                    contra = Contractor.objects.get(email = jwtToken['email'])
                    # print("\n Contractor", contra)
                    job = Job.objects.get(id = user_job)
                    # print("\n Job",job)
                    users = SlpUser.objects.get(id= userId)
                    # print("\n Users", users)
                    tasks = Task.objects.create(
                        title =title,
                        user = users,
                        job = job,
                        description = description,
                        contractor = contra,
                    )
                    tasks.save()
                    data = {"status": "success", "message":"Thank you", "data": "Task assignded...",'url':'/contractor/tasks/'}
                    return HttpResponse(json.dumps(data), content_type='application/json')
                except ObjectDoesNotExist:
                    return redirect('/contractor/signin/')
            except KeyError:
                return redirect('/contractor/signin/')
        
        # PUT
        if request.method == 'PUT':
            
            try:
                token = request.session['contractortoken']
                jwtToken = jwt.decode(token, 'jwt')
                taskId = request.POST['task_id']
                print("\n Task Id:",taskId)
                additionaPoints = request.POST['additionaPoints']
                try:
                    contra = Contractor.objects.get(email = jwtToken['email'])
                    # print("\n Contractor", contra)
                    
                    tasks = Task.objects.get(id=taskId)
                    tasksJob = tasks.job
                    tasksUser = tasks.user
                    print("\nTasks",tasks)
                    tasks.additional_points = additionaPoints
                    addPointsRequest = AdditionalPointRequest.objects.create(
                        contractor = contra,
                        job = tasksJob,
                        user = tasksUser,
                        additional_points = additionaPoints
                    )
                    tasks.save()
                    addPointsRequest.save()
                    # print('Taks',tasks.additional_points)
                    
                    data = {"status": "success", "message":"Thank you", "data": "Points added successfully...",'url':'/contractor/tasks/'}
                    return HttpResponse(json.dumps(data), content_type='application/json')
                except ObjectDoesNotExist:
                    return redirect('/contractor/signin/')
            except KeyError:
                return redirect('/contractor/signin/')

# Task Delete
@api_view(['GET'])
def deleteTask(request,taskid):
    try:
        token = request.session['contractortoken']
        jwtToken = jwt.decode(token, 'jwt')
        try:
            contra = Contractor.objects.get(email = jwtToken['email'])
            try:
                tasks = Task.objects.get(id=taskid,contractor=contra.id,status='Todo')
                tasks.is_deleted = True
                tasks.save()
                data = {"icon": "success", "title":"Thank you", "message": "Task Deleted successfully...",'url':'/contractor/tasks/'}
                return render(request, 'contractor/tasks.html',data)
            except ObjectDoesNotExist:
                data = {"icon": "error", "title":"Try again", "message": "Record not found..."}
                return render(request, 'contractor/tasks.html',data)
        except ObjectDoesNotExist:
            return redirect('/contractor/signin/')
    except KeyError:
        return redirect('/contractor/signin/')

# Task Due Bills
@api_view(['GET','POST'])
def taskduebils(request):
        #GET
        if request.method == 'GET':
            try:
                token = request.session['contractortoken']
                jwtToken = jwt.decode(token, 'jwt')
                try:
                    contra = Contractor.objects.get(email = jwtToken['email'])
                    # jobs = Job.objects.filter(contractor = contra.id)
                    # users = SlpUser.objects.filter(company= contra.company_name)
                    tasks = Task.objects.filter(contractor = contra.id)
                    # print('Taks',tasks.values('additional_points') )
                    points = {}
                    for point in tasks.values('additional_points'):
                        points.update(point)
                    addPointsRequest = AdditionalPointRequest.objects.filter(contractor=contra)
                    
                    return render(request, 'contractor/tasks-due-bills.html',{'tasks':tasks, 'addPointsRequest':addPointsRequest})
                except Exception as e:
                    return HttpResponse(e)
            except KeyError:
                return redirect('/contractor/signin/')