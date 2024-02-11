# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
import django_filters
from django import forms
from django.utils import timezone


class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)


class Baidang(models.Model):
    id_baidang = models.BigIntegerField(db_column='ID_BAIDANG', primary_key=True)  # Field name made lowercase.
    tieude = models.CharField(db_column='TIEUDE', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    loai = models.CharField(db_column='LOAI', max_length=7, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    diachi = models.CharField(db_column='DIACHI', max_length=30, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    huyen = models.CharField(db_column='HUYEN', max_length=30, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    quan = models.CharField(db_column='QUAN', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    tinh = models.CharField(db_column='TINH', max_length=30, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    giayto = models.BooleanField(db_column='GIAYTO')  # Field name made lowercase.
    sopn = models.IntegerField(db_column='SOPN')  # Field name made lowercase.
    tinhtrang = models.CharField(db_column='TINHTRANG', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    dientich = models.FloatField(db_column='DIENTICH')  # Field name made lowercase.
    dai = models.FloatField(db_column='DAI')  # Field name made lowercase.
    rong = models.FloatField(db_column='RONG')  # Field name made lowercase.
    giaban = models.DecimalField(db_column='GIABAN', max_digits=19, decimal_places=4)  # Field name made lowercase.
    chitiet = models.TextField(db_column='CHITIET', db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    trangthai = models.IntegerField(db_column='TRANGTHAI')  # Field name made lowercase.
    chudang = models.CharField(db_column='CHUDANG', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    ngaydang = models.DateField(db_column='NGAYDANG', default=timezone.now())  # Field name made lowercase.
    ngayban = models.DateField(db_column='NGAYBAN', blank=True, null=True)  # Field name made lowercase.
    tendangnhap = models.ForeignKey('Nguoidung', models.DO_NOTHING, db_column='TENDANGNHAP')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BAIDANG'


class Chungcu(models.Model):
    machungcu = models.OneToOneField(Baidang, models.DO_NOTHING, db_column='MACHUNGCU', primary_key=True)  # Field name made lowercase.
    lo = models.CharField(db_column='LO', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    macan = models.CharField(db_column='MACAN', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    sotang = models.IntegerField(db_column='SOTANG', blank=True, null=True)  # Field name made lowercase.
    huong = models.CharField(db_column='HUONG', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'CHUNGCU'


class DsYeuthich(models.Model):
    tendangnhap = models.OneToOneField('Nguoidung', models.DO_NOTHING, db_column='TENDANGNHAP', primary_key=True)  # Field name made lowercase. The composite primary key (TENDANGNHAP, ID_BAIDANG) found, that is not supported. The first column is selected.
    id_baidang = models.ForeignKey(Baidang, models.DO_NOTHING, db_column='ID_BAIDANG')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DS_YEUTHICH'
        unique_together = (('tendangnhap', 'id_baidang'),)


class Hinhanh(models.Model):
    id_hinhanh = models.BigIntegerField(db_column='ID_HINHANH', primary_key=True)  # Field name made lowercase.
    nguon = models.CharField(db_column='NGUON', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    id_baidang = models.ForeignKey(Baidang, models.DO_NOTHING, db_column='ID_BAIDANG', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'HINHANH'


class Nguoidung(models.Model):
    tendangnhap = models.CharField(db_column='TENDANGNHAP', primary_key=True, max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    matkhau = models.CharField(db_column='MATKHAU', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    phanquyen = models.ForeignKey('Phanquyen', models.DO_NOTHING, db_column='PHANQUYEN')  # Field name made lowercase.
    khoa = models.BooleanField(db_column='KHOA')  # Field name made lowercase.
    ho = models.CharField(db_column='HO', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    ten = models.CharField(db_column='TEN', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    gioitinh = models.CharField(db_column='GIOITINH', max_length=3, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    ngaysinh = models.DateField(db_column='NGAYSINH', blank=True, null=True)  # Field name made lowercase.
    sdt = models.CharField(db_column='SDT', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(db_column='EMAIL', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'NGUOIDUNG'


class Nha(models.Model):
    manha = models.OneToOneField(Baidang, models.DO_NOTHING, db_column='MANHA', primary_key=True)  # Field name made lowercase.
    loaihinh = models.CharField(db_column='LOAIHINH', max_length=30, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    sotang = models.IntegerField(db_column='SOTANG')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'NHA'


class Phanquyen(models.Model):
    maquyen = models.CharField(db_column='MAQUYEN', primary_key=True, max_length=5, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    tenquyen = models.CharField(db_column='TENQUYEN', unique=True, max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PHANQUYEN'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS')

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS')
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128, db_collation='SQL_Latin1_General_CP1_CI_AS')
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS')
    first_name = models.CharField(max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS')
    last_name = models.CharField(max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS')
    email = models.CharField(max_length=254, db_collation='SQL_Latin1_General_CP1_CI_AS')
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    object_repr = models.CharField(max_length=200, db_collation='SQL_Latin1_General_CP1_CI_AS')
    action_flag = models.SmallIntegerField()
    change_message = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS')
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')
    model = models.CharField(max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS')
    name = models.CharField(max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS')
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40, db_collation='SQL_Latin1_General_CP1_CI_AS')
    session_data = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS')
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class MainUploadedfile(models.Model):
    id = models.BigAutoField(primary_key=True)
    file = models.CharField(max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')
    uploaded_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'main_uploadedfile'


class Sysdiagrams(models.Model):
    name = models.CharField(max_length=128, db_collation='SQL_Latin1_General_CP1_CI_AS')
    principal_id = models.IntegerField()
    diagram_id = models.AutoField(primary_key=True)
    version = models.IntegerField(blank=True, null=True)
    definition = models.BinaryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sysdiagrams'
        unique_together = (('principal_id', 'name'),)

# class BaidangFilter(django_filters.FilterSet):
    
#     tinh = django_filters.ChoiceFilter(
#         choices=[('Biên Hòa','Biên Hòa'),('Đồng Nai','Đồng Nai')],
#         label='tinh'
#     )
#     sopn = django_filters.NumberFilter()
    

#     class Meta:
#         model = Baidang
#         fields = ['tinh','sopn']

class BaidangFilter(django_filters.FilterSet):
    TINH_CHOICES = (
        ('',''),
        ('an-giang', 'An Giang'),
        ('ba-ria-vung-tau', 'Bà Rịa - Vũng Tàu'),
        ('bac-giang', 'Bắc Giang'),
        ('bac-kan', 'Bắc Kạn'),
        ('bac-lieu', 'Bạc Liêu'),
        ('bac-ninh', 'Bắc Ninh'),
        ('ben-tre', 'Bến Tre'),
        ('binh-dinh', 'Bình Định'),
        ('binh-duong', 'Bình Dương'),
        ('binh-phuoc', 'Bình Phước'),
        ('binh-thuan', 'Bình Thuận'),
        ('ca-mau', 'Cà Mau'),
        ('cao-bang', 'Cao Bằng'),
        ('dak-lak', 'Đắk Lắk'),
        ('dak-nong', 'Đắk Nông'),
        ('dien-bien', 'Điện Biên'),
        ('dong-nai', 'Đồng Nai'),
        ('dong-thap', 'Đồng Tháp'),
        ('gia-lai', 'Gia Lai'),
        ('ha-giang', 'Hà Giang'),
        ('ha-nam', 'Hà Nam'),
        ('Hà Nội', 'Hà Nội'),
        ('ha-tinh', 'Hà Tĩnh'),
        ('hai-duong', 'Hải Dương'),
        ('hai-phong', 'Hải Phòng'),
        ('hoa-binh', 'Hòa Bình'),
        ('Hồ Chí Minh', 'Hồ Chí Minh'),
        ('hau-giang', 'Hậu Giang'),
        ('hung-yen', 'Hưng Yên'),
        ('khanh-hoa', 'Khánh Hòa'),
        ('kien-giang', 'Kiên Giang'),
        ('kon-tum', 'Kon Tum'),
        ('lai-chau', 'Lai Châu'),
        ('lao-cai', 'Lào Cai'),
        ('lang-son', 'Lạng Sơn'),
        ('lam-dong', 'Lâm Đồng'),
        ('long-an', 'Long An'),
        ('nam-dinh', 'Nam Định'),
        ('nghe-an', 'Nghệ An'),
        ('ninh-binh', 'Ninh Bình'),
        ('ninh-thuan', 'Ninh Thuận'),
        ('phu-tho', 'Phú Thọ'),
        ('phu-yen', 'Phú Yên'),
        ('quang-binh', 'Quảng Bình'),
        ('quang-nam', 'Quảng Nam'),
        ('quang-ngai', 'Quảng Ngãi'),
        ('quang-ninh', 'Quảng Ninh'),
        ('quang-tri', 'Quảng Trị'),
        ('soc-trang', 'Sóc Trăng'),
        ('son-la', 'Sơn La'),
        ('tay-ninh', 'Tây Ninh'),
        ('thai-binh', 'Thái Bình'),
        ('thai-nguyen', 'Thái Nguyên'),
        ('thanh-hoa', 'Thanh Hóa'),
        ('thua-thien-hue', 'Thừa Thiên Huế'),
        ('tien-giang', 'Tiền Giang'),
        ('tra-vinh', 'Trà Vinh'),
        ('tuyen-quang', 'Tuyên Quang'),
        ('vinh-long', 'Vĩnh Long'),
        ('vinh-phuc', 'Vĩnh Phúc'),
        ('yen-bai', 'Yên Bái'),
    )
    
    LOAI_CHOICES = (
        ('',''),
        ('NHA', 'Nhà'),
        ('CHUNGCU', 'Chung cư'),
        # Thêm các tùy chọn khác tại đây
    )
    CHUDANG_CHOICES=(
        ('',''),
        ('Cá nhân','Cá nhân'),
        ('Môi giới','Môi giới'),
    )

    loai = django_filters.CharFilter(
        widget=forms.Select(choices=LOAI_CHOICES),
        field_name='loai',
        label='Loại'
    )
    
    tinh = django_filters.CharFilter(
        field_name='tinh',
        label='Tỉnh',
        lookup_expr='exact',
        widget=forms.Select(choices=TINH_CHOICES)
    )
    
    giayto = django_filters.ChoiceFilter(
        field_name='giayto',
        label='Có giấy tờ',
        choices=(
            (True, 'Có giấy tờ'),
            (False, 'Không có giấy tờ'),
        )
    )
    
    dientich__gt = django_filters.NumberFilter(
        field_name='dientich',
        lookup_expr='gt',
        label='Diện tích lớn hơn'
    )
    
    giaban__lt = django_filters.NumberFilter(
        field_name='giaban',
        lookup_expr='lt',
        label='Giá bán nhỏ hơn'
    )
    
    
    chudang = django_filters.CharFilter(
        field_name='chudang',
        label='Chủ đăng',
        widget=forms.Select(choices=CHUDANG_CHOICES),

    )
    class Meta:
        model = Baidang
        fields = {
            'loai': ['exact'],
            'tinh': ['exact'],
            'giayto': ['exact'],
            'dientich': ['gt'],
            'giaban': [ 'lt'],
            'chudang': ['exact'],
        }