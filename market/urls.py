from django.urls import re_path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [

    re_path(r'^$', views.product_list, name='product_list'),
    re_path(r'^login/$', LoginView.as_view(template_name='account/login.html'), name='login'),
    re_path(r'^logout/$', LogoutView.as_view(template_name='account/logged_out.html'), name='logout'),
    re_path(r'^search/$', views.product_search, name='product_search'),
    re_path(r'^register/$', views.register, name='register'),
    re_path(r'^(?P<category_slug>[-\w]+)/$', views.product_list, name='product_list_by_category'),
    re_path(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$', views.product_detail, name='product_detail'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)