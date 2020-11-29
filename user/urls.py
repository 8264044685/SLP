from django.contrib import admin
from django.urls import path
from .apis import category_list, video_list, quiz_list,question_list
from user_auth import *
from .views import *
from upc.apis import TechSupportQuestions
from .apis import Giftbit
from django.urls import include
from rest_framework.routers import DefaultRouter
from . import apis

router = DefaultRouter()
router.register('scan', apis.ScannedQRCodeApi, basename='qr_code-list')
router.register('dispute', apis.RaiseDispute)
router.register('product-activation', apis.ProductActivationApi)

router1 = DefaultRouter()
router1.register('', apis.RewardHistory, basename='reward_history-list')

router2 = DefaultRouter()
router2.register('users', apis.SplitPointsApi, basename='users-list')

router3 = DefaultRouter()
router3.register('', apis.DontSplitApi)

urlpatterns = [
    path('qr/', include(router.urls)),
    path('rewards/', include(router1.urls)),
    path('split/', include(router2.urls)),
    path('dont-split/', include(router3.urls)),
    path('register/', register_user),
    path('login/', login_user),
    path('logout/', logout_user),
    path('change_password/', change_password_user),
    path('forget_password/', forget_password),
    path('reset_password/<str:ids>/', reset_password),
    path('upc-questions/', TechSupportQuestions.as_view()),
    path('giftbit/', Giftbit.as_view()),
    path('categorylist/',category_list),
    path('videolist/',video_list),
    path('quizlist/',quiz_list),
    path('questionlist/',question_list),
]