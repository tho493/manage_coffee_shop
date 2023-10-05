from django.shortcuts import render, redirect
from .admin import *
from django.db.models import Q
from django.core.paginator import Paginator


def create_new_order(request):
        user = request.user
        khach_hang = KhachHang.objects.all().last()

        last_order = DonBanHang.objects.all().order_by('ma_don_hang').last()
        if not last_order:
                id_order = '001'
        else:
                order_ma_don_hang = last_order.ma_don_hang
                new_order_ma_don_hang = int(order_ma_don_hang)
                new_order_ma_don_hang += 1
                id_order = '{0:03d}'.format(new_order_ma_don_hang)

        don_hang, created = DonBanHang.objects.get_or_create(
        ma_don_hang= id_order,
        defaults={
                'nguoi_order': user,
                'tong_tien': 0.0,
                'khach_hang': khach_hang,
        },
        )

        if not created:
                return -1
        return don_hang.ma_don_hang

# Create your views here.
def index(request):
        if not request.user.is_authenticated:
                return redirect('/login/')
        if(request.method == 'POST' and request.POST.get('create_order') != None):
                return redirect('/order/')
        
        danh_sach_don_hang = DonBanHang.objects.filter(cancelled=False, confirmed=False)
        tong_so_don = len([obj.ma_don_hang for obj in danh_sach_don_hang])
        tong_doanh_thu = sum(obj.tong_tien for obj in DonBanHang.objects.filter(Q(confirmed=True)))
        doanh_thu_thang = sum(obj.tong_tien for obj in DonBanHang.objects.filter(Q(confirmed=True)) if obj.created.month == datetime.now().month)
        data = {"danh_sach_don_hang": danh_sach_don_hang, "tong_so_don": tong_so_don, 'tong_doanh_thu':tong_doanh_thu, 'doanh_thu_thang':doanh_thu_thang}
        return render(request, 'index.html', data)

def error(request):
        return render(request, '404.html')

def order(request, ma_don_hang=None):
        if not request.user.is_authenticated:
                return redirect('/login/')
        
        id_order = (request.POST.get('id_order') or ma_don_hang) or create_new_order(request)
        don_ban_hang = DonBanHang.objects.get(ma_don_hang=id_order)
        all_order = don_ban_hang.DonBanHang.all()

        if(request.method == 'POST'):
                for key in request.POST:
                        if key.startswith('btn_order'):
                                ma_hang_hoa = key[len('btn_order'):]
                                hang_hoa = HangHoa.objects.get(ma_hang_hoa=ma_hang_hoa)
                                so_luong = request.POST.get('so_luong') or 1
                                don_ban_hang.tong_tien += hang_hoa.gia
                                don_ban_hang.save()
                                new_order = Order(DonBanHang=don_ban_hang, hang_hoa=hang_hoa, so_luong=so_luong)
                                new_order.save()
                        if key.startswith('update_so_luong'):
                                ma_hang_hoa = key[len('update_so_luong'):]
                                hang_hoa = HangHoa.objects.get(ma_hang_hoa=ma_hang_hoa)
                                hang_order = don_ban_hang.DonBanHang.get(hang_hoa=hang_hoa)
                                so_luong = request.POST.get('so_luong' + str(ma_hang_hoa))
                                hang_order.so_luong = so_luong
                                hang_order.save()
                                don_ban_hang.tong_tien = don_ban_hang.get_total_price()
                                don_ban_hang.save()
                        if(key.startswith('delete_item')):
                                ma_hang_hoa = key[len('delete_item'):]
                                hang_hoa = HangHoa.objects.get(ma_hang_hoa=ma_hang_hoa)
                                don_ban_hang.tong_tien -= hang_hoa.gia
                                don_ban_hang.save()
                                san_pham = Order.objects.filter(DonBanHang=don_ban_hang, hang_hoa=hang_hoa)
                                san_pham.delete()
                        if(key.startswith('delete_all_item')):
                                san_pham = Order.objects.filter(DonBanHang=don_ban_hang)
                                don_ban_hang.tong_tien = 0
                                don_ban_hang.save()
                                san_pham.delete()
                        if(key.startswith('cancel_order')):
                                don_ban_hang.cancelled = True
                                don_ban_hang.save()
                                return redirect('/home/')
                        if(key.startswith('thanh_toan')):
                                don_ban_hang.confirmed = True
                                don_ban_hang.save()
                                return redirect('/home/')
        
        danh_sach_san_pham = HangHoa.objects.filter(Q(ten_hang_hoa__icontains=request.POST.get('search_product')) | Q(nhom_hang_hoa__icontains=request.POST.get('search_product'))) if (request.method == 'POST' and request.POST.get('btn_search') != None) else HangHoa.objects.all()
        nhom_san_pham = HangHoa.objects.values('nhom_hang_hoa').distinct()
        data =  {"danh_sach_san_pham": danh_sach_san_pham, "id_order": id_order, "order": all_order, "don_ban_hang": don_ban_hang, "nhom_san_pham": nhom_san_pham}
        return render(request, 'order/main.html',data )


def danh_sach_don_da_thanh_toan(request, page_number = None):
        if not request.user.is_authenticated:
                return redirect('/login/')
        
        danh_sach_don_hang = DonBanHang.objects.filter(confirmed=True)
        paginator_list = Paginator(danh_sach_don_hang, 10)
        page_numbers = range(1, paginator_list.num_pages + 1)
        page_obj = paginator_list.get_page(page_number)

        arr = []
        for don_hang in page_obj:
                arr.append({don_hang.ma_don_hang: don_hang.get_str_hang_hoa()})

        data =  {"page_obj": page_obj, 'page_numbers': page_numbers, 'arr': arr}
        return render(request, 'order/don_hang_da_thanh_toan.html', data)

def chi_tiet_don_hang(request, ma_don_hang=None):
        if not request.user.is_authenticated:
                return redirect('/login/')
        
        # data =  {"don_ban_hang": don_ban_hang, "array_don_hang": array_don_hang}
        return render(request, 'order/chi_tiet_don_hang.html')

def quan_ly_khach_hang(request):
        if not request.user.is_authenticated:
                return redirect('/login/')
        KhachHangs = KhachHang.objects.all()
        data =  {"KhachHangs": KhachHangs}
        if(request.method == 'POST'):
                if(request.POST.get('delete_khach_hang') != None): 
                        khach = KhachHang.objects.get(ma_khach_hang=request.POST.get('ma_khach_hang'))
                        khach.delete()
                elif(request.POST.get('edit_khach_hang') != None):
                        khach = KhachHang.objects.get(ma_khach_hang=request.POST.get('ma_khach_hang'))
                        return render(request, 'khach_hang/sua_khach_hang.html', {'khach': khach})
                elif(request.POST.get('luu_thong_tin_khach_hang') != None):
                        khach = KhachHang.objects.get(ma_khach_hang=request.POST.get('ma_khach_hang'))
                        khach.ten_khach_hang = request.POST.get('ten_khach_hang')
                        khach.dia_chi = request.POST.get('dia_chi')
                        khach.so_dien_thoai = request.POST.get('so_dien_thoai')
                        khach.email = request.POST.get('email')
                        khach.note = request.POST.get('note')
                        khach.save()
        return render(request, 'khach_hang/danh_sach_khach_hang.html', data)

def them_khach_hang(request):
        if not request.user.is_authenticated:
                return redirect('/login/')                
        if(request.method == 'POST' and request.POST.get('ma_khach_hang') != None):
                khach, created = KhachHang.objects.get_or_create(
                        ma_khach_hang=request.POST.get('ma_khach_hang')
                        ,
                defaults={
                        'ma_khach_hang': request.POST.get('ma_khach_hang'),
                        'ten_khach_hang': request.POST.get('ten_khach_hang'),
                        'dia_chi': request.POST.get('dia_chi'),
                        'so_dien_thoai': request.POST.get('so_dien_thoai'),
                        'email': request.POST.get('email'),
                        'note': request.POST.get('note'),
                },
                )
                if not created:
                        khach.ma_khach_hang = request.POST.get('ma_khach_hang')
                        khach.ten_khach_hang = request.POST.get('ten_khach_hang')
                        khach.dia_chi = request.POST.get('dia_chi')
                        khach.so_dien_thoai = request.POST.get('so_dien_thoai')
                        khach.email = request.POST.get('email')
                        khach.note = request.POST.get('note')
                        khach.save()
                return redirect('/quan_ly_khach_hang/')
        return render(request, 'khach_hang/them_khach_hang.html')


def quan_ly_san_pham(request):
        if not request.user.is_authenticated:
                return redirect('/login/')
        HangHoas = HangHoa.objects.all()
        data =  {"HangHoas": HangHoas}
        if(request.method == 'POST'):
                if(request.POST.get('delete_hang_hoa') != None): 
                        hang = HangHoa.objects.get(ma_hang_hoa=request.POST.get('ma_hang_hoa'))
                        hang.delete()
                elif(request.POST.get('edit_hang_hoa') != None):
                        hang = HangHoa.objects.get(ma_hang_hoa=request.POST.get('ma_hang_hoa'))
                        return render(request, 'quan_ly_hang_hoa/sua_san_pham.html', {'hang': hang})
                elif(request.POST.get('luu_thong_tin_san_pham') != None):
                        hang = HangHoa.objects.get(ma_hang_hoa=request.POST.get('ma_hang_hoa'))
                        hang.ten_hang_hoa = request.POST.get('ten_hang_hoa')
                        hang.nhom_hang_hoa = request.POST.get('nhom_hang_hoa')
                        hang.gia = request.POST.get('gia')
                        hang.save()
                        # return render(request, 'quan_ly_hang_hoa/quan_ly_san_pham.html', data)
        # elif (request.method == 'GET'):
        return render(request, 'quan_ly_hang_hoa/quan_ly_san_pham.html', data)

def them_san_pham(request):
        if not request.user.is_authenticated:
                return redirect('/login/')
        if(request.method == 'POST'):
                new_hang_hoa = HangHoa( ten_hang_hoa= request.POST.get('ten_hang_hoa'), nhom_hang_hoa= request.POST.get('nhom_hang_hoa'), gia=request.POST.get('gia'), image=request.FILES.get('image'))
                new_hang_hoa.save()
                return redirect('/quan_ly_san_pham/')
        return render(request, 'quan_ly_hang_hoa/them_san_pham.html', {})