import random
import string
import pandas as pd
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.contrib.auth.models import User, Group
from django.core.mail import send_mail, EmailMessage
from .models import Nguoidung, Phanquyen, Baidang, Nha, Chungcu, Hinhanh, DsYeuthich
from random import choice
from string import digits
from .forms import LoginForm, NguoidungForm, FormChangepass
from django.contrib import messages
from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return redirect('homepage')

def random_id(length):
    return ''.join(choice(digits) for i in range(length))

def kiemtra_phanquyen(user):
    # request.user.groups.all()[0]
    if not user.is_authenticated:
        return False
    return user.groups.filter(name='admin').exists()

class home(View):
    def get(self, request):
        user_all = User.objects.filter(is_active=True).count()
        user_ad = User.objects.filter(is_active=True, is_superuser=True).count()
        user_us = User.objects.filter(is_active=True, is_superuser=False).count()
        baidang_all = Baidang.objects.all().count()
        baidang_1 = Baidang.objects.filter(trangthai=1).count()
        return render(request, 'home/home.html', {"user_all": user_all, "user_ad":  user_ad, "user_us":  user_us, "baidang_all": baidang_all, "baidang_1": baidang_1})



class account(View):
    def get(self, request):
        if not kiemtra_phanquyen(request.user):
            return redirect('login')
        status = request.GET.get("status")
        if status == "all":
            nguoidung_list = Nguoidung.objects.all()
        elif status == "active":
            nguoidung_list = Nguoidung.objects.filter(khoa=0)
        elif status == "locked":
            nguoidung_list = Nguoidung.objects.filter(khoa=1)
        else:
            nguoidung_list = Nguoidung.objects.all()
        return render(request, 'account/account.html', {"nguoidung_list": nguoidung_list, "status": status})
    def post(self, request):
        # lấy tên tài khoản của người dùng hiện tại
        if not kiemtra_phanquyen(request.user):
            return redirect('login')
        usname = request.user.username
        tendangnhap = request.POST.get('id')
        nguoidung = Nguoidung.objects.get(tendangnhap=tendangnhap)
        Us = User.objects.get(username=tendangnhap)
        button = request.POST.get('button')
        if button == "status":
            if nguoidung.tendangnhap == usname:
                messages.error(request, "Không thể đổi trạng thái. Bạn đang đang nhập bằng tài khoản này!")
            elif nguoidung.khoa == 1:
                nguoidung.khoa = 0
                Us.is_active = True
                messages.error(request, "Đổi trạng thái thành công! Tài khoản đã được mở khóa")
            elif nguoidung.khoa == 0:
                nguoidung.khoa = 1
                Us.is_active = False
                messages.error(request, "Đổi trạng thái thành công! Tài khoản đã bị khóa")
            nguoidung.save()
            Us.save()
            return redirect('quanly-account')
        elif button == "permissions":
            if Us.is_superuser == False:
                quyen = Phanquyen.objects.get(maquyen="ADMIN")
                nguoidung.phanquyen = quyen
                Us.is_superuser = True
                nguoidung.save()
                Us.save()
                messages.success(request, "Đã cấp quyền admin cho tài khoản " + tendangnhap + " thành công")
                return redirect('quanly-account')
            else:
                messages.success(request, "Tài khoản " + tendangnhap + " đã có quyền admin")
                return redirect('quanly-account')
        elif button == "reset":
            chars = string.ascii_letters + string.digits
            newpass = ''.join(random.choice(chars) for _ in range(10))
            email = EmailMessage("Mật khẩu mới", newpass, from_email=None, to=[nguoidung.email])
            email.send()
            nguoidung.matkhau=newpass
            Us.password=newpass
            nguoidung.save()
            Us.save()
            messages.success(request, "Đã reset mật khẩu cho tài khoản " + tendangnhap + " thành công. Mật khẩu mới đã được gửi về email của người dùng")
            return redirect('quanly-account')

class baidang(View):
    def get(self, request):
        if not kiemtra_phanquyen(request.user):
            return redirect('login')
        status = request.GET.get("status")
        if status == "all":
            baidang_list = Baidang.objects.all()
        elif status == "pending":
            baidang_list = Baidang.objects.filter(trangthai=0)
        elif status == "approved":
            baidang_list = Baidang.objects.filter(trangthai=1)
        else:
            baidang_list = Baidang.objects.all()
        return render(request, 'baidang/baidang_list.html', {"baidang_list": baidang_list, "status": status})
    def post(self, request):
        if not kiemtra_phanquyen(request.user):
            return redirect('login')
        id_baidang = request.POST.get('id')
        baidang = Baidang.objects.get(id_baidang=id_baidang)
        button = request.POST.get('button')
        if button == "status":
            if baidang.trangthai == 1:
                messages.success(request,"Bài đăng đã được duyệt")
                return redirect('quanly-baidang')
            else:
                baidang.trangthai = 1
                baidang.save()
                messages.success(request, "Duyệt bài đăng thành công")
                return redirect('quanly-baidang')
        elif button == "delete":
            Nha.objects.filter(manha=id_baidang).delete()
            Chungcu.objects.filter(machungcu=id_baidang).delete()
            Hinhanh.objects.filter(id_baidang=id_baidang).delete()
            DsYeuthich.objects.filter(id_baidang=id_baidang).delete()
            baidang.delete()
            messages.success(request, "Xóa bài đăng thành công")
            return redirect('quanly-baidang')


class changepass(View):
    def get(self, request):
        form = FormChangepass()
        context = {
            'form': form
        }
        return render(request, 'pass/changepass.html',context)
    def post(self, request):
        # cần lấy người dùng hiện tại đang đăng nhập
        usname = request.user.username
        nguoidung = Nguoidung.objects.get(tendangnhap=usname)
        myUser = User.objects.get(username=usname)
        form = FormChangepass(request.POST)
        if form.is_valid():
            usname = request.user.username
            nguoidung = Nguoidung.objects.get(tendangnhap=usname)
            myUser = User.objects.get(username=usname)

            # Kiểm tra mật khẩu hiện tại
            if form.cleaned_data['password'] != nguoidung.matkhau:
                messages.error(request, "Mật khẩu hiện tại không đúng!")
            # Kiểm tra mật khẩu mới
            elif form.cleaned_data['password1'] != form.cleaned_data['password2']:
                messages.error(request, "Mật khẩu mới không khớp!")
            else:
                nguoidung.matkhau = form.cleaned_data['password1']
                nguoidung.save()
                myUser.set_password(form.cleaned_data['password1'])
                myUser.save()
                return redirect('login')
        else:
            messages.error(request,"Mật khẩu mới không hợp lệ")
        return render(request, 'pass/changepass.html', {'form': form})
        

class changesuccess(View):
    def get(self, request):
        return render(request, 'pass/success.html')
    def post(self, request):
        return redirect('/admin/home')

class infor(View):
    def get(self, request):
        usname = request.user.username
        nguoidung = Nguoidung.objects.get(tendangnhap=usname)
        form = NguoidungForm(instance=nguoidung)
        form.fields['email'].widget.attrs['readonly'] = True
        messages =""
        context = {
            'form': form,
            'messages':messages
        }
        return render(request, 'infor/infor.html', context)

    def post(self, request):
        us = request.user.username
        nguoidung = Nguoidung.objects.get(tendangnhap=us)
        form = NguoidungForm(request.POST, instance=nguoidung)
        if form.is_valid():
            form.save()
            print('lưu thành công')
        else:
            print('lưu thất bại')
        return redirect("infor")

class ThuThapData(View):
    def get(self,request):
        if not kiemtra_phanquyen(request.user):
            return redirect('login')
        return render(request,'data/thuthap.html')
    def post(self,request):
        if not kiemtra_phanquyen(request.user):
            return redirect('login')
        from_date=request.POST.get('from')
        to_date=request.POST.get('to')
        file=request.POST.get('file')
        ds_baidang=Baidang.objects.raw("SELECT * FROM BAIDANG where ngayban>='"+from_date+"' and ngayban <='"+to_date+"'")
        list_sample_nha=[]
        list_sample_chungcu=[]
        columns=['id_baidang','ngayban','quan','huyen','giayto','sopn','dientich','dai','rong','giaban']
        nha=['loaihinh','sotang']
        chungcu=['huong']
        for x in ds_baidang:
            data=[x.id_baidang,x.ngayban,x.quan,x.huyen,x.giayto,x.sopn,x.dientich,x.dai,x.rong,x.giaban]
            
            if x.loai == 'NHA':
                nha_list=[x.nha.loaihinh,x.nha.sotang]
                sample=pd.Series(data+nha_list,columns+nha)
                list_sample_nha.append(sample)
            else:
                chungcu_list=[x.chungcu.huong]
                sample=pd.Series(data+chungcu_list,columns+chungcu)
                list_sample_chungcu.append(sample)
        df=pd.DataFrame(list_sample_nha)
        df.to_csv('data_nha_'+file+'.csv')
        df=pd.DataFrame(list_sample_chungcu)
        df.to_csv('data_chungcu_'+file+'.csv')
        return render(request,'data/thuthap.html',{'message':'Thành công'})


