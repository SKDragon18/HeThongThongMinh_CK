from django.urls import path
from . import views

urlpatterns = [
    path('logout/', views.logout_view, name='logout'),
    path('home', views.home.as_view(), name='quanly-home'),
    path('account/', views.account.as_view(), name='quanly-account'),
    path('baidang/', views.baidang.as_view(), name='quanly-baidang'),
    path('changepass/', views.changepass.as_view(), name='changepass'),
    path('infor/', views.infor.as_view(), name='infor'),
    path('success/', views.changesuccess.as_view(), name='success'),
    path('thuthap/',views.ThuThapData.as_view(),name='thuthap')
]