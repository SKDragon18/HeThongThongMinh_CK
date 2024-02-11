import pickle
import pandas as pd
import os

model_dir_nha=os.path.abspath('main\\model\\nha')
model_dir_cc=os.path.abspath('main\\model\\chungcu')

quan={'Huyện Thạch Thất': 0.0385, 'Thị xã Sơn Tây': 0.077, 'Huyện Thanh Oai': 0.1155, 'Huyện Phúc Thọ': 0.154, 'Huyện Hoài Đức': 0.1925, 'Huyện Thanh Trì': 0.231, 'Huyện Đông Anh': 0.2695, 'Huyện Mê Linh': 0.308, 'Huyện Sóc Sơn': 0.3465, 'Huyện Thường Tín': 0.385, 'Quận Hà Đông': 0.4235, 'Quận Hoàng Mai': 0.462, 'Quận Bắc Từ Liêm': 0.5005, 'Quận Long Biên': 0.539, 'Quận Hai Bà Trưng': 0.5775, 'Huyện Đan Phượng': 0.616, 'Quận Nam Từ Liêm': 0.6545, 'Quận Thanh Xuân': 0.693, 'Huyện Chương Mỹ': 0.7315, 'Huyện Quốc Oai': 0.77, 'Quận Đống Đa': 0.8085, 'Huyện Gia Lâm': 0.847, 'Quận Ba Đình': 0.8855, 'Quận Tây Hồ': 0.924, 'Quận Cầu Giấy': 0.9625, 'Quận Hoàn Kiếm': 1.001}
huyen={'Xã Dương Quang': 0.0042, 'Xã Đại Yên': 0.0084, 'Xã Cổ Đông': 0.0126, 'Xã Đại áng': 0.0168, 'Xã Sơn Đồng': 0.021, 'Phường Phú Thịnh': 0.0252, 'Xã Sơn Đông': 0.0294, 'Xã Phú Cường': 0.0336, 'Xã Hương Ngải': 0.0378, 'Xã Tiên Dược': 0.042, 'Xã Bích Hòa': 0.0462, 'Xã Phú Cát': 0.0504, 'Xã Văn Bình': 0.0546, 'Xã Đặng Xá': 0.0588, 'Xã Kim Hoa': 0.063, 'Phường Đồng Mai': 0.0672, 'Xã Đông La': 0.0714, 'Xã Nhị Khê': 0.0756, 'Xã Đức Thượng': 0.0798, 'Xã Ngũ Hiệp': 0.084, 'Phường Thượng Cát': 0.0882, 'Xã Di Trạch': 0.0924, 'Xã La Phù': 0.0966, 'Xã Thượng Mỗ': 0.1008, 'Xã Cự Khê': 0.105, 'Xã Đông Dư': 0.1092, 'Xã Liên Ninh': 0.1134, 'Xã Võng Xuyên': 0.1176, 'Phường Yên Nghĩa': 0.1218, 'Phường Phú Lương': 0.126, 'Xã An Khánh': 0.1302, 'Phường Phú Lãm': 0.1344, 'Xã An Thượng': 0.1386, 'Xã Đa Tốn': 0.1428, 'Phường Ngô Quyền': 0.147, 'Xã Vĩnh Quỳnh': 0.1512, 'Xã Dương Liễu': 0.1554, 'Xã Hải Bối': 0.1596, 'Xã Tả Thanh Oai': 0.1638, 'Xã Vân Canh': 0.168, 'Xã Đông Mỹ': 0.1722, 'Phường Biên Giang': 0.1764, 'Xã Bắc Hồng': 0.1806, 'Phường Dương Nội': 0.1848, 'Xã Tứ Hiệp': 0.189, 'Xã Hữu Hoà': 0.1932, 'Xã Kim Chung': 0.1974, 'Phường Phúc Lợi': 0.2016, 'Xã Tiền Phong': 0.2058, 'Xã Ngọc Hồi': 0.21, 'Phường Tây Mỗ': 0.2142, 'Phường Vĩnh Hưng': 0.2184, 'Thị trấn Đông Anh': 0.2226, 'Phường Chương Dương': 0.2268, 'Phường Lĩnh Nam': 0.231, 'Thị trấn Trạm Trôi': 0.2352, 'Xã Tam Hiệp': 0.2394, 'Xã Võng La': 0.2436, 'Phường Thụy Phương': 0.2478, 'Xã Nghĩa Hương': 0.252, 'Phường Thanh Trì': 0.2562, 'Phường Trần Phú': 0.2604, 'Phường Phương Canh': 0.2646, 'Phường Yên Sở': 0.2688, 'Phường Cự Khối': 0.273, 'Phường Kiến Hưng': 0.2772, 'Phường Khâm Thiên': 0.2814, 'Xã Kim Sơn': 0.2856, 'Phường Trung Phụng': 0.2898, 'Xã Lê Lợi': 0.294, 'Phường Vạn Phúc': 0.2982, 'Xã Tân Triều': 0.3024, 'Phường Xuân Phương': 0.3066, 'Xã Nam Hồng': 0.3108, 'Phường Mai Động': 0.315, 'Xã Duyên Thái': 0.3192, 'Xã Mai Lâm': 0.3234, 'Thị trấn Văn Điển': 0.3276, 'Phường Hà Cầu': 0.3318, 'Xã Vân Côn': 0.336, 'Phường Giang Biên': 0.3402, 'Phường Tân Mai': 0.3444, 'Phường Hàng Bông': 0.3486, 'Phường Thanh Xuân Nam': 0.3528, 'Phường Hoàng Liệt': 0.357, 'Phường Thượng Thanh': 0.3612, 'Phường Thạch Bàn': 0.3654, 'Thị trấn Phùng': 0.3696, 'Phường Quốc Tử Giám': 0.3738, 'Phường La Khê': 0.378, 'Phường Quỳnh Mai': 0.3822, 'Phường Định Công': 0.3864, 'Phường Đại Kim': 0.3906, 'Phường Thịnh Liệt': 0.3948, 'Phường Cổ Nhuế 2': 0.399, 'Phường Phú Đô': 0.4032, 'Phường Lê Đại Hành': 0.4074, 'Xã Thanh Liệt': 0.4116, 'Xã Kiêu Kỵ': 0.4158, 'Phường Ngọc Thụy': 0.42, 'Phường Sài Đồng': 0.4242, 'Phường Tương Mai': 0.4284, 'Phường Hoàng Văn Thụ': 0.4326, 'Phường Đức Thắng': 0.4368, 'Phường Đại Mỗ': 0.441, 'Phường Kim Giang': 0.4452, 'Phường Long Biên': 0.4494, 'Phường Bạch Mai': 0.4536, 'Phường Xuân Đỉnh': 0.4578, 'Phường Trương Định': 0.462, 'Phường Đông Ngạc': 0.4662, 'Phường Yên Phụ': 0.4704, 'Phường Thổ Quan': 0.4746, 'Phường Bùi Thị Xuân': 0.4788, 'Phường Phúc Diễn': 0.483, 'Phường Giáp Bát': 0.4872, 'Phường Minh Khai': 0.4914, 'Phường Nam Đồng': 0.4956, 'Xã Phù Đổng': 0.4998, 'Phường Văn Miếu': 0.504, 'Phường Hàng Bột': 0.5082, 'Phường Khương Đình': 0.5124, 'Phường Thanh Nhàn': 0.5166, 'Phường Yết Kiêu': 0.5208, 'Phường Văn Quán': 0.525, 'Phường Phương Liên': 0.5292, 'Phường Đồng Tâm': 0.5334, 'Phường Thượng Đình': 0.5376, 'Phường Cầu Dền': 0.5418, 'Phường Cổ Nhuế 1': 0.546, 'Phường Văn Chương': 0.5502, 'Phường Đống Mác': 0.5544, 'Xã Cổ Bi': 0.5586, 'Phường Phố Huế': 0.5628, 'Phường Khương Thượng': 0.567, 'Phường Thanh Lương': 0.5712, 'Phường Quang Trung': 0.5754, 'Phường Ngọc Lâm': 0.5796, 'Phường Phú Diễn': 0.5838, 'Phường Nhân Chính': 0.588, 'Phường Mộ Lao': 0.5922, 'Phường Trung Tự': 0.5964, 'Phường Nguyễn Trãi': 0.6006, 'Phường Vĩnh Tuy': 0.6048, 'Phường Phú La': 0.609, 'Xã Phù Linh': 0.6132, 'Phường Phúc La': 0.6174, 'Phường Mễ Trì': 0.6216, 'Phường Hạ Đình': 0.6258, 'Phường Kim Liên': 0.63, 'Phường Trung Văn': 0.6342, 'Phường Quỳnh Lôi': 0.6384, 'Phường Khương Trung': 0.6426, 'Phường Phúc Tân': 0.6468, 'Phường Mỹ Đình 1': 0.651, 'Phường Phạm Đình Hổ': 0.6552, 'Phường Thanh Xuân Trung': 0.6594, 'Phường Cát Linh': 0.6636, 'Phường Bách Khoa': 0.6678, 'Phường Bồ Đề': 0.672, 'Phường Việt Hưng': 0.6762, 'Xã Tân Lập': 0.6804, 'Phường Mỹ Đình 2': 0.6846, 'Phường Giảng Võ': 0.6888, 'Phường Thanh Xuân Bắc': 0.693, 'Phường Phúc Đồng': 0.6972, 'Thị trấn Chúc Sơn': 0.7014, 'Thị trấn Quang Minh': 0.7056, 'Phường Ô Chợ Dừa': 0.7098, 'Phường Phúc Xá': 0.714, 'Phường Cống Vị': 0.7182, 'Phường Đức Giang': 0.7224, 'Phường Ngô Thì Nhậm': 0.7266, 'Phường Bạch Đằng': 0.7308, 'Phường Ngọc Hà': 0.735, 'Phường Cầu Diễn': 0.7392, 'Phường Thành Công': 0.7434, 'Phường Phương Liệt': 0.7476, 'Phường Đội Cấn': 0.7518, 'Phường Phương Mai': 0.756, 'Phường Gia Thụy': 0.7602, 'Phường Ngã Tư Sở': 0.7644, 'Phường Thụy Khuê': 0.7686, 'Phường Tứ Liên': 0.7728, 'Phường Kim Mã': 0.777, 'Phường Láng Thượng': 0.7812, 'Phường Thịnh Quang': 0.7854, 'Phường Khương Mai': 0.7896, 'Phường Vĩnh Phúc': 0.7938, 'Phường Nhật Tân': 0.798, 'Phường Tây Tựu': 0.8022, 'Phường Trung Liệt': 0.8064, 'Phường Quan Hoa': 0.8106, 'Thị trấn Trâu Quỳ': 0.8148, 'Phường Láng Hạ': 0.819, 'Phường Yên Hoà': 0.8232, 'Phường Bưởi': 0.8274, 'Phường Đồng Nhân': 0.8316, 'Xã Khánh Hà': 0.8358, 'Phường Phú Thượng': 0.84, 'Phường Xuân Tảo': 0.8442, 'Phường Đồng Xuân': 0.8484, 'Phường Ngọc Khánh': 0.8526, 'Phường Dịch Vọng': 0.8568, 'Phường Xuân La': 0.861, 'Phường Nghĩa Đô': 0.8652, 'Thị trấn Sóc Sơn': 0.8694, 'Phường Nguyễn Du': 0.8736, 'Thị trấn Quốc Oai': 0.8778, 'Phường Quán Thánh': 0.882, 'Phường Mai Dịch': 0.8862, 'Thị trấn Yên Viên': 0.8904, 'Phường Điện Biên': 0.8946, 'Phường Dịch Vọng Hậu': 0.8988, 'Phường Liễu Giai': 0.903, 'Phường Nghĩa Tân': 0.9072, 'Phường Quảng An': 0.9114, 'Phường Trung Hoà': 0.9156, 'Xã Đình Xuyên': 0.9198, 'Xã Sài Sơn': 0.924, 'Phường Cửa Nam': 0.9282, 'Xã Hoàng Văn Thụ': 0.9324, 'Phường Nguyễn Trung Trực': 0.9366, 'Phường Trúc Bạch': 0.9408, 'Phường Cửa Đông': 0.945, 'Xã Yên Thường': 0.9492, 'Phường Hàng Bài': 0.9534, 'Phường Tràng Tiền': 0.9576, 'Phường Hàng Bồ': 0.9618, 'Phường Phan Chu Trinh': 0.966, 'Phường Hàng Đào': 0.9702, 'Phường Hàng Mã': 0.9744, 'Phường Hàng Gai': 0.9786, 'Phường Hàng Buồm': 0.9828, 'Phường Trần Hưng Đạo': 0.987, 'Phường Hàng Trống': 0.9912, 'Phường Lý Thái Tổ': 0.9954}
giayto={'Giấy tờ khác': 0.25, 'Đang chờ sổ': 0.5, 'Không rõ': 0.75, 'Đã có sổ': 1.0}
loaihinh={'Nhà ngõ, hẻm': 0.25, 'Nhà mặt phố, mặt tiền': 0.5, 'Nhà phố liền kề': 0.75, 'Nhà biệt thự': 1.0}

quan_chungcu={'Huyện Bình Chánh': 0.0455, 'Quận 12': 0.091, 'Quận Thủ Đức': 0.1365, 'Quận 9': 0.182, 'Quận Bình Tân': 0.2275, 'Quận 8': 0.273, 'Quận Tân Bình': 0.3185, 'Quận Gò Vấp': 0.364, 'Huyện Nhà Bè': 0.4095, 'Quận 6': 0.455, 'Huyện Hóc Môn': 0.5005, 'Quận Tân Phú': 0.546, 'Quận 7': 0.5915, 'Quận 11': 0.637, 'Quận 3': 0.6825, 'Quận 5': 0.728, 'Quận 2': 0.7735, 'Quận Bình Thạnh': 0.819, 'Quận 4': 0.8645, 'Quận 10': 0.91, 'Quận Phú Nhuận': 0.9555, 'Quận 1': 1.001}
huong_chungcu={'Tây': 0.1111, 'Bắc': 0.2222, 'Đông Nam': 0.3333, 'Nam': 0.4444, 'Tây Bắc': 0.5555, 'Không': 0.6666, 'Đông': 0.7777, 'Tây Nam': 0.8888, 'Đông Bắc': 0.9999}
giayto_chungcu={'Giấy tờ khác': 0.25, 'Không rõ': 0.5, 'Đã có sổ': 0.75, 'Đang chờ sổ': 1.0}

mean_quan=0
for key in quan.keys():
    mean_quan+=quan[key]
mean_quan=mean_quan/len(quan)

mean_huyen=0
for key in huyen.keys():
    mean_huyen+=huyen[key]
mean_huyen=mean_huyen/len(huyen)

mean_loaihinh=0
for key in loaihinh.keys():
    mean_loaihinh+=loaihinh[key]
mean_loaihinh=mean_loaihinh/len(loaihinh)

mean_quan_chungcu=0
for key in quan_chungcu.keys():
    mean_quan_chungcu+=quan_chungcu[key]
mean_quan_chungcu=mean_quan_chungcu/len(quan_chungcu)

mean_huong_chungcu=0
for key in huong_chungcu.keys():
    mean_huong_chungcu+=huong_chungcu[key]
mean_huong_chungcu=mean_huong_chungcu/len(huong_chungcu)

def load_model_nha():
    for file in os.listdir(model_dir_nha):
        if '.pkl' in file:
            print(model_dir_nha)
            try:
                model=pickle.load(open(model_dir_nha+'\\'+file,'rb'))
            except Exception as e:
                print(e)
                return None
            return model
    return None
def load_model_chungcu():
    for file in os.listdir(model_dir_cc):
        if '.pkl' in file:
            print(model_dir_cc)
            try:
                model=pickle.load(open(model_dir_cc+'\\'+file,'rb'))
            except Exception as e:
                print(e)
                return None
            return model
    return None

def predict_nha(model,data):
    features=['Quận','Huyện', 'Loại hình nhà ở', 'Giấy tờ pháp lý',
              'Số tầng','Số phòng ngủ','Diện tích','Dài','Rộng']
    if data[3]=='1':
        data[3]='Đã có sổ'
    else:
        data[3]='Không rõ'
    data[0]=(quan[data[0]] if data[0] in quan.keys() else mean_quan)
    data[1]=(huyen[data[1]] if data[1] in huyen.keys() else mean_huyen)
    data[2]=(loaihinh[data[2]] if data[2] in loaihinh.keys() else mean_loaihinh)
    data[3]=(giayto[data[3]])
    x=pd.Series(data,features)
    x=pd.DataFrame([x])
    pred=model.predict(x)
    result=round(pred[0][0],3)
    if result<=0:
        return 1
    return result

def predict_chungcu(model,data):
    features=['QUẬN HUYỆN','DIỆN TÍCH - M2', 'HƯỚNG', 'SỐ PHÒNG', 'GIẤY TỜ PHÁP LÝ']
    if data[4]=='1':
        data[4]='Đã có sổ'
    else:
        data[4]='Không rõ'
    data[0]=(quan_chungcu[data[0]] if data[0] in quan_chungcu.keys() else mean_quan_chungcu)
    data[2]=(huong_chungcu[data[2]] if data[2] in huong_chungcu.keys() else mean_huong_chungcu)
    data[4]=(giayto_chungcu[data[4]])
    x=pd.Series(data,features)
    x=pd.DataFrame([x])
    pred=model.predict(x)
    result=round(pred[0],3)
    if result <=0:
        return 1
    return result
if __name__=='__main__':
    model=load_model_nha()
    if model is None:
        print('Lỗi')
    else:
        print(model)
    data=['Huyện Thạch Thất','Xã Dương Quang', 'Nhà ngõ, hẻm', '1',
              '5','5','25','5','5']
    pred=predict_nha(model,data)
    print(pred)