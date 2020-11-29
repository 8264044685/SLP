from django.conf import settings
from django.urls import path
from django.urls import re_path

from slp_admin import views
from user_auth import *
from .quiz import *
from .show_user import *
from .views import *

# from .quiz import *

urlpatterns = [
    path('', login_admin, name='admin_login'),
    path('logout/', logout_admin, name='admin_logout'),
    path('dashboard/', dashboard, name='slpdashboard'),
    path('change_password/', change_password),
    path('users/', list_user, name='slp_list_user'),
    path('view_user/<str:id>/', view_user),
    path('profile/', user_profile),
    path('forget_password/', forget_password),
    path('reset_password/<str:id>/', reset_password),
    path('view_user/block/<str:id>/', block_user, name='block_user'),
    path('purchased_gifts', purchased_gift_page),
    # path('quiz/' , quiz),
    # path('quiz/add_question/' , add_question),
    path('qr-codes/', views.qr_codes, name='qr_codes'),
    path('dispute/requests/', views.dispute_requests, name='qr_codes'),
    path('contractors/', views.contractor_list, name='list_contractor'),
    path('contractor/<int:contraId>/', views.contractor_dtl, name='contractor_detail'),
    path('points-request/', views.points_request, name='point_request'),
    path('videos/add/', views.add_video, name='add-video'),
    re_path(r'videos/(?P<video_id>\d+)/edit/', views.edit_video, name='edit-video'),
    re_path(r'videos/(?P<video_id>\d+)/delete/', views.delete_video, name='delete-video'),
    path('videos/', views.videos, name='videos'),
    path('category/', views.category, name='category'),
    re_path(r'category/(?P<category_id>\d+)/delete/', views.delete_category, name='delete-category'),
    path('quiz/', quiz, name='quiz'),
    path('quiz/add_question/', add_question),
    path('quiz/<int:quiz_id>/edit/', edit_quiz, name='edit-quiz'),
    path('quiz/<str:quiz_id>/delete/', delete_quiz),
    path('quiz/<str:quiz_id>/view/', view_quiz),
    path('merchant/<int:id>', views.merchant, name='merchant'),
    path('add_merchant', views.add_merchant, name='add_merchant'),
    path('view_merchant', views.view_merchant, name='view_merchant'),
    path('delete_merchant/<int:id>', views.delete_merchant, name='delete_merchant'),
    path('merchant_status', views.merchant_status, name='merchant_status'),
    path('add_products', views.add_products, name='add_products'),
    path('products', views.products, name='products'),
    path('view_product/<int:id>', views.view_slp_product, name='slp_admin_view_product'),
    path('delete_product/<int:id>', views.delete_product, name='delete_product'),
    path('edit_product/<int:id>', views.edit_product, name='edit_product'),
    path('edit_product_tech_file', views.edit_product_tech_file, name='edit_product_tech_file'),
    path('edit_product_guide_file', views.edit_product_guide_file, name='edit_product_guide_file'),
    path('edit_product_video_file', views.edit_product_video_file, name='edit_product_video_file'),
    path('edit_product_safety_file', views.edit_product_safety_file, name='edit_product_safety_file'),
    path('edit_product_certificate_file', views.edit_product_certificate_file, name='edit_product_certificate_file'),

]

if settings.DEBUG:
    from django.conf.urls.static import static

    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
