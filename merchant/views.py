import json
import os
import zipfile
from random import randint, sample

import pyqrcode
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.core.exceptions import ObjectDoesNotExist
from django.core.files import File
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect

from SLP.settings import EMAIL_HOST_USER
from slp_admin.models import *

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO, BytesIO

import jwt


# Create your views here.

def dashboard_page(request):
    try:
        token = request.session['merchanttoken']
        jwtToken = jwt.decode(token, 'merchant_jwt_key')
    except KeyError:
        return redirect('merchant_login')

    try:
        merchant = Merchant.objects.get(email=jwtToken['email'])
        batch_count = Batch.objects.filter()
        return render(request, 'merchant/dashboard.html')
    except Exception as e:
        return HttpResponse(e)


def merchant_login(request):
    if request.method == 'POST':
        try:
            if Merchant.objects.get(email=request.POST['email']):
                print("request.POST['email']", request.POST['email'])
                obj = Merchant.objects.get(email=request.POST['email'])
                if obj.password is not None:
                    if (check_password(request.POST['password'], obj.password)):

                        sequence = [i for i in range(100)]
                        smple = sample(sequence, 5)
                        merchant_token = ''.join(map(str, smple))
                        jwtToken = jwt.encode({'email': obj.email, 'jti': merchant_token}, 'merchant_jwt_key', )
                        token = jwtToken.decode("utf-8")
                        request.session['merchanttoken'] = token
                        request.session['name'] = obj.name
                        data = {"status": "success", "message": "Thank you", "data": "Login successfully...",
                                'jwtToken': token}
                        # return render(request, 'merchant/dashboard.html', {'data': json.dumps(data)})
                        return redirect('dashboard')
                    else:
                        data = {"status": "warning", "message": "Try again...", "data": "Password invalid..."}
                        return render(request, 'merchant/login-page.html', data)
                else:
                    return render(request, 'merchant/login-page.html')
            else:
                return render(request, "merchant/login-page.html", {"error": 'Email does not exists'})
        except Exception as e:
            print("error is ", e)
            return render(request, "merchant/login-page.html", {"error": 'Please try again later'})
    else:
        return render(request, 'merchant/login-page.html')

def logout(request):
    try:
        token = request.session['merchanttoken']
        jwtToken = jwt.decode(token, 'merchant_jwt_key')
        try:
            merchant = Merchant.objects.get(email=jwtToken['email'])
            del request.session['merchanttoken']
            del request.session['name']
            data = {"status": "success", "message": "Bye...", "data": "You are logged out...",
                    "url": "/contractor/signin/"}
            return redirect('merchant_login')
        except ObjectDoesNotExist:
            return redirect('merchant_login')
    except KeyError:
        return redirect('merchant_login')

def add_batch(request):
    try:
        token = request.session['merchanttoken']
        jwtToken = jwt.decode(token, 'merchant_jwt_key')
        try:
            if request.method == 'GET':
                products = Product.objects.all()
                context = {'products': products}
                return render(request, 'merchant/add-batch.html', context)
            if request.method == 'POST':
                try:
                    product_id = request.POST['product_id']
                    batch_number = request.POST['batch_number']

                    batch_start_date = request.POST['batch_start_date']
                    batch_start_time = request.POST['batch_start_time']
                    batch_quantity = request.POST['batch_quantity']

                    # code = pyqrcode.create('Are you suggesting coconuts migrate?')
                    # code.png('swallow.png', scale=5)
                    # code.png('swallow.png', scale=5, module_color=(0x66, 0x33, 0x0),
                    #          background=(0xff, 0xff, 0xff, 0x88))

                    batchobj = Batch(product_id=product_id, batch_name=batch_number, quantity=batch_quantity,
                                     start_date=batch_start_date, start_time=batch_start_time)
                    batchobj.save()
                    latest_batch_record = Batch.objects.latest('id')
                    print("latest_batch_id", latest_batch_record.id)

                    product_data = Product.objects.get(id=product_id)

                    def random_with_N_digits(n):
                        range_start = 10 ** (n - 1)
                        range_end = (10 ** n) - 1
                        return randint(range_start, range_end)

                    for i in range(int(batch_quantity)):
                        randomNumber = random_with_N_digits(8)
                        qr_code = randint(100000, 99999999)
                        qr_dict = {
                            "merchant_id": product_data.merchant_id,
                            "product_id": batchobj.product_id,
                            "qr_code": qr_code
                        }
                        qrjson = json.dumps(qr_dict)

                        code = pyqrcode.create(qrjson)
                        code.png(settings.MEDIA_ROOT + '/qr/' + str(randomNumber) + 'qrcode.png', scale=5)
                        reopen = open(settings.MEDIA_ROOT + '/qr/' + str(randomNumber) + 'qrcode.png', "rb+")
                        # print("basename", os.path.basename(reopen.name))
                        django_file = File(reopen)
                        print("qr/" + os.path.basename(reopen.name))
                        data = QrCodes.objects.create(product_id=product_id, batch_id=latest_batch_record.id,
                                                      qr_code="qr/" + os.path.basename(reopen.name))
                    return redirect('batch')
                except Exception as e:
                    print("error is ", e)
        except ObjectDoesNotExist:
            return redirect('merchant_login')
    except KeyError:
        return redirect('merchant_login')

def batch(request):
    try:
        token = request.session['merchanttoken']
        jwtToken = jwt.decode(token, 'merchant_jwt_key')
        try:
            if request.method == 'GET':
                merchant_detail = Merchant.objects.get(email=jwtToken['email'])
                batch_detail = Batch.objects.select_related('product')

                # data = zip(batch_detail, qr_code_detail)
                return render(request, 'merchant/batch.html', {"batch_details": batch_detail})
        except ObjectDoesNotExist:
            return redirect('merchant_login')
    except KeyError:
        return redirect('merchant_login')

def edit_profile(request):
    if request.method == 'POST':
        try:
            token = request.session['merchanttoken']
            jwtToken = jwt.decode(token, 'merchant_jwt_key')
            try:
                merchant_name = request.POST['merchant_name']
                company_name = request.POST['company_name']
                merchant_add_line1 = request.POST['add_line1']
                merchant_add_line2 = request.POST['add_line2']
                merchant_city = request.POST['city']
                merchant_state = request.POST['state']
                merchant_country = request.POST['country']
                merchant_zipcode = request.POST['zipcode']
                merchant_profile_pic = request.FILES.get('merchant_profile_pic')

                merchant = Merchant.objects.get(email=jwtToken['email'])
                try:
                    merchant_add = Address.objects.get(merchant_id=merchant.id)
                    # Insert Merchant Address
                    merchant_add.add_line1 = merchant_add_line1
                    merchant_add.add_line2 = merchant_add_line2
                    merchant_add.city = merchant_city
                    merchant_add.state = merchant_state
                    merchant_add.country = merchant_country
                    merchant_add.zip_code = merchant_zipcode
                    merchant_add.save()
                except ObjectDoesNotExist:
                    merchant_add = Address.objects.create(
                        merchant_id=merchant.id,
                        add_line1=merchant_add_line1,
                        add_line2=merchant_add_line2,
                        city=merchant_city,
                        state=merchant_city,
                        country=merchant_country,
                        zip_code=merchant_zipcode
                    )
                    merchant_add.save()

                # Update Merchant Profile
                merchant.name = merchant_name
                merchant.company = company_name
                merchant.address = merchant_add
                merchant.profile_pic = merchant_profile_pic
                merchant.save()
                return redirect('edit_profile')
            except Exception as e:
                return HttpResponse(e)
        except KeyError:
            return redirect('merchant_login')

    else:
        if request.method == 'GET':
            try:
                token = request.session['merchanttoken']
                jwtToken = jwt.decode(token, 'merchant_jwt_key')
                merchant_detail = Merchant.objects.get(email=jwtToken['email'])
                return render(request, 'merchant/edit-profile.html', {'merchant_detail': merchant_detail})
            except KeyError:
                return redirect('merchant_login')

def products(request):
    try:
        token = request.session['merchanttoken']
        jwtToken = jwt.decode(token, 'merchant_jwt_key')
        try:
            if request.method == 'GET':
                merchant_detail = Merchant.objects.get(email=jwtToken['email'])
                print("merchant id {} mer email {}".format(merchant_detail.id, merchant_detail.email))
                product_list = Product.objects.all().filter(is_deleted=False, merchant_id=merchant_detail.id)
                return render(request, 'merchant/products.html', {'product_list': product_list})
        except Exception as e:
            return HttpResponse(e)
    except KeyError:
        return redirect('merchant_login')


def view_product(request, id):
    try:
        token = request.session['merchanttoken']
        try:
            if request.method == 'GET':
                product_detail = Product.objects.select_related('merchant').get(pk=id)
                return render(request, 'merchant/view-product.html', {'product_detail': product_detail})
        except Exception as e:
            return HttpResponse(e)
    except KeyError:
        return redirect('merchant_login')


def reset_password(request):
    if request.method == 'GET':
        token = request.GET.get('token')
        request.session['token1'] = token
    elif request.method == 'POST':
        sessionToken = request.session['token1']

        if ResetToken.objects.get(token=sessionToken):
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            if password1 == password2:
                resettokenemail = ResetToken.objects.get(token=sessionToken).email
                Merchant.objects.filter(email=resettokenemail).update(password=make_password(password2))
                ResetToken.objects.get(email=resettokenemail).delete()
                return redirect('merchant_login')
            else:
                pass
        else:
            print("not available")
            return render(request, 'merchant/reset-password.html')
    return render(request, 'merchant/reset-password.html')


def change_password(request):
    try:
        token = request.session['merchanttoken']
        jwtToken = jwt.decode(token, 'merchant_jwt_key')
        try:
            if request.method == 'GET':
                return render(request, 'merchant/change-password.html')
            elif request.method == 'POST':
                old_password = request.POST.get('old_password')
                password1 = request.POST.get('password1')
                password2 = request.POST.get('password2')
                obj = Merchant.objects.get(email=jwtToken['email'])
                if Merchant.objects.get(email=jwtToken['email']):
                    if password1 == password2:
                        if check_password(old_password, obj.password):
                            Merchant.objects.filter(email=jwtToken['email']).update(password=make_password(password2))
                            return redirect('dashboard')
                        else:
                            messages.error(request, 'Password Not match with old password')
                            return redirect('chane_password')
                    else:
                        messages.error(request, 'Password Not match with confirm password')
                        return redirect('chane_password')
                else:
                    messages.error(request, 'Invalid Request')
                    return redirect('chane_password')
        except Exception as e:
            return HttpResponse(e)
    except KeyError:
        return redirect('merchant_login')


def forget_password(request):
    if request.method == 'GET':
        token = request.GET.get('token')
        request.session['token1'] = token
    elif request.method == 'POST':
        sessionToken = request.session['token1']
        if ForgetPasswordToken.objects.get(token=sessionToken):
            password1 = request.POST['password1']
            password2 = request.POST['password2']

            if password1 == password2:
                resettokenemail = ForgetPasswordToken.objects.get(token=sessionToken).email
                Merchant.objects.filter(email=resettokenemail).update(password=make_password(password2))
                ForgetPasswordToken.objects.get(email=resettokenemail).delete()
                return redirect('merchant_login')
        else:
            return render(request, 'merchant/reset-password.html')
    return render(request, 'merchant/reset-password.html')

def send_reset_mail(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            if Merchant.objects.filter(email=email).exists():
                import string
                import random
                import urllib.parse
                letters = string.digits + string.ascii_letters
                code = ''.join([random.choice(letters) for i in range(10)])
                params = {'token': code}

                letters = string.digits + string.ascii_letters
                code = ''.join([random.choice(letters) for i in range(10)])
                params = {'token': code}
                try:
                    if ForgetPasswordToken.objects.filter(email=email).exists():
                        return render(request, 'merchant/messages.html',
                                      {'message': 'Reset password email already sent.'})
                    else:
                        token = ForgetPasswordToken(token=code, email=email)
                        token.save()
                except ObjectDoesNotExist:
                    token = ForgetPasswordToken(token=code, email=email)
                    token.save()

                message = 'http://127.0.0.1:8000/merchant/forget_password?' + urllib.parse.urlencode(params)

                subject = "This mail for reset password just Click Below link to reset password Thank you for using our services parasdabhi2021@gmail.com"

                send_mail(subject, message, EMAIL_HOST_USER, [email], fail_silently=False)
                return render(request, 'merchant/messages.html', {'messagesuccess': 'Send mail successfully'})
            else:
                return render(request, 'merchant/messages.html', {'merchantNOtExists': 'Invalid Email'})
        except ObjectDoesNotExist as e:
            return render(request, 'merchant/messages.html', {'message': 'Email dose not exists'})

def download_qr_code(request, id):
    qr_codes_list = []
    batch_detail = Batch.objects.select_related('product')
    for batch in batch_detail:
        qr_code_detail = QrCodes.objects.filter(batch_id=id)

        for qrCode in qr_code_detail:
            qr_codes_list.append(qrCode.qr_code.url)
        zipfilename = "Batch_No_" + batch.batch_name

        zip_subdir = "Batch_No_" + str(id)
        zip_filename = "%s.zip" % zip_subdir
        s = BytesIO()
        zf = zipfile.ZipFile(s, "w")

        for fpath in qr_codes_list:
            fdir, fname = os.path.splitext(fpath)
            zf.write('.' + fdir + fname)
        zf.close()
        resp = HttpResponse(s.getvalue())
        resp['Content-Disposition'] = 'attachment; filename=%s' % zip_filename
        return resp
