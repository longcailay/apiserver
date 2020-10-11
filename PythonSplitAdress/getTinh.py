a = '59, Đặng Thúc Vịnh, Xã Đông Thạnh, H. Hóc Môn, Tp. Hồ Chí Minh'
b = 'Ấp Thạnh Thới, Xã Đồng Sơn, H. Gò Công Tây, T. Tiền Giang'
c = 'Ấp Tân Hưng, Xã Đồi 61, H. Trảng Bom, T. Đồng Nai'
d = 'Nhà văn hóa Lao Động, 168, Trần Thanh Mại, Q. Bình Tân, Tp. Hồ Chí Minh'
e = '93, Trần Thị Nghĩ, P. 7, Q. Gò Vấp, Tp. Hồ Chí Minh'
f = '808, Đường 30/4, P. 11, Thành phố Vũng Tàu, T. Bà Rịa - Vũng Tàu'
#Từ địa chỉ đầy đủ, cho ra tỉnh hoặc thành phố tương ứng
# VÍ dụ: input: 808, Đường 30/4, P. 11, Thành phố Vũng Tàu, T. Bà Rịa - Vũng Tàu
# output: Bà Rịa - Vũng Tàu
def getProvince(address):
    temp = address.split(", ")
    result = temp[len(temp)-1].strip()# Bỏ khoản trắng đầu và cuối string
    if 'T.' in result == True:
        result = result[2:len(result)].strip()
    else:
        result = result[3:len(result)].strip()
    return result


#Từ địa chỉ đầy đủ, trả về mã code của tỉnh/thành phố đó
#Ví dụ: input: 808, Đường 30/4, P. 11, Thành phố Vũng Tàu, T. Bà Rịa - Vũng Tàu
# output: ba-ria-vung-tau
# Cần cài thư viện: pip install unidecode

from unidecode import unidecode
def getProvinceCode(address):
    temp = getProvince(address)
    result = unidecode(temp)
    result = result.replace(' - ','-').replace(' ','-').replace('  ','-')
    result = result.lower()
    return result

#Từ địa chỉ đầy đủ, cho ra quận hoặc huyện tương ứng
# VÍ dụ: input: 808, Đường 30/4, P. 11, Thành phố Vũng Tàu, T. Bà Rịa - Vũng Tàu
# output: Thành phố Vũng Tàu
# input: Ấp Thạnh Thới, Xã Đồng Sơn, H. Gò Công Tây, T. Tiền Giang => output: Huyện Gò Công Tây
def getDistrict(address):
    temp = address.split(", ")
    result = temp[len(temp)-2].strip()# Bỏ khoản trắng đầu và cuối string
    result = result.replace("H.", "Huyện")
    result = result.replace("h.", "Huyện")
    result = result.replace("Q.", "Quận")
    result = result.replace("q.", "Quận")
    return result


#Từ địa chỉ đầy đủ, trả về mã code của quận/huyện đó
#Ví dụ: input: 808, Đường 30/4, P. 11, Thành phố Vũng Tàu, T. Bà Rịa - Vũng Tàu
# output: thanh-pho-vung-tau
# Cần cài thư viện: pip install unidecode
def getDistrictCode(address):
    temp = getDistrict(address)
    result = unidecode(temp)
    result = result.replace(' - ','-').replace(' ','-').replace('  ','-')
    result = result.lower()
    return result


#Từ địa chỉ đầy đủ, cho ra phường/ xã tương ứng
# VÍ dụ: input: 808, Đường 30/4, P. 11, Thành phố Vũng Tàu, T. Bà Rịa - Vũng Tàu
# output: Phường 11
# result = result.replace("Tt.", "Thị trấn")
# result = result.replace("P.", "Phường")
# result = result.replace("p.", "Phường")
def getVillage(address):
    temp = address.split(", ")
    result = temp[len(temp)-3].strip()# Bỏ khoản trắng đầu và cuối string
    if 'P.' in result  or 'Tt.' in result or 'Xã' in result:
        result = result.replace('P.', 'Phường')
        result = result.replace('Tt.', 'Thị trấn')
    else:
        result = 'Undefined'
    return result


#Từ địa chỉ đầy đủ, cho ra mã phường/ xã tương ứng
# VÍ dụ: input: 808, Đường 30/4, P. 11, Thành phố Vũng Tàu, T. Bà Rịa - Vũng Tàu
# output: phuong-11
def getVillageCode(address):
    temp = getVillage(address)
    result = unidecode(temp)
    result = result.replace(' - ','-').replace(' ','-').replace('  ','-')
    result = result.lower()
    return result


#Từ địa chỉ đầy đủ, cho ra dường (nếu có) tương ứng
# VÍ dụ: input: 808, Đường 30/4, P. 11, Thành phố Vũng Tàu, T. Bà Rịa - Vũng Tàu
# output: Đường 30/4
# input: 'Ấp Thạnh Thới, Xã Đồng Sơn, H. Gò Công Tây, T. Tiền Giang' => output: Ấp Thạnh Thới
def getStreet(address):
    temp = address.split(", ")
    result = temp[len(temp)-3].strip()# Bỏ khoản trắng đầu và cuối string
    if 'P.' in result  or 'Tt.' in result or 'Xã' in result:
        result = result = temp[len(temp)-4].strip()
    return result

#Từ địa chỉ đầy đủ, cho ra mã dường (nếu có) tương ứng
# VÍ dụ: input: 808, Đường 30/4, P. 11, Thành phố Vũng Tàu, T. Bà Rịa - Vũng Tàu
# output: duong-40/4
# input: 'Ấp Thạnh Thới, Xã Đồng Sơn, H. Gò Công Tây, T. Tiền Giang' => output: Ấp Thạnh Thới
def getStreetCode(address):
    temp = getStreet(address)
    result = unidecode(temp)
    result = result.replace(' - ','-').replace(' ','-').replace('  ','-')
    result = result.lower()
    return result

