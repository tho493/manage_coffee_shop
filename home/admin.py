from django.contrib import admin
from .models import *

class PostHangHoa(admin.ModelAdmin):
    list_display = ['ma_hang_hoa', 'ten_hang_hoa', 'nhom_hang_hoa', 'gia']
    list_filter = ['nhom_hang_hoa','gia']
    search_fields = ['ten_hang_hoa','nhom_hang_hoa']

class PostDonBanHang(admin.ModelAdmin):
    list_display = ['ma_don_hang', 'nguoi_order', 'ngay_ban', 'tong_tien', 'khach_hang', 'display_hang_hoa', 'created','updated','note','cancelled','confirmed']
    list_per_page = 20
    list_filter = ['nguoi_order','ngay_ban']
    search_fields = ['ma_don_hang','khach_hang']

    def display_hang_hoa(self, obj):
        return ", ".join([hang_hoa.ten_hang_hoa for hang_hoa in obj.hang_hoa.all()])

    display_hang_hoa.short_description = 'Hang Hoa'

class PostOrder(admin.ModelAdmin):
    list_display = ['DonBanHang','hang_hoa','so_luong']

class PostKhachHang(admin.ModelAdmin):
    list_display = ['ma_khach_hang', 'ten_khach_hang', 'dia_chi', 'so_dien_thoai', 'email', 'created', 'updated', 'note', 'cancelled']
    list_search_fields = ['ma_khach_hang','ten_khach_hang']
    list_filter = ['ma_khach_hang','ten_khach_hang']

# admin.site.register(Admin, PostAdmin)
admin.site.register(HangHoa, PostHangHoa)
admin.site.register(DonBanHang, PostDonBanHang)
admin.site.register(Order, PostOrder)
admin.site.register(KhachHang, PostKhachHang)


