from .serializers import *
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from .models import Category
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
import requests
import string
import random
from slp_admin.models import *
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from slp_admin import models
from . import serializers


@api_view(['get'])
@csrf_exempt
@permission_classes([AllowAny, ])
def category_list(request):
    category = Category.objects.all()
    serializer = CategorySerializer(category, many=True)
    return Response({
        "status_code": 200,
        "status": "success",
        "message": "category list",
        "data": serializer.data
    }, status=status.HTTP_200_OK)


@api_view(['get'])
@csrf_exempt
@permission_classes([AllowAny])
def video_list(request):
    category = Category.objects.get(pk=request.data['categoryid'])

    video = Video.objects.filter(category=category)
    serializer = VideoSerializer(video, many=True)
    return Response({
        "status_code": 200,
        "status": "success",
        "message": "video list",
        "data": serializer.data
    }, status=status.HTTP_200_OK)


@api_view(['get'])
@csrf_exempt
@permission_classes([AllowAny])
def quiz_list(requset):
    video = Video.objects.get(pk=requset.data['videoid'])
    print("video ---------------------->", video)
    quiz = Quiz.objects.filter(video=video)
    print("quiz-------------------->", quiz)
    serializer = QuizSerializer(quiz, many=True)
    return Response({
        "status_code": 200,
        "status": "success",
        "message": "quiz list",
        "data": serializer.data
    }, status=status.HTTP_200_OK)


@api_view(['get'])
@csrf_exempt
@permission_classes([AllowAny])
def question_list(request):
    quiz = Quiz.objects.get(pk=request.data['quizid'])
    question = Question.objects.filter(quiz=quiz)
    serializer = QuestionSerializer(question, many=True)
    return Response({
        "status_code": 200,
        "status": "success",
        "message": "question list",
        "data": serializer.data
    }, status=status.HTTP_200_OK)



class Giftbit(APIView):
    """ List of gift cards  """

    def get(self, request):
        try:
            verify_token = request.headers.get('Usertoken')
            print(verify_token)
        except Exception as e:
            print(e)
            return Response("Session Expired")
        try:
            user = UserToken.objects.get(token = verify_token)
            print(user)
        except Exception as e:
            print(e)
            return Response("invalid token or user not found")

        r = requests.get('https://api-testbed.giftbit.com/papi/v1/brands/', headers={
            'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJTSEEyNTYifQ==.Ujh3VkcrY0MvU3BzSmN1UktKekl0elh0aW4xV3BGZGYxUXdTOC84K1VueWtHWHllaHRWeDVYRms5akthRXltVzJYMDBPZldLeDJacWdQTVpMcXUySW9ZRSt6bm04QnVVa0dFczNRbEJXd0dIdGxrOUU2VWprNWJldVVZYjNzc1M=.IMHfmFHvaYsvn3DJSj+hEuVOvwTXibdFTChgDP63/zA=',
            'Content-Type': 'application/json'})
        data = r.json()
        list_of_brands = data["brands"]

        status_header = {
            'status': status.HTTP_201_CREATED,
            'message': "questions received successfully",
            'data': list_of_brands
        }
        return Response(status_header)

    def post(self, request):
        try:
            verify_token = request.headers.get('Usertoken')
        except Exception as e:
            print(e)
            return Response("Session Expired")
        x = request.data['brand_code']
        list_of_brands = [x]

        res = ''.join(random.choices(string.ascii_uppercase + string.digits, k=7))
        usd = int(request.data['USD'])
        user_token = UserToken.objects.get(token = verify_token)
        user = SlpUser.objects.get(id=user_token.user.id)
        user_points = user.available_points
        settings_object = SlpAdminSetings.objects.get(id = 1)
        print("user points" , user_points)
        if user_points > usd * settings_object.conversion_points and user_points > settings_object.eligibility_points:
            if user_points - usd * settings_object.conversion_points >= 1000:
                user_points = user_points - usd * settings_object.conversion_points
                user.available_points = user_points
                user.save()
                values = """{
                    "message":"The gift message!",
                    "subject":"Please enjoy this gift!",
                    "contacts": [{
                        "firstname": """+user.first_name+""",
                        "lastname":  """+user.last_name+""",
                        "email":  """+user.email+"""
                      }],
                    "price_in_cents": """+request.data['USD']+"00"+""",
                    "brand_codes": """+str(list_of_brands)+""",
                    "expiry": "2020-11-09",
                    "id": """+res+"""
                  }"""

                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJTSEEyNTYifQ==.Ujh3VkcrY0MvU3BzSmN1UktKekl0elh0aW4xV3BGZGYxUXdTOC84K1VueWtHWHllaHRWeDVYRms5akthRXltVzJYMDBPZldLeDJacWdQTVpMcXUySW9ZRSt6bm04QnVVa0dFczNRbEJXd0dIdGxrOUU2VWprNWJldVVZYjNzc1M=.IMHfmFHvaYsvn3DJSj+hEuVOvwTXibdFTChgDP63/zA='
                }
                prequest = requests.post('https://api-testbed.giftbit.com/papi/v1/campaign', data=values, headers=headers)
                PurchasedGifts.objects.create(user = user, brand_code = x, coupon_amount = usd)

                status_header = {
                    'status': status.HTTP_201_CREATED,
                    'message': "Congratulations! Gift card is purchased.E-mail is sent to your email id.",
                    'data': [user_points,prequest.json()]
                }
                return Response(status_header)
            else:
                status_header = {
                    'status': status.HTTP_201_CREATED,
                    'message': "1000 points must be kept in the account."
                }
                return Response(status_header)
        else:
            status_header = {
                'status': status.HTTP_201_CREATED,
                'message': "You have not enough points."
            }
            return Response(status_header)


class ScannedQRCodeApi(mixins.CreateModelMixin, mixins.ListModelMixin, GenericViewSet):
    """API ViewSet for QR Scan and QR Scanned Listing"""
    serializer_class = serializers.QRCodeSerializer

    def get_queryset(self):
        verify_token = self.request.headers.get('UserToken')
        user_token = models.UserToken.objects.get(token=verify_token)
        user = models.ScannedQRCode.objects.filter(user=user_token.user)
        return user

    def create(self, request, *args, **kwargs):
        """Create Scanned QR code in receive of QR Code"""
        if models.ScannedQRCode.objects.filter(QR_code_id=self.request.data['QR_code']).count() != 0:
            status_header = {
                "status_code": status.HTTP_400_BAD_REQUEST,
                "status": "bad request",
                "message": "QR Code already scanned before."
            }
            return Response(status_header)
        else:
            verify_token = self.request.headers.get('UserToken')
            user_token = models.UserToken.objects.get(token=verify_token)
            user = models.SlpUser.objects.get(id=user_token.user.id)
            qr = models.QRCode.objects.get(id=self.request.data['QR_code'])
            product = models.Product.objects.get(id=self.request.data['product'])
            data = {
                "user": user.id,
                "QR_code": qr.id,
                "product": product.id
            }
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            status_header = {
                "status_code": 200,
                "status": "success",
                "message": "QR Code Scanned.",
                "data": serializer.data
            }
            return Response(status_header)

    def list(self, request, *args, **kwargs):
        """List scanned QR Codes to user"""
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        status_header = {
            "status_code": 200,
            "status": "success",
            "message": "Scanned QR Codes.",
            "data": serializer.data
        }
        return Response(status_header)


class RewardHistory(mixins.ListModelMixin, GenericViewSet):
    """Api for Rewards History (transactions)"""
    serializer_class = serializers.RewardHistorySerializer

    def get_queryset(self):
        verify_token = self.request.headers.get('UserToken')
        user_token = models.UserToken.objects.get(token=verify_token)
        user = models.PointsTransaction.objects.filter(user=user_token.user)
        return user

    def list(self, request, *args, **kwargs):
        """List Reward History to user"""
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        status_header = {
            "status_code": 200,
            "status": "success",
            "message": "Reward History",
            "data": serializer.data
        }
        return Response(status_header)


class RaiseDispute(mixins.CreateModelMixin, GenericViewSet):
    """Api to raise dispute from user"""
    serializer_class = serializers.DisputeRaiseSerializer
    queryset = models.Dispute.objects.all()

    def create(self, request, *args, **kwargs):
        qr = models.QRCode.objects.get(id=self.request.data['QR_code'])
        verify_token = self.request.headers.get('UserToken')
        user_token = models.UserToken.objects.get(token=verify_token)
        user = models.SlpUser.objects.get(id=user_token.user.id)
        data = {
            "user": user.id,
            "QR_code": qr.id,
            "message": request.data["message"]
        }
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user, QR_code=qr)
        status_header = {
            "status_code": status.HTTP_200_OK,
            "status": "success",
            "message": "Dispute Successfully Raised.",
        }
        return Response(status_header)


class ProductActivationApi(mixins.CreateModelMixin, GenericViewSet, mixins.UpdateModelMixin):
    """Api for product activation detail"""
    serializer_class = serializers.ProductActivationSerializer
    queryset = models.Product.objects.all()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = models.Product.objects.get(id=self.kwargs.get('pk'))
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        status_header = {
            "status_code": status.HTTP_200_OK,
            "status": "success",
            "message": "Product Activation Successful.",
        }
        return Response(status_header)

    # def create(self, request, *args, **kwargs):
    #     product = models.Product.objects.get(id=self.request.data['product_id'])
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     status_header = {
    #         "status_code": status.HTTP_200_OK,
    #         "status": "success",
    #         "message": "Product Activation Successful.",
    #     }
    #     return Response(status_header)


class SplitPointsApi(mixins.ListModelMixin, mixins.CreateModelMixin, GenericViewSet):
    """Api to get list of users in same company and to receive split of points"""
    serializer_class = serializers.GetUserSerializer

    def get_queryset(self):
        verify_token = self.request.headers.get('UserToken')
        user_token = models.UserToken.objects.get(token=verify_token)
        user = models.SlpUser.objects.filter(company=user_token.user.company)
        return user

    def list(self, request, *args, **kwargs):
        """Method to return list of users with same company as that of logged in user"""
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        status_header = {
            "status_code": status.HTTP_200_OK,
            "status": "success",
            "message": "Users List With Same Company as User Received.",
            "data": serializer.data
        }
        return Response(status_header)

    @staticmethod
    def transaction(user_id, points, split):
        """Method to make transactions"""
        user = models.SlpUser.objects.get(id=user_id)
        data = {
            "user": user.id,
            "point": points,
            "transaction_type": "credit",
            "type": "Spray Points",
            "splitted": split
        }
        serializer = serializers.TransactionSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

    def create(self, request, *args, **kwargs):
        """Method to split points to provided users with their respective percents"""
        users = request.data['user']
        user_list = users.split(",")
        percents = request.data['percent']
        percent_list = percents.split(",")

        user_list = [int(i) for i in user_list]
        percent_list = [int(i) for i in percent_list]

        user_percent = 100 - sum(percent_list)

        scanned_qr_code = models.ScannedQRCode.objects.get(id=request.data['scanned_qr'])
        points = scanned_qr_code.product.productrewardpoint_set.first().qr_code_scan

        verify_token = self.request.headers.get('UserToken')
        user_token = models.UserToken.objects.get(token=verify_token)

        user = models.SlpUser.objects.get(id=user_token.user.id)
        user_points = (user_percent*points)/100

        # create a transaction for user who is splitting points
        SplitPointsApi.transaction(user.id, user_points, True)

        # create transactions for users who is split in points
        for user_id, percent in zip(user_list, percent_list):
            user_split_points = (percent*points)/100
            SplitPointsApi.transaction(user_id, user_split_points, True)

        status_header = {
            "status_code": status.HTTP_200_OK,
            "status": "success",
            "message": "Successfully Split Points to Users.",
        }
        return Response(status_header)


class DontSplitApi(mixins.CreateModelMixin, GenericViewSet):
    """Api to create transaction to user for dont split option."""
    queryset = models.PointsTransaction.objects.all()

    def create(self, request, *args, **kwargs):
        verify_token = self.request.headers.get('UserToken')
        user_token = models.UserToken.objects.get(token=verify_token)
        scanned_qr_code = models.ScannedQRCode.objects.get(id=request.data['scanned_qr'])
        points = scanned_qr_code.product.productrewardpoint_set.first().qr_code_scan
        user = models.SlpUser.objects.get(id=user_token.user.id)
        SplitPointsApi.transaction(user.id, points, True)
        status_header = {
            "status_code": status.HTTP_200_OK,
            "status": "success",
            "message": "Successfully Rewarded Points to User.",
        }
        return Response(status_header)
