from django.urls import path
from . import views


urlpatterns = [
    path('', views.index),
    path('home/', views.index),
    path('order/', views.order),
    path('order/<str:ma_don_hang>/', views.order, name='order'),
    path('quan_ly_san_pham/', views.quan_ly_san_pham),
    path('them_san_pham/', views.them_san_pham),
    path('quan_ly_khach_hang/', views.quan_ly_khach_hang),
    path('them_khach_hang/', views.them_khach_hang),
    path('xem_don_hang/<slug:page_number>', views.danh_sach_don_da_thanh_toan, name='page_number'),
    path('chi_tiet_don_hang/<slug:ma_don_hang>', views.chi_tiet_don_hang, name='chi_tiet_don_hang'),
]
