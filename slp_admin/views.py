import json
import random
import string
import urllib.parse

from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMultiAlternatives, EmailMessage
from django.core.mail import send_mail
from django.db.models import Count
from django.shortcuts import render, HttpResponse, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response

from SLP.settings import EMAIL_HOST_USER
from slp_admin.models import *


def add_video(request):
    try:
        admin_session = request.session['Admintoken']
    except:
        redirect("slpdashboard")

    if request.method == 'GET':
        admin_token = AdminToken.objects.get(token=admin_session)
        admin_info = SlpAdmin.objects.get(id=admin_token.admin.id)
        category = models.Category.objects.all()
        context = {
            "categories": category,
            'name': admin_info.first_name
        }
        return render(request, "add-videos.html", context)
    if request.method == "POST":
        category = request.POST['category_id']
        title = request.POST['title']
        video = request.FILES.get('video')
        description = request.POST['description']
        video = models.Video(category_id=category, title=title, description=description, video=video)
        video.save()
        return redirect('videos')


def edit_video(request, video_id):
    if request.method == 'GET':
        try:
            admin_session = request.session['Admintoken']
        except:
            redirect("slpdashboard")

        admin_token = AdminToken.objects.get(token=admin_session)
        admin_info = SlpAdmin.objects.get(id=admin_token.admin.id)
        video = models.Video.objects.get(id=video_id)
        category = models.Category.objects.all()
        context = {
            "categories": category,
            "videos": video,
            'name': admin_info.first_name
        }
        return render(request, "edit-videos.html", context)

    if request.method == "POST":
        video1 = models.Video.objects.filter(id=video_id)
        category = request.POST['category_id']
        title = request.POST['title']
        # video = request.FILES.get('video')
        description = request.POST['description']
        cat = models.Category.objects.get(id=category)
        video1.update(title=title, category=cat, description=description)
        return redirect('videos')


def delete_video(request, video_id):
    video = models.Video.objects.get(id=video_id)
    video.delete()
    return redirect('videos')


def videos(request):
    if request.method == 'GET':
        try:
            admin_session = request.session['Admintoken']
        except:
            redirect("slpdashboard")

        admin_token = AdminToken.objects.get(token=admin_session)
        admin_info = SlpAdmin.objects.get(id=admin_token.admin.id)
        video = models.Video.objects.all()
        context = {
            "videos": video,
            'name': admin_info.first_name
        }
        return render(request, "videos.html", context)


def category(request):
    if request.method == 'GET':
        try:
            admin_session = request.session['Admintoken']
        except:
            redirect("slpdashboard")

        admin_token = AdminToken.objects.get(token=admin_session)
        admin_info = SlpAdmin.objects.get(id=admin_token.admin.id)
        category = models.Category.objects.all()
        context = {
            "categories": category,
            'name': admin_info.first_name
        }
        return render(request, "videos-categories.html", context)
    if request.method == "POST":
        category = request.POST['category']
        category_new = models.Category(name=category)
        category_new.save()
        return redirect('category')


def delete_category(request, category_id):
    category = models.Category.objects.get(id=category_id)
    category.delete()
    return redirect('category')


def dashboard(request):
    return render(request, "admin_dashboard.html", {})


def contractor_list(request):
    try:
        admin_session = request.session['Admintoken']
    except:
        context = {
            'message': "Session Expired!",
            'url': '/slp_admin/login/',
            'icon': 'error',
        }
        return render(request, "admin_login.html", context)

    if request.method == 'GET':
        admin_token = AdminToken.objects.get(token=admin_session)
        admin_info = SlpAdmin.objects.get(id=admin_token.admin.id)
        print(request.build_absolute_uri().rsplit("/", 3)[0])
        contractors = Contractor.objects.all()
        return render(request, 'contractors.html', {'contractors': contractors, "name": admin_info.first_name})

    if request.method == 'POST':
        contractor_name = request.POST['name']
        contractor_email = request.POST['email']
        contractor_contact = request.POST['contact']
        contractor_company = request.POST['company_name']

        # Create Token
        letters = string.digits + string.ascii_letters
        code = ''.join([random.choice(letters) for i in range(10)])
        params = {'token': code}

        try:
            contra = Contractor.objects.get(email=contractor_email)
            data = {"title": 'Try again', "message": 'Email already exist', "icon": 'warning',
                    'url': '/slp_admin/contractors/'}
            return render(request, 'contractors.html', data)
        except ObjectDoesNotExist:
            try:
                contra = Contractor.objects.get(email=contractor_email)
                data = {"title": 'Try again', "message": 'Email already exist', "icon": 'warning',
                        'url': '/slp_admin/contractors/'}
                return render(request, 'contractors.html', data)
            except ObjectDoesNotExist:
                try:
                    contra = Contractor.objects.get(contact=contractor_contact)
                    data = {"title": 'Try again', "message": 'Contact number already exist', "icon": 'warning',
                            'url': '/slp_admin/contractors/'}
                    return render(request, 'contractors.html', data)
                except ObjectDoesNotExist:
                    contra = Contractor.objects.create(
                        name=contractor_name,
                        email=contractor_email,
                        contact=contractor_contact,
                        company_name=contractor_company,
                    )
                    contra.save()

                    # Add token and mail in ResetToken Model

                    token = ResetToken(token=code, email=contractor_email)
                    token.save()

                    absolute_url = request.build_absolute_uri().rsplit("/", 3)[0]
                    message = absolute_url + '/contractor/set_password?' + urllib.parse.urlencode(params)
                    subject = "This mail for set a password just Click Below link to set a password Thank you for using our services demotestmail007@gmail.com"

                    send_mail(subject, message, EMAIL_HOST_USER, [contractor_email], fail_silently=False)

                    data = {"title": 'Contractor added successfully',
                            "message": 'Please check mail for set password...', "icon": 'success'}
                    return render(request, 'contractors.html', data)


# Contractor Details
def contractor_dtl(request, contraId):
    try:
        admin_session = request.session['Admintoken']
    except:
        context = {
            'message': "Session Expired!",
            'url': '/slp_admin/login/',
            'icon': 'error',
        }
        return render(request, "admin_login.html", context)
    admin_token = AdminToken.objects.get(token=admin_session)
    admin_info = SlpAdmin.objects.get(id=admin_token.admin.id)
    contra = Contractor.objects.get(id=contraId)
    users = SlpUser.objects.filter(company=contra.company_name)
    return render(request, 'contractor-profile.html', {'contra': contra, 'users': users, "name": admin_info.first_name})


# Points Requests
def points_request(request):
    try:
        admin_session = request.session['Admintoken']
    except:
        context = {
            'message': "Session Expired!",
            'url': '/slp_admin/login/',
            'icon': 'error',
        }
        return render(request, "admin_login.html", context)

    if request.method == 'GET':
        admin_token = AdminToken.objects.get(token=admin_session)
        admin_info = SlpAdmin.objects.get(id=admin_token.admin.id)
        add_points = AdditionalPointRequest.objects.all()
        choices = AdditionalPointRequest._meta.get_field('action').choices
        defaultChoices = dict((x, y) for x, y in choices)
        return render(request, 'points-request.html',
                      {'add_points': add_points, 'defaultChoices': defaultChoices, "name": admin_info.first_name})
    if request.method == 'POST':
        try:
            print("\n", request.POST)
            addpointsId = request.POST['addpoint_id']
            print("\nAdditional id", addpointsId)
            pointsaction = request.POST['points_action']

            add_points = AdditionalPointRequest.objects.get(id=addpointsId)
            add_points.action = pointsaction

            print('\nPoints action', pointsaction == 'Resolved')
            add_points.save()
            if pointsaction == 'Resolved':
                user = SlpUser.objects.get(id=add_points.user.id)
                user.total_points += add_points.additional_points
                user.available_points += add_points.additional_points
                user.save()
                print("\nAvailabel points: ", user.available_points)
            # return redirect('/slp_admin/points-request/')
            data = {"icon": "success", "title": "Done", "message": "Action applied successfully...",
                    'url': '/slp_admin/points-request/'}
            return HttpResponse(json.dumps(data), content_type='application/json')

        except ObjectDoesNotExist:
            return redirect('/slp_admin/points-request/')


@api_view(['GET'])
def dashboard(request):
    try:
        admin_session = request.session['Admintoken']
    except:
        context = {
            'message': "Session Expired!",
            'url': '/slp_admin/login/',
            'icon': 'error',
        }
        return render(request, "admin_login.html", context)
    if request.method == "GET":
        admin_token = AdminToken.objects.get(token=admin_session)
        admin_info = SlpAdmin.objects.get(id=admin_token.admin.id)
        try:
            user_count = SlpUser.objects.all()
            print("count ", user_count.count())
            dashboar_list = {"user_count": user_count.count(),
                             "merchant_count": 0,
                             "videos_count": 0,
                             "products_count": 0,
                             "banner_count": 0,
                             "contractor_count": 0,
                             }
        except:
            print("SlpUser model Empty")
            user_count = 0

        try:
            merchant_count = Merchant.objects.all()
            dashboar_list = {"user_count": user_count.count(),
                             "merchant_count": merchant_count.count(),
                             "videos_count": 0,
                             "products_count": 0,
                             "banner_count": 0,
                             "contractor_count": 0,
                             }
        except:
            print("Merchant model Empty")
            merchant_count = 0

        try:
            video_count = Video.objects.all()
            dashboar_list = {"user_count": user_count.count(),
                             "merchant_count": merchant_count.count(),
                             "videos_count": video_count.count(),
                             "products_count": 0,
                             "banner_count": 0,
                             "contractor_count": 0,
                             }
        except:
            print("Video model Empty")
            video_count = 0
        try:
            product_count = Product.objects.all()
            dashboar_list = {"user_count": user_count.count(),
                             "merchant_count": merchant_count.count(),
                             "videos_count": video_count.count(),
                             "products_count": product_count.count(),
                             "banner_count": 0,
                             "contractor_count": 0,
                             }
        except:
            print("Product model Empty")
            product_count = 0

        try:
            banner_count = Banner.objects.all()
            dashboar_list = {"user_count": user_count.count(),
                             "merchant_count": merchant_count.count(),
                             "videos_count": video_count.count(),
                             "products_count": product_count.count(),
                             "banner_count": banner_count.count(),
                             "contractor_count": 0,
                             }
        except:
            print("Banner model Empty")
            banner_count = 0

        try:
            contractor_count = Contractor.objects.all()
            dashboar_list = {"user_count": user_count.count(),
                             "merchant_count": merchant_count.count(),
                             "videos_count": video_count.count(),
                             "products_count": product_count.count(),
                             "banner_count": banner_count.count(),
                             "contractor_count": contractor_count.count(),
                             }
        except:
            print("Banner model Empty")
            banner_count = 0

        context = {"count": dashboar_list, "name": admin_info.first_name}
        return render(request, "admin_dashboard.html", context)


@api_view(['POST', 'GET'])
def change_password(request):
    verify_token = request.session['Admintoken']
    # return render(request , "admin_login.html" , {"context" : "Session Expired"})
    print("token", verify_token)
    try:
        admin = AdminToken.objects.get(token=verify_token)
    except:
        context = {
            'message': "Invalid token or Account not found!",
            'url': '/slp_admin/login/',
            'icon': 'error',
        }
        return render(request, "admin_edit-profile.html", context)
    try:
        admin_info = SlpAdmin.objects.get(id=admin.admin.id)
    except:
        context = {
            'message': "Admin account not found!",
            'url': '/slp_admin/login/',
            'icon': 'error',
        }
        return render(request, "admin_login.html", context)

    if request.method == 'GET':
        context = {"name": admin_info.first_name}
        return render(request, "admin_edit-profile.html", context)

    if request.method == 'POST':

        password = request.POST['password']
        old_passwrd = request.POST['old_pass']
        confrm_password = request.POST['cnfm_pass']

        try:
            SlpAdmin.objects.get(password=old_passwrd)
        except:
            context = {"message": "Password Incorrect",
                       'icon': 'error',
                       "password": password,
                       "old_passwrd": old_passwrd,
                       "name": admin_info.first_name}
            return render(request, "admin_edit-profile.html", context)

        if password == old_passwrd:
            context = {"message": "Old Password same as New Password",
                       'icon': 'error',
                       "password": password,
                       "old_passwrd": old_passwrd,
                       "name": admin_info.first_name}
            return render(request, "admin_edit-profile.html", context)

        if password != confrm_password:
            context = {"message": "Password and Confirm Password aren't same",
                       'icon': 'error',
                       "password": password,
                       "old_passwrd": old_passwrd,
                       "name": admin_info.first_name}
            return render(request, "admin_edit-profile.html", context)

        admin_pass = SlpAdmin.objects.get(id=admin.admin.id)
        admin_pass.password = password
        print("idddddddd", admin.admin.id)
        admin_pass.save()
        context = {"message": "Password Updated",
                   'icon': 'success',
                   'url': '/slp_admin/login/',
                   "name": admin_info.first_name}
        return render(request, "admin_edit-profile.html", context)


@api_view(['GET', 'POST'])
def forget_password(request):
    print("in method forget")
    if request.method == 'POST':
        email = request.POST['resetEmail']
        try:
            admin_email = SlpAdmin.objects.get(email=email)
        except:
            context = {
                'message': "Email not Registerd!",
                'url': '/slp_admin/login/',
                'icon': 'error',
            }
            return render(request, "admin_login.html", context)
        try:
            ids = admin_email.id
            subject = 'hello'
            text_content = 'http://127.0.0.1:8000/slp_admin/reset_password/admin_email.id/'
            data = 'Please Click the link to Reset your Password'
            content = '<br><a href="http://127.0.0.1:8000/slp_admin/reset_password/' + str(
                ids) + '/"><button type="button"> CLICK </button></a>'
            html_content = data + content
            # msg = send_mail(subject,message, EMAIL_HOST_USER, [email], fail_silently = False)
            # send_mail(subject,message, EMAIL_HOST_USER, [email], fail_silently = False)
            msg = EmailMessage(subject, html_content, EMAIL_HOST_USER, [email])
            msg.content_subtype = "html"  # Main content is now text/html
            msg = EmailMultiAlternatives(subject, text_content, EMAIL_HOST_USER, [email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            print("email sent")
        except Exception as e:
            print(e)
            return Response("error")
        context = {
            'message': "Email is Sent",
            'url': '/slp_admin/login/',
            'icon': 'success',
        }
        return render(request, "admin_login.html", context)


@api_view(['POST', 'GET'])
def reset_password(request, id):
    print("idddd_reset", id)
    if request.method == 'GET':
        resetPass = SlpAdmin.objects.get(id=id)
        return render(request, "admin_2reset_password.html")

    if request.method == 'POST':
        newPass = request.POST['new_password']
        cnfmPass = request.POST['confirm_password']
        print("new pass", newPass)
        if newPass != cnfmPass:
            context = {
                'message': "Your New Password and Confirm Password Does not Match!",
                'url': '/slp_admin/reset_password/' + str(id) + '/',
                'icon': 'error',
            }
            return render(request, "admin_2reset_password.html", context)
        resetPass = SlpAdmin.objects.get(id=id)
        resetPass.password = newPass
        resetPass.save()
        context = {
            'message': "Password Reset",
            'url': '/slp_admin/login/',
            'icon': 'success',
        }
        return render(request, "admin_2reset_password.html", context)


def purchased_gift_page(request):
    try:
        admin_session = request.session['Admintoken']
    except:
        context = {
            'message': "Session Expired!",
            'url': '/slp_admin/login/',
            'icon': 'error',
        }
        return render(request, "admin_login.html", context)

    if request.method == 'GET':
        admin_token = AdminToken.objects.get(token=admin_session)
        admin_info = SlpAdmin.objects.get(id=admin_token.admin.id)
        obj = PurchasedGifts.objects.all()
        template_name = "purchased_gifts.html"
        return render(request, template_name, {'gift_log': obj, 'name': admin_info.first_name})


from slp_admin import models


def qr_codes(request):
    try:
        admin_session = request.session['Admintoken']
    except:
        redirect("slpdashboard")

    if request.method == 'GET':
        admin_token = AdminToken.objects.get(token=admin_session)
        admin_info = SlpAdmin.objects.get(id=admin_token.admin.id)
        scanned_qr = models.ScannedQRCode.objects.all()
        context = {
            "scanned_qr": scanned_qr,
            'name': admin_info.first_name
        }
        return render(request, "qr-codes.html", context)


def dispute_requests(request):
    try:
        admin_session = request.session['Admintoken']
    except:
        redirect("slpdashboard")

    if request.method == 'GET':
        admin_token = AdminToken.objects.get(token=admin_session)
        admin_info = SlpAdmin.objects.get(id=admin_token.admin.id)
        disputes = models.Dispute.objects.all()
        context = {
            "disputes": disputes,
            'name': admin_info.first_name
        }
        return render(request, "dispute-request.html", context)


def merchant(request, id):
    try:
        admin_session = request.session['Admintoken']
    except:
        redirect("slpdashboard")

    if request.method == 'GET':
        admin_token = AdminToken.objects.get(token=admin_session)
        admin_info = SlpAdmin.objects.get(id=admin_token.admin.id)

        print("admin_info", admin_info)
        merchant_detail = Merchant.objects.get(id=id)
        products_detail = Product.objects.filter(merchant_id=merchant_detail.id)

        context = {'name': admin_info.first_name, 'merchant_detail': merchant_detail,
                   'products_detail': products_detail}

        return render(request, 'slp_admin/merchant.html', context)


def add_merchant(request):
    try:
        admin_session = request.session['Admintoken']
    except:
        redirect("slpdashboard")

    if request.method == 'GET':
        admin_token = AdminToken.objects.get(token=admin_session)
        admin_info = SlpAdmin.objects.get(id=admin_token.admin.id)
        return render(request, 'slp_admin/add_merchant.html', {'name': admin_info.first_name})
        if request.method == 'POST':
            try:
                merchant_name = request.POST['merchant_name']

                merchant_email = request.POST['merchant_email']
                merchant_phone_number = request.POST['merchant_phone_number']
                merchant = Merchant(name=merchant_name, email=merchant_email, phone=merchant_phone_number)
                print(merchant)

                import string
                import random
                import urllib.parse
                letters = string.digits + string.ascii_letters
                code = ''.join([random.choice(letters) for i in range(10)])
                params = {'token': code}

                letters = string.digits + string.ascii_letters
                code = ''.join([random.choice(letters) for i in range(10)])
                params = {'token': code}

                token = ResetToken(token=code, email=merchant_email)
                token.save()

                if not ResetToken.objects.filter(token=token.token):
                    print("not found")
                else:
                    message = 'http://127.0.0.1:8000/merchant/reset_password?' + urllib.parse.urlencode(params)
                    subject = "This mail for reset password just Click Below link to reset password Thank you for using our services parasdabhi2021@gmail.com"

                    send_mail(subject, message, EMAIL_HOST_USER, [merchant_email], fail_silently=False)

                merchant.save()
                return redirect('view_merchant')
            except Exception as e:
                print(e)


def view_merchant(request):
    # admin_token = AdminToken.objects.get(token=admin_session)
    # admin_info = SlpAdmin.objects.get(id=admin_token.admin.id)
    # merchant_list = Merchant.objects.annotate(num_of_products=models.Count('product')).filter(is_deleted="False")

    try:
        admin_session = request.session['Admintoken']
    except:
        redirect("slpdashboard")

    if request.method == 'GET':
        admin_token = AdminToken.objects.get(token=admin_session)
        admin_info = SlpAdmin.objects.get(id=admin_token.admin.id)
        merchant_list = Merchant.objects.all().annotate(num_of_products=Count('product')).filter(is_deleted="False")

    context = {
        'merchant_list': merchant_list,
        'name': admin_info.first_name

    }
    return render(request, 'slp_admin/view_merchant.html', context)


def delete_merchant(request, id):
    Merchant.objects.filter(id=id).update(is_deleted="True")
    return redirect('view_merchant')


def merchant_status(request):
    """Update merchant status like Block/ Unblock"""
    status = request.POST['status']
    merchant_id = request.POST['id']
    if request.method == 'POST':
        status = request.POST['status']
        merchant_id = request.POST['id']

        if status == 'Unblock':
            merchant_update = Merchant.objects.filter(id=merchant_id).update(status='Block')
            merchant = Merchant.objects.get(id=merchant_id)
            return HttpResponse({'status': merchant.status})
        else:
            merchant_update = Merchant.objects.filter(id=merchant_id).update(status='Unblock')
            merchant = Merchant.objects.get(id=merchant_id)
            return HttpResponse({'status': merchant.status})


def add_products(request):
    try:
        admin_session = request.session['Admintoken']
    except:
        redirect("slpdashboard")

    if request.method == 'GET':
        admin_token = AdminToken.objects.get(token=admin_session)
        admin_info = SlpAdmin.objects.get(id=admin_token.admin.id)
        merchant_list = Merchant.objects.all()
        context = {'merchant_list': merchant_list, 'name': admin_info.first_name}
        return render(request, 'slp_admin/add-products.html', context)

    if request.method == 'POST':

        techncal_file_count = int(request.POST['technical_uploaded_file_count'])
        technical_file_list = []
        for tech_count in range(techncal_file_count):
            techcou = str(tech_count)
            tech_file = request.FILES.get('technical_datasheet_' + techcou + '')

            if tech_file is None:
                continue
                techfileobj = TechnicalFiles.objects.create(
                    technical_data_sheet=request.FILES.get('technical_datasheet_' + techcou + '')
                )
                technical_file_list.append(techfileobj)
            else:
                techfileobj = TechnicalFiles.objects.create(
                    technical_data_sheet=request.FILES.get('technical_datasheet_' + techcou + '')
                )
                technical_file_list.append(techfileobj)

        guideline_file_count = int(request.POST['guidelines_uploaded_file_count'])
        guideline_file_list = []
        for guide_count in range(guideline_file_count):
            guidecou = str(guide_count)
            guide_file = request.FILES.get('application_guidelines_' + guidecou + '')

            if guide_file is None:
                continue
                guidefileobj = TechnicalFiles.objects.create(
                    application_guidelines=request.FILES.get('application_guidelines_' + guidecou + '')
                )
                guideline_file_list.append(guidefileobj)
            else:
                guidefileobj = AppilicationGuideLineFiles.objects.create(
                    application_guidelines=request.FILES.get('application_guidelines_' + guidecou + '')
                )
                guideline_file_list.append(guidefileobj)

        video_file_count = int(request.POST['video_uploaded_file_count'])
        video_file_list = []
        for video_count in range(video_file_count):
            videocou = str(video_count)
            video_file = request.FILES.get('videofile_' + videocou + '')

            if video_file is None:
                continue
                videofileobj = VideoFiles.objects.create(
                    video=request.FILES.get('videofile_' + videocou + '')
                )
                video_file_list.append(videofileobj)
            else:
                videofileobj = VideoFiles.objects.create(
                    video=request.FILES.get('videofile_' + videocou + '')
                )
                video_file_list.append(videofileobj)

        safety_file_count = int(request.POST['safety_datasheet_uploaded_file_count'])
        safety_file_list = []
        for safety_count in range(safety_file_count):
            safetycou = str(safety_count)
            safety_file = request.FILES.get('safety_datasheet_file_' + safetycou + '')

            if safety_file is None:
                continue
                safetyfileobj = SafetyFiles.objects.create(
                    safety_data_sheet=request.FILES.get('safety_datasheet_file_' + safetycou + '')
                )
                safety_file_list.append(safetyfileobj)
            else:
                safetyfileobj = SafetyFiles.objects.create(
                    safety_data_sheet=request.FILES.get('safety_datasheet_file_' + safetycou + '')
                )
                safety_file_list.append(safetyfileobj)

        certificate_file_count = int(request.POST['certificate_file_count'])
        certificate_file_list = []
        for certificate_count in range(certificate_file_count):
            certificatecou = str(certificate_count)
            certificate_file = request.FILES.get('certificate_file_' + certificatecou + '')

            if certificate_file is None:
                continue
                certificatefileobj = Certificate.objects.create(
                    certificate=request.FILES.get('certificate_file_' + certificatecou + '')
                )
                certificate_file_list.append(certificatefileobj)
            else:
                certificatefileobj = Certificate.objects.create(
                    certificate=request.FILES.get('certificate_file_' + certificatecou + '')
                )
                certificate_file_list.append(certificatefileobj)

        # Product model fields
        merchant_id = request.POST['merchant_id']
        product_name = request.POST['product_name']
        product_description = request.POST['product_description']
        product_image = request.FILES.get('product_image')
        # print("product image is ",product_image)

        # ProductActivationDetail model fields
        a_side_batch = request.POST['a_side_batch']
        b_side_set_temp = request.POST['b_side_set_temp']
        a_side_set_temp = request.POST['a_side_set_temp']
        hot_set_temp = request.POST['hot_set_temp']
        mixing_chamber_size = request.POST['mixing_chamber_size']
        pressure_set = request.POST['pressure_set']
        starting_drum_temperature = request.POST['starting_drum_temperature']

        qr_code_scan_reward = request.POST['qr_code_scan_reward']
        a_side_batch_reward = request.POST['a_side_batch_reward']
        a_side_set_temp_reward = request.POST['a_side_set_temp_reward']
        b_side_set_temp_reward = request.POST['b_side_set_temp_reward']
        hot_set_temp_reward = request.POST['hot_set_temp_reward']
        pressure_set_reward = request.POST['pressure_set_reward']
        mixing_chamber_size_reward = request.POST['mixing_chamber_size_reward']
        photo_of_install_foam_reward = request.POST['photo_of_install_foam_reward']
        starting_drum_temperature_point_reward = request.POST['starting_drum_temperature_point_reward']
        total_point = request.POST['total_points']
        product = Product(merchant_id=merchant_id, product_name=product_name,
                          product_description=product_description,
                          product_image=product_image, Technical_file=technical_file_list,
                          application_guidelines=guideline_file_list,
                          video=video_file_list,
                          safety_data_sheet=safety_file_list,
                          certificate=certificate_file_list,
                          a_side_batch=a_side_batch,
                          a_side_set_temperature=a_side_set_temp,
                          b_side_set_temperature=b_side_set_temp,
                          hot_set_temperature=hot_set_temp,
                          mixing_chamber_size=mixing_chamber_size,
                          pressure_set=pressure_set,
                          starting_drum_temperature=starting_drum_temperature,
                          qr_code_scan_reward=qr_code_scan_reward,
                          a_side_batch_reward=a_side_batch_reward,
                          a_side_set_temp_reward=a_side_set_temp_reward,
                          b_side_set_temp_reward=b_side_set_temp_reward,
                          hot_set_temp_reward=hot_set_temp_reward,
                          pressure_set_reward=pressure_set_reward,
                          mixing_chamber_size_reward=mixing_chamber_size_reward,
                          photo_of_install_foam_reward=photo_of_install_foam_reward,
                          starting_drum_temperature_point_reward=starting_drum_temperature_point_reward,
                          total_point=total_point,
                          )
        product.save()

        merchant_list = Merchant.objects.all()
        context = {'merchant_list': merchant_list}
        return render(request, 'slp_admin/add-products.html', context)


def products(request):
    try:
        admin_session = request.session['Admintoken']
    except:
        redirect("slpdashboard")

    if request.method == 'GET':
        admin_token = AdminToken.objects.get(token=admin_session)
        admin_info = SlpAdmin.objects.get(id=admin_token.admin.id)
        product_list = Product.objects.select_related('merchant').filter(merchant__is_deleted=False, is_deleted=False)
        context = {'product_list': product_list, 'name': admin_info.first_name}
        return render(request, 'slp_admin/products.html', context)


def delete_product(request, id):
    Product.objects.filter(id=id).update(is_deleted="True")
    return redirect('products')


def edit_product(request, id):
    try:
        admin_session = request.session['Admintoken']
    except:
        redirect("slpdashboard")

    if request.method == 'GET':
        admin_token = AdminToken.objects.get(token=admin_session)
        admin_info = SlpAdmin.objects.get(id=admin_token.admin.id)

        numbers = []
        mixing_chamber_size = []
        pressure_set = []
        starting_drum_temperature = []
        for i in range(100, 150):
            numbers.append(i)
        for i in range(0, 4):
            mixing_chamber_size.append(i)
        for i in range(900, 1500, 25):
            pressure_set.append(i)
        for i in range(40, 120):
            starting_drum_temperature.append(i)

        product_detail = Product.objects.get(id=id)
        merchant_list = Merchant.objects.all()
        merchant_name = []
        for merchanob in merchant_list:
            merchant_name.append(merchanob)
        count = 0
        context = {
            'product_detail': product_detail,
            'numbers': numbers,
            'mixing_chamber_size': mixing_chamber_size,
            'pressure_set': pressure_set,
            'count': count,
            'starting_drum_temperature': starting_drum_temperature,
            'merchant_list': merchant_list,
            'merchant_name': merchant_name,
            'name': admin_info.first_name
        }
        return render(request, 'slp_admin/edit-product.html', context)
    if request.method == 'POST':

        techncal_file_count = int(request.POST['technical_uploaded_file_count'])
        technical_file_list = []
        product_data = Product.objects.get(id=id)
        previous_tech_data = product_data.Technical_file
        for techobj in previous_tech_data:
            technical_file_list.append(techobj)
        for tech_count in range(techncal_file_count):
            techcou = str(tech_count)
            tech_file = request.FILES.get('technical_datasheet_' + techcou + '')

            if tech_file is None:
                continue
                techfileobj = TechnicalFiles.objects.create(
                    technical_data_sheet=request.FILES.get('technical_datasheet_' + techcou + '')
                )
                technical_file_list.append(techfileobj)
            else:
                techfileobj = TechnicalFiles.objects.create(
                    technical_data_sheet=request.FILES.get('technical_datasheet_' + techcou + '')
                )
                technical_file_list.append(techfileobj)

        guideline_file_count = int(request.POST['guidelines_uploaded_file_count'])
        guideline_file_list = []
        previous_guide_data = product_data.application_guidelines
        for guideobj in previous_guide_data:
            guideline_file_list.append(guideobj)
        for guide_count in range(guideline_file_count):
            guidecou = str(guide_count)
            guide_file = request.FILES.get('application_guidelines_' + guidecou + '')

            if guide_file is None:
                continue
                guidefileobj = TechnicalFiles.objects.create(
                    application_guidelines=request.FILES.get('application_guidelines_' + guidecou + '')
                )
                guideline_file_list.append(guidefileobj)
            else:
                guidefileobj = AppilicationGuideLineFiles.objects.create(
                    application_guidelines=request.FILES.get('application_guidelines_' + guidecou + '')
                )
                guideline_file_list.append(guidefileobj)

        video_file_count = int(request.POST['video_uploaded_file_count'])
        video_file_list = []
        previous_video_data = product_data.video
        for vidobj in previous_video_data:
            video_file_list.append(vidobj)
        for video_count in range(video_file_count):
            videocou = str(video_count)
            video_file = request.FILES.get('videofile_' + videocou + '')

            if video_file is None:
                continue
                videofileobj = VideoFiles.objects.create(
                    video=request.FILES.get('videofile_' + videocou + '')
                )
                video_file_list.append(videofileobj)
            else:
                videofileobj = VideoFiles.objects.create(
                    video=request.FILES.get('videofile_' + videocou + '')
                )
                video_file_list.append(videofileobj)

        safety_file_count = int(request.POST['safety_datasheet_uploaded_file_count'])
        safety_file_list = []
        previous_safety_data = product_data.safety_data_sheet
        for safetyobj in previous_safety_data:
            safety_file_list.append(safetyobj)
        for safety_count in range(safety_file_count):
            safetycou = str(safety_count)
            safety_file = request.FILES.get('safety_datasheet_file_' + safetycou + '')

            if safety_file is None:
                continue
                safetyfileobj = SafetyFiles.objects.create(
                    safety_data_sheet=request.FILES.get('safety_datasheet_file_' + safetycou + '')
                )
                safety_file_list.append(safetyfileobj)
            else:
                safetyfileobj = SafetyFiles.objects.create(
                    safety_data_sheet=request.FILES.get('safety_datasheet_file_' + safetycou + '')
                )
                safety_file_list.append(safetyfileobj)

        certificate_file_count = int(request.POST['certificate_file_count'])
        certificate_file_list = []
        previous_certificate_data = product_data.certificate
        for certiobj in previous_certificate_data:
            certificate_file_list.append(certiobj)
        for certificate_count in range(certificate_file_count):
            certificatecou = str(certificate_count)
            certificate_file = request.FILES.get('certificate_file_' + certificatecou + '')
            if certificate_file is None:
                continue
                certificatefileobj = Certificate.objects.create(
                    certificate=request.FILES.get('certificate_file_' + certificatecou + '')
                )
                certificate_file_list.append(certificatefileobj)
            else:
                certificatefileobj = Certificate.objects.create(
                    certificate=request.FILES.get('certificate_file_' + certificatecou + '')
                )
                certificate_file_list.append(certificatefileobj)

        # Product model fields
        merchant_id = request.POST['merchant_id']
        product_name = request.POST['product_name']
        product_description = request.POST['product_description']
        product_image = request.FILES.get('product_image')
        # print("product image is ",product_image)

        # ProductActivationDetail model fields
        a_side_batch = request.POST['a_side_batch']
        b_side_set_temp = request.POST['b_side_set_temp']
        a_side_set_temp = request.POST['a_side_set_temp']
        hot_set_temp = request.POST['hot_set_temp']
        mixing_chamber_size = request.POST['mixing_chamber_size']
        pressure_set = request.POST['pressure_set']
        starting_drum_temperature = request.POST['starting_drum_temperature']

        # ArrayModelField all model

        qr_code_scan_reward = request.POST['qr_code_scan_reward']
        a_side_batch_reward = request.POST['a_side_batch_reward']
        a_side_set_temp_reward = request.POST['a_side_set_temp_reward']
        b_side_set_temp_reward = request.POST['b_side_set_temp_reward']
        hot_set_temp_reward = request.POST['hot_set_temp_reward']
        pressure_set_reward = request.POST['pressure_set_reward']
        mixing_chamber_size_reward = request.POST['mixing_chamber_size_reward']
        photo_of_install_foam_reward = request.POST['photo_of_install_foam_reward']
        starting_drum_temperature_point_reward = request.POST['starting_drum_temperature_point_reward']
        total_point = request.POST.get('total_points')
        print("Total point is ", total_point)

        product = Product.objects.filter(id=id).update(merchant_id=merchant_id, product_name=product_name,
                                                       product_description=product_description,
                                                       product_image=product_image,
                                                       Technical_file=technical_file_list,
                                                       application_guidelines=guideline_file_list,
                                                       video=video_file_list,
                                                       safety_data_sheet=safety_file_list,
                                                       certificate=certificate_file_list,
                                                       a_side_batch=a_side_batch,
                                                       a_side_set_temperature=a_side_set_temp,
                                                       b_side_set_temperature=b_side_set_temp,
                                                       hot_set_temperature=hot_set_temp,
                                                       mixing_chamber_size=mixing_chamber_size,
                                                       pressure_set=pressure_set,
                                                       starting_drum_temperature=starting_drum_temperature,
                                                       qr_code_scan_reward=qr_code_scan_reward,
                                                       a_side_batch_reward=a_side_batch_reward,
                                                       a_side_set_temp_reward=a_side_set_temp_reward,
                                                       b_side_set_temp_reward=b_side_set_temp_reward,
                                                       hot_set_temp_reward=hot_set_temp_reward,
                                                       pressure_set_reward=pressure_set_reward,
                                                       mixing_chamber_size_reward=mixing_chamber_size_reward,
                                                       photo_of_install_foam_reward=photo_of_install_foam_reward,
                                                       starting_drum_temperature_point_reward=starting_drum_temperature_point_reward,
                                                       total_point=total_point,
                                                       )
        return redirect('products')


def edit_product_tech_file(request):
    if request.method == 'POST':
        tech_id = request.POST.get('tech_file_id')
        product_id = request.POST.get('product_id')
        tech_detail = TechnicalFiles.objects.get(tech_file_id=tech_id)
        productObj = Product.objects.get(id=product_id)
        techfileObj = productObj.Technical_file
        for obj in techfileObj:
            if int(tech_id) == obj.tech_file_id:
                productObj.Technical_file.pop(techfileObj.index(obj))
                print("success delete")
        productObj.save()
        tech_detail.delete()
        return HttpResponse({'messgae': 'Deleted'})


def edit_product_guide_file(request):
    if request.method == 'POST':
        guide_file_id = request.POST.get('guide_file_id')
        product_id = request.POST.get('product_id')
        guide_detail = AppilicationGuideLineFiles.objects.get(app_guide_file_id=guide_file_id)
        print("guide_detail", guide_detail)
        productObj1 = Product.objects.get(id=product_id)
        guidefileObj = productObj1.application_guidelines
        for obj in guidefileObj:
            if int(guide_file_id) == obj.app_guide_file_id:
                productObj1.application_guidelines.pop(guidefileObj.index(obj))
        productObj1.save()
        guide_detail.delete()
    return HttpResponse({'messgae': 'Deleted'})


def edit_product_video_file(request):
    if request.method == 'POST':
        video_file_id = request.POST.get('video_file_id')
        product_id = request.POST.get('product_id')
        video_detail = VideoFiles.objects.get(video_file_id=video_file_id)
        print("guide_detail", video_detail)
        productObj1 = Product.objects.get(id=product_id)
        videofileObj = productObj1.video
        for obj in videofileObj:
            if int(video_file_id) == obj.video_file_id:
                productObj1.video.pop(videofileObj.index(obj))
        productObj1.save()
        video_detail.delete()
    return HttpResponse({'messgae': 'Deleted'})


def edit_product_safety_file(request):
    if request.method == 'POST':
        safety_file_id = request.POST.get('safety_file_id')
        product_id = request.POST.get('product_id')
        safety_detail = SafetyFiles.objects.get(safety_file_id=safety_file_id)
        print("safety_detail", safety_detail)
        productObj1 = Product.objects.get(id=product_id)
        safetyfileObj = productObj1.safety_data_sheet
        for obj in safetyfileObj:
            if int(safety_file_id) == obj.safety_file_id:
                productObj1.safety_data_sheet.pop(safetyfileObj.index(obj))
        productObj1.save()
        safety_detail.delete()
    return HttpResponse({'messgae': 'Deleted'})


def edit_product_certificate_file(request):
    if request.method == 'POST':
        certificate_file_id = request.POST.get('certificate_file_id')
        product_id = request.POST.get('product_id')
        certificate_detail = Certificate.objects.get(certificate_id=certificate_file_id)
        print("safety_detail", certificate_detail)
        productObj1 = Product.objects.get(id=product_id)
        certificatefileObj = productObj1.certificate
        for obj in certificatefileObj:
            if int(certificate_file_id) == obj.certificate_id:
                productObj1.certificate.pop(certificatefileObj.index(obj))
        productObj1.save()
        certificate_detail.delete()
    return HttpResponse({'messgae': 'Deleted'})


def view_slp_product(request, id):
    try:
        admin_session = request.session['Admintoken']
    except:
        redirect("slpdashboard")

    if request.method == 'GET':
        admin_token = AdminToken.objects.get(token=admin_session)
        admin_info = SlpAdmin.objects.get(id=admin_token.admin.id)
        product_detail = Product.objects.select_related('merchant').get(pk=id)
        return render(request, 'slp_admin/view-product.html',
                      {'product_detail': product_detail, 'name': admin_info.first_name})
