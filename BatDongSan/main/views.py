from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import Baidang, Phanquyen, Nguoidung, Hinhanh, DsYeuthich, Nha,Chungcu
from django.views import View
from django.db import connection
from .forms import BaiDangForm, NhaForm, ChungCuForm
from .models import UploadedFile, BaidangFilter
from unidecode import unidecode
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .load_model import predict_nha, load_model_nha, predict_chungcu, load_model_chungcu
import datetime

#function

def lay_tendangnhap(request):
    try:
        username=request.user.username
    except Exception as e:
        print(e)
        return None
    return username

def kiemtra_phanquyen(user):
    # request.user.groups.all()[0]
    if not user.is_authenticated:
        return False
    return user.groups.filter(name='user').exists()

def tao_id_baidang():
    try:
        with connection.cursor() as cursor:
            cursor.execute('Select dbo.SinhIdBaiDang()')
            result=cursor.fetchone()[0]
            cursor.close()
    except Exception as e:
        return e
    return result

def tao_id_hinhanh():
    try:
        with connection.cursor() as cursor:
            cursor.execute('Select dbo.SinhIdHinhAnh()')
            result=cursor.fetchone()[0]
            cursor.close()
    except Exception as e:
        return e
    return result

def tao_phan_trang(request,ds):
    paginator = Paginator(ds, 5)
    try:
        page= request.GET.get('page')
        ds=paginator.get_page(page)
    except PageNotAnInteger:
        ds=paginator.get_page(1)
    except EmptyPage:
        ds=paginator.get_page(paginator.num_pages)
    return ds

def ds_baidang_timkiem(user,timkiem=None):
    if timkiem is None:
        return Baidang.objects.raw("SELECT * FROM BAIDANG where tendangnhap='"+user+"' and trangthai = 1")
    else:
        if timkiem.isdigit():
            ds_baidang=Baidang.objects.raw("SELECT * FROM BAIDANG where tendangnhap = %s and trangthai = 1 and (id_baidang = %s "+
                                           "or ngaydang LIKE %s)",[user,timkiem,'%'+timkiem+'%'])
        else: 
            chuoi_chuan_hoa= str.upper(unidecode(timkiem))
            ds_baidang=Baidang.objects.raw("SELECT * FROM BAIDANG where tendangnhap= %s and trangthai = 1 and (tieude LIKE %s or loai LIKE %s)",[user,'%'+timkiem+'%','%'+chuoi_chuan_hoa+'%'])
        return ds_baidang
    
def ds_yeuthich_timkiem(user,timkiem=None):
    if timkiem is None:
        return Baidang.objects.raw("SELECT * FROM BAIDANG where id_baidang in (SELECT id_baidang FROM DS_YEUTHICH where tendangnhap='"+user+"') and trangthai=1")
    else:
        if timkiem.isdigit():
            ds_baidang=Baidang.objects.raw("SELECT * FROM BAIDANG where trangthai=1 and ((id_baidang in (SELECT id_baidang FROM DS_YEUTHICH where id_baidang = %s and tendangnhap= %s ))"
                                           + " or (id_baidang in (SELECT id_baidang FROM DS_YEUTHICH where tendangnhap= %s ) and ngaydang LIKE %s))",[timkiem,user,user,'%'+timkiem+'%'])
        else: 
            chuoi_chuan_hoa= str.upper(unidecode(timkiem))
            ds_baidang=Baidang.objects.raw("SELECT * FROM BAIDANG where id_baidang in (SELECT id_baidang FROM DS_YEUTHICH where tendangnhap= %s ) and trangthai = 1 and (tieude LIKE %s or loai LIKE %s)",[user,'%'+timkiem+'%','%'+chuoi_chuan_hoa+'%'])
        return ds_baidang

# Create your views here.
def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]

# def view_home(request):
#     cursor = connection.cursor()

#     cursor.execute('EXEC dbo.DS_NHA')

#     ds_nha = dictfetchall(cursor)

#     cursor.execute('EXEC dbo.DS_CHUNGCU')

#     ds_chungcu = dictfetchall(cursor)

#     return render(request, 'home1/index.html', {'ds_nha': ds_nha, 'ds_chungcu': ds_chungcu})

# def index(request):
#     return render(request, template_name='main/hompage.html')

def home(request):
    cursor = connection.cursor()

    cursor.execute('EXEC dbo.DS_NHA')

    ds_nha = dictfetchall(cursor)

    cursor.execute('EXEC dbo.DS_CHUNGCU')

    ds_chungcu = dictfetchall(cursor)

    username = request.user.username
    cursor.execute(
        "Select ID_BAIDANG from DS_YEUTHICH where TENDANGNHAP = %s", (username,))
    ds_yeuthich = dictfetchall(cursor)
    yeuthich_ids = [item['ID_BAIDANG'] for item in ds_yeuthich]

    # print(ds_yeuthich)
    # print(yeuthich_ids)
    baidang_list = Baidang.objects.filter(trangthai=1)
    hinhanh_list = {}
    for bd in baidang_list:
        img = Hinhanh.objects.filter(id_baidang = bd).first()
        if img:
            key = bd.id_baidang
            value = img.nguon
            hinhanh_list [key]=value 
    baidang_filter = BaidangFilter(request.GET, queryset=baidang_list)
    filtered_data = baidang_filter.qs
    return render(request, 'user/homepage.html', {'ds_nha': ds_nha, 'ds_chungcu': ds_chungcu, 'ds_yeuthich': yeuthich_ids, 'filter': baidang_filter,'anh_filter':hinhanh_list})

class DangTin(View):

    def get(self,request,loai):
        if not kiemtra_phanquyen(request.user):
            return redirect('login')
        f=BaiDangForm(prefix='f')
        if loai =='Nha':
            fh=NhaForm(prefix='fh')
        else:
            fh=ChungCuForm(prefix='fh')
        
        f.fields['id_baidang'].initial=int(tao_id_baidang())
        f.fields['loai'].initial=str.upper(loai)
        f.fields['chudang'].initial='cá nhân'
        f.fields['id_baidang'].widget.attrs['readonly'] = True
        f.fields['ngaydang'].widget.attrs['readonly'] = True
        return render(request,'user/forms_dang.html',{'f':f, 'fh':fh,'loai':loai})
    
    def post(self,request,loai):
        if not kiemtra_phanquyen(request.user):
            return redirect('login')
        f=BaiDangForm(request.POST,prefix='f')
        if loai =='Nha':
            fh=NhaForm(request.POST,prefix='fh')
        else:
            fh=ChungCuForm(request.POST,prefix='fh')
        
        giaban=request.POST.get('giaban')
        
        if f.is_valid() and fh.is_valid():
            file_list=list(request.FILES.getlist('files'))
            
            if request.POST.get('submit')=='Đề xuất giá':
                if loai =='Nha':
                    print(f.data)
                    try:
                        giayto=f.data['f-giayto']
                        giayto='1'
                    except Exception as e:
                        giayto='0'
                    data=[f.data['f-quan'],f.data['f-huyen'],fh.data['fh-loaihinh'],giayto,
                        fh.data['fh-sotang'],f.data['f-sopn'],f.data['f-dientich'],f.data['f-dai'],f.data['f-rong']]
                    print(data)
                    model=load_model_nha()
                    giaban=predict_nha(model,data)
                else:
                    print(f.data)
                    try:
                        giayto=f.data['f-giayto']
                        giayto='1'
                    except Exception as e:
                        giayto='0'
                    data=[f.data['f-quan'],f.data['f-dientich'],fh.data['fh-huong'], f.data['f-sopn'],giayto]
                    model=load_model_chungcu()
                    giaban=predict_chungcu(model,data)
                return render(request,'user/forms_dang.html',{'f':f, 'fh':fh,'loai':loai,'giaban':giaban})
            
            
            if len(file_list)<3:
                    return render(request,'user/forms_dang.html',{'f':f, 'fh':fh,'loai':loai,'giaban':giaban,'message':'Mời chọn ít nhất 3 hình ảnh'})
            
            baidang = f.save(commit=False)
            user=lay_tendangnhap(request)
            baidang.tendangnhap=Nguoidung.objects.get(pk=user)
            baidang.giaban=giaban
            baidang.trangthai=0
            baidang.save()
            baidangnha = fh.save(commit=False)
            if loai=='Nha':
                baidangnha.manha = baidang
            else:
                baidangnha.machungcu=baidang
            baidangnha.save()
            try:
                
                
                for uploaded_file in file_list:
                    file=UploadedFile.objects.create(file=uploaded_file)
                    hinh_anh=Hinhanh()
                    hinh_anh.id_hinhanh=tao_id_hinhanh()
                    hinh_anh.nguon=file.file.url
                    hinh_anh.id_baidang=baidang
                    hinh_anh.save() 
                    
                return render(request,'user/thanh_cong.html',{'message':'Thành công'})
                
            except Exception as e:
                return HttpResponse(e)
        else:
            print('Bài đăng')
            for error in f.errors:
                print(error)
            print('Nhà')
            for error in fh.errors:
                print(error)
            return render(request,'user/thanh_cong.html',{'message':'Thất bại'})

class DanhSachBaiDang(View):
    
    def get(self, request):
        if not kiemtra_phanquyen(request.user):
            return redirect('login')
        user=lay_tendangnhap(request)
        if user is None:
            return redirect('login')
        if request.GET.get('timkiem'):
            timkiem=request.GET.get('timkiem')
            ds_baidang=ds_baidang_timkiem(user,timkiem)  
        else:
            ds_baidang=Baidang.objects.raw("SELECT * FROM BAIDANG where tendangnhap='"+user+"' and trangthai = 1")
        ds_baidang=tao_phan_trang(request,ds_baidang)
        if request.GET.get('timkiem'):
            return render(request,'user/ds_baidang.html',{'ds':ds_baidang,'timkiem':request.GET.get('timkiem')})
        return render(request,'user/ds_baidang.html',{'ds':ds_baidang})

    def post(self,request):
        if not kiemtra_phanquyen(request.user):
            return redirect('login')
        user=lay_tendangnhap(request)
        if user is None:
            return redirect('login')

        if not request.POST["timkiem"]:
            ds_baidang=ds_baidang_timkiem(user=user)
            ds_baidang=tao_phan_trang(request,ds_baidang)
            return render(request,'user/ds_baidang.html',{'ds':ds_baidang})
        
        timkiem=request.POST["timkiem"]
        ds_baidang=ds_baidang_timkiem(user,timkiem)
        ds_baidang=tao_phan_trang(request,ds_baidang)
        return render(request,'user/ds_baidang.html',{'ds':ds_baidang,'timkiem':timkiem})

class DanhSachYeuThich(View):
    
    def get(self, request):
        if not kiemtra_phanquyen(request.user):
            return redirect('login')
        user=lay_tendangnhap(request)
        if user is None:
            return redirect('login')

        if request.GET.get('timkiem'):
            timkiem=request.GET.get('timkiem')
            ds_baidang=ds_yeuthich_timkiem(user,timkiem)  
        else:
            ds_baidang=ds_yeuthich_timkiem(user,None)  
        ds_baidang=tao_phan_trang(request,ds_baidang)
        
        if request.GET.get('timkiem'):
            return render(request,'user/ds_yeuthich.html',{'ds':ds_baidang,'timkiem':request.GET.get('timkiem')})
        return render(request,'user/ds_yeuthich.html',{'ds':ds_baidang})

    def post(self,request):
        if not kiemtra_phanquyen(request.user):
            return redirect('login')
        user=lay_tendangnhap(request)
        if user is None:
            return redirect('login')
        
        if not request.POST["timkiem"]:
            ds_baidang=ds_yeuthich_timkiem(user,None)
            ds_baidang=tao_phan_trang(request,ds_baidang)
            return render(request,'user/ds_yeuthich.html',{'ds':ds_baidang})
        timkiem=request.POST["timkiem"]
        ds_baidang=ds_yeuthich_timkiem(user,timkiem)
        ds_baidang=tao_phan_trang(request,ds_baidang)
        return render(request,'user/ds_yeuthich.html',{'ds':ds_baidang,'timkiem':timkiem})


def xem_chitiet(request,id_baidang):
    baidang=Baidang.objects.get(pk=id_baidang)
    hinhanh=Hinhanh.objects.filter(id_baidang=baidang.id_baidang)
    if baidang.giayto:
        giayto='1'
    else:
        giayto='0'
    if baidang.loai=='NHA':
        fh=Nha.objects.get(pk=id_baidang)
        data=[baidang.quan,baidang.huyen,fh.loaihinh,giayto,
                        fh.sotang,baidang.sopn,baidang.dientich,baidang.dai,baidang.rong]
        model=load_model_nha()
        gia_dudoan=predict_nha(model,data)
    else:
        fh=Chungcu.objects.get(pk=id_baidang)
        data=[baidang.quan,baidang.dientich,fh.huong, baidang.sopn,giayto]
        model=load_model_chungcu()
        gia_dudoan=predict_chungcu(model,data)
    diachi='đường '+ baidang.diachi + ' phường '+baidang.huyen + ' quận ' +baidang.quan + ' tỉnh '+ baidang.tinh
    if gia_dudoan <0:
            gia_dudoan='Không có đủ cơ sở để ước lượng'
    return render (request,'user/chitiet.html',{'baidang':baidang,'fh':fh,'diachi':diachi,'hinhanh':hinhanh,'gia_dudoan':gia_dudoan})

class GoBaiDang(View):
    def get(self,request,id_baidang):
        if not kiemtra_phanquyen(request.user):
            return redirect('login')
        baidang=Baidang.objects.get(pk=id_baidang)
        return render(request,'user/go_baidang.html',{'baidang':baidang})
    
    def post(self,request,id_baidang):
        if not kiemtra_phanquyen(request.user):
            return redirect('login')
        baidang=Baidang.objects.get(pk=id_baidang)
        ghinhan=request.POST["ghinhan"]
        if ghinhan=='daban':
            baidang.trangthai=2
            baidang.ngayban=datetime.datetime.now()
        elif ghinhan =='khong':
            baidang.trangthai=3
        else:
            return render(request,'user/go_baidang.html',{'baidang':baidang,'message':'Vui lòng nhập chính xác mã xác nhận daban/khong'})
        baidang.save()
        return render(request,'user/go_baidang.html',{'message':'Thành công'})



def unfollow(request,id_baidang):
    if not kiemtra_phanquyen(request.user):
            return redirect('login')
    user=lay_tendangnhap(request)
    if user is None:
        return redirect('login')
    try:
        yeuthich=DsYeuthich.objects.filter(tendangnhap=user, id_baidang=id_baidang)
        yeuthich.delete()
        ds_baidang=Baidang.objects.raw("SELECT * FROM BAIDANG where id_baidang in (SELECT id_baidang FROM DS_YEUTHICH where tendangnhap='"+user+"') and trangthai=1")
        return render(request,'user/ds_yeuthich.html',{'ds':ds_baidang,'message':'unfollow thành công'})
    except Exception as e:
        ds_baidang=Baidang.objects.raw("SELECT * FROM BAIDANG where id_baidang in (SELECT id_baidang FROM DS_YEUTHICH where tendangnhap='"+user+"') and trangthai=1")
        return render(request,'user/ds_yeuthich.html',{'ds':ds_baidang,'message':e})
    

class DanhSachDuyet(View):
    
    def get(self, request):
        ds_baidang=Baidang.objects.raw("SELECT * FROM BAIDANG where trangthai = 0")
        return render(request,'user/ds_duyet.html',{'ds':ds_baidang})

    def post(self,request):
        user=lay_tendangnhap(request)
        if not request.POST["timkiem"]:
            
            ds_baidang=Baidang.objects.raw("SELECT * FROM BAIDANG where tendangnhap='"+user+"' and trangthai = 1")
            return render(request,'user/ds_baidang.html',{'ds':ds_baidang})
        timkiem=request.POST["timkiem"]
        if timkiem.isdigit():
            ds_baidang=Baidang.objects.raw("SELECT * FROM BAIDANG where tendangnhap = %s and trangthai = 1 and (id_baidang = %s "+
                                           "or ngaydang LIKE %s)",[user,timkiem,'%'+timkiem+'%'])
        else: 
            chuoi_chuan_hoa= str.upper(unidecode(timkiem))
            ds_baidang=Baidang.objects.raw("SELECT * FROM BAIDANG where tendangnhap= %s and trangthai = 1 and (tieude LIKE %s or loai LIKE %s)",[user,'%'+timkiem+'%','%'+chuoi_chuan_hoa+'%'])
        
        return render(request,'user/ds_baidang.html',{'ds':ds_baidang,'timkiem':timkiem})

class DuyetBaiDang(View):
    def get(self,request,id_baidang):
        f=Baidang.objects.get(pk=id_baidang)
        if f.loai=='NHA':
            fh=Nha.objects.get(pk=id_baidang)
        else:
            fh=Chungcu.objects.get(pk=id_baidang)
        if not f or not fh:
            return HttpResponse('Lỗi')
        
        return render(request,'user/duyet_baidang.html',{'f':f,'fh':fh})
    def post(self,request,id_baidang):
        f=Baidang.objects.get(pk=id_baidang)
        if f.loai=='NHA':
            fh=Nha.objects.get(pk=id_baidang)
        else:
            fh=Chungcu.objects.get(pk=id_baidang)
        if not f or not fh:
            return HttpResponse('Lỗi')
        try:
            button=request.POST['btn']
            if button=='Cho phép':
                f.trangthai=1
                f.save()
                return render(request,'main/thong_bao_duyet.html',{'message':'Đã cho phép đăng bài'})
            elif button=='Từ chối':
                for item in f.hinhanh_set.all():
                    item.delete()
                    print(item)
                fh.delete()
                f.delete()
                return render(request,'user/thong_bao_duyet.html',{'message':'Đã từ chối và xóa bài đăng'})
        except Exception as e:
            return render(request,'user/duyet_baidang.html',{'f':f,'fh':fh,'message':'Thao tác thất bại'})

# def yeuthich(request):
#     id = request.POST.get('post-id')
#     baidang = Baidang.objects.get(id_baidang=id)
#     bd_yeuthich = DsYeuthich()
#     tendangnhap = request.user.username
#     nguoidung = Nguoidung.objects.get(tendangnhap=tendangnhap)
#     bd_yeuthich.tendangnhap = nguoidung
#     bd_yeuthich.id_baidang = baidang
#     try:
#         bd_yeuthich.save()
#     except:
#         pass
#     return JsonResponse(None,safe=False)

def yeuthich(request):
        id = request.POST.get('post-id')
        baidang = Baidang.objects.get(id_baidang=id)
        tendangnhap = request.user.username
        nguoidung = Nguoidung.objects.get(tendangnhap=tendangnhap)

        bd_yeuthich, created = DsYeuthich.objects.get_or_create(
            tendangnhap=nguoidung,
            id_baidang=baidang
        )
        if created:
            return JsonResponse({'update': 'success'})
        else:
            bd_yeuthich.delete()
            return JsonResponse({'update': 'fail'})
