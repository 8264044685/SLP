from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
                  path('login', views.merchant_login, name='merchant_login'),
                  path('dashboard', views.dashboard_page, name='dashboard'),
                  path('add_batch', views.add_batch, name='add_batch'),
                  path('batch', views.batch, name='batch'),
                  path('edit_profile', views.edit_profile, name='edit_profile'),
                  path('products', views.products, name='products_merchant'),
                  path('view_product/<int:id>', views.view_product, name='view_product'),
                  path('reset_password', views.reset_password, name='reset_password'),
                  path('change_password', views.change_password, name='change_password'),
                  path('send_mail', views.send_reset_mail, name='send_mail'),
                  path('forget_password', views.forget_password, name='forget_password'),
                  path('download_qr_code/<int:id>', views.download_qr_code, name='download_qr_code'),
                  path('logout', views.logout, name='logout'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
