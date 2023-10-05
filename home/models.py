from django.db import models
from datetime import datetime
from django.conf import settings
    
class HangHoa(models.Model):
    ma_hang_hoa = models.CharField(max_length=50, primary_key=True)
    ten_hang_hoa = models.CharField(max_length=100)
    nhom_hang_hoa = models.CharField(max_length=100)
    image = models.ImageField('Label', default=None)
    gia = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        if not self.ma_hang_hoa:
            max_ma_hang_hoa = HangHoa.objects.all().order_by('ma_hang_hoa').last()
            if max_ma_hang_hoa is not None:
                self.ma_hang_hoa = '{0:03d}'.format(int(max_ma_hang_hoa.ma_hang_hoa) + 1)
            else:
                self.ma_hang_hoa = '001'
        super().save(*args, **kwargs)


class KhachHang(models.Model):
    ma_khach_hang = models.CharField(max_length=50, primary_key=True)
    ten_khach_hang = models.CharField(max_length=100)
    dia_chi = models.CharField(max_length=100)
    so_dien_thoai = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    note = models.TextField(null=True, blank=True)
    cancelled = models.BooleanField(default=False)

class DonBanHang(models.Model):
    ma_don_hang = models.CharField(max_length=50, primary_key=True)
    nguoi_order = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='orders', on_delete=models.CASCADE)
    ngay_ban = models.DateTimeField(default=datetime.now)
    tong_tien = models.DecimalField(max_digits=10, decimal_places=2)
    khach_hang = models.ForeignKey(KhachHang, related_name='KhachHang', on_delete=models.CASCADE)
    hang_hoa = models.ManyToManyField(HangHoa, through='Order')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    note = models.TextField(null=True, blank=True)
    cancelled = models.BooleanField(default=False)
    confirmed = models.BooleanField(default=False)

    def get_str_hang_hoa(self):
        return ", ".join([obj.ten_hang_hoa for obj in self.hang_hoa.all()])

    def get_total_price(self):
        return sum(Order.get_cost() for Order in self.DonBanHang.all())
    

# def create_id_order():
#     last_order = Order.objects.all().order_by('ma_order').last()
#     if not last_order:
#         return '001'
#     order_ma_order = last_order.ma_order
#     new_order_ma_order = int(order_ma_order)
#     new_order_ma_order += 1
#     return '{0:03d}'.format(new_order_ma_order)
class Order(models.Model):
    DonBanHang = models.ForeignKey(DonBanHang, related_name='DonBanHang', on_delete=models.CASCADE)
    hang_hoa = models.ForeignKey(HangHoa, on_delete=models.CASCADE)
    so_luong = models.IntegerField()
    
    def get_cost(self):
        return self.hang_hoa.gia * self.so_luong
    
