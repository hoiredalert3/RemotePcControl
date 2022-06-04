import re, winreg
import os

def parse_data(full_path):
    try:
        #r'SOFTWARE/Microsoft/Windows/CurrentVersion/App Paths/chrome.exe'
        
        # Đổi '/' trong full_path thành '\\'
        full_path = re.sub(r'/', r'\\', full_path)
        #full_path = r'SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\App Paths\\chrome.exe'
        
        # hive =  chuỗi mà được xóa đoạn từ '\\' đến hết
        hive = re.sub(r'\\.*$', '', full_path)
        #hive = r'SOFTWARE'
        if not hive:
            raise ValueError('Invalid \'full_path\' param.')
        if len(hive) <= 4:
            if hive == 'HKLM':
                hive = 'HKEY_LOCAL_MACHINE'
            elif hive == 'HKCU':
                hive = 'HKEY_CURRENT_USER'
            elif hive == 'HKCR':
                hive = 'HKEY_CLASSES_ROOT'
            elif hive == 'HKU':
                hive = 'HKEY_USERS'
        #Xóa những kí tự là chữ từ đầu đến \\ rồi gán cho reg_key
        reg_key = re.sub(r'^[A-Z_]*\\', '', full_path)
        # reg_key = \Microsoft\\Windows\\CurrentVersion\\App Paths\\chrome.exe
        
        #Xóa những đoạn mã '\\' có kí tự ở sau đến hết
        reg_key = re.sub(r'\\[^\\]+$', '', reg_key)
        # reg_key = \Microsoft\\Windows\\CurrentVersion\\App Paths\

        reg_value = re.sub(r'^.*\\', '', full_path)
        #reg_value = r'chrome.exe'
        return hive, reg_key, reg_value

    except:
        return None, None, None


def get_value(full_path):
    value_list = parse_data(full_path)
    #value_list[0] = hive
    #value_list[1] = reg_key
    #value_list[2] = reg_name
    try:
        opened_key = winreg.OpenKey(getattr(winreg, value_list[0]), value_list[1], 0, winreg.KEY_READ)
        value_of_value, value_type = winreg.QueryValueEx(opened_key, value_list[2])
        winreg.CloseKey(opened_key)
        return ["1", value_of_value]
    except:
        return ["0", "0"]


def dec_value(c):
    c = c.upper()
    if ord('0') <= ord(c) and ord(c) <= ord('9'):
        return ord(c) - ord('0')
    if ord('A') <= ord(c) and ord(c) <= ord('F'):
        return ord(c) - ord('A') + 10
    return 0

def str_to_bin(s):
    res = b""
    for i in range(0, len(s), 2):
        a = dec_value(s[i])
        b = dec_value(s[i + 1])
        res += (a * 16 + b).to_bytes(1, byteorder='big')
    return res

def str_to_dec(s):
    s = s.upper()
    res = 0
    for i in range(0, len(s)):
        v = dec_value(s[i])
        res = res*16 + v
    return res


def set_value(full_path, value, value_type):
    value_list = parse_data(full_path)
    #value_list[0] = hive
    #value_list[1] = reg_key
    #value_list[2] = reg_value
    try:
        winreg.CreateKey(getattr(winreg, value_list[0]), value_list[1])
        opened_key = winreg.OpenKey(getattr(winreg, value_list[0]), value_list[1], 0, winreg.KEY_WRITE)
        if 'REG_BINARY' in value_type:
            if len(value) % 2 == 1:
                value += '0'
            value = str_to_bin(value)
        if 'REG_DWORD' in value_type:
            if len(value) > 8:
                value = value[:8]
            value = str_to_dec(value)
        if 'REG_QWORD' in value_type:
            if len(value) > 16:
                value = value[:16]
            value = str_to_dec(value)                 
        
        winreg.SetValueEx(opened_key, value_list[2], 0, getattr(winreg, value_type), value)
        winreg.CloseKey(opened_key)
        return ["1", "1"]
    except:
        return ["0", "0"]


def delete_value(full_path):
    value_list = parse_data(full_path)
    try:
        opened_key = winreg.OpenKey(getattr(winreg, value_list[0]), value_list[1], 0, winreg.KEY_WRITE)
        winreg.DeleteValue(opened_key, value_list[2])
        winreg.CloseKey(opened_key)
        return ["1", "1"]
    except:
        return ["0", "0"]


def create_key(full_path):
    value_list = parse_data(full_path)
    print(value_list)
    try:
        winreg.CreateKey(getattr(winreg, value_list[0]), value_list[1] + r'\\' + value_list[2])
        return ["1", "1"]
    except:
        return ["0", "0"]


def delete_key(full_path):
    value_list = parse_data(full_path)
    try:
        winreg.DeleteKey(getattr(winreg, value_list[0]), value_list[1] + r'\\' + value_list[2])
        return ["1", "1"]
    except:
        return ["0", "0"]


def registry(ID, full_path, name_value = r'', value = r'', v_type = r''):
    res = ["0", "0"]
    if ID == 0:
        try:
            outout_file = os.getcwd() + '\\run.reg'
            with open(outout_file, 'w+') as f:
                f.write(full_path)
                f.close()
            os.system(r'regedit /s ' + os.getcwd() + '\\run.reg')
            res = ["1", "1"]
            print('file reg created')
        except:
            res = ["0", "0"]
            print('cannot create file reg')

    elif ID == 1:
        res = get_value(full_path + r'\\' + name_value)     

    elif ID == 2:
        res = set_value(full_path + r'\\' + name_value, value, v_type)       
    
    elif ID == 3:
        res = delete_value(full_path + r'\\' + name_value)
    
    elif ID == 4:
        res = create_key(full_path)

    elif ID == 5:
        res = delete_key(full_path + r'\\')
    
    # res sẽ trả về 2 giá trị
    # giá trị đầu tiên là thể hiện thành công hay không
    # Nếu thành công là 1 không thành công là 0
    # giá trị thứ 2 chỉ có ở get_value tức là giá trị trả về của key_name tương ứng
    # còn các hàm còn lại thì giá trị res[1] sẽ = res[0]
    print(res)


'''
ID là để điều khiển phù hợp cho registry
Các ID tương ứng 
0 : tạo file reg với fullpath đầu vào 
## mặc định file tạo là run.reg
## Sau đó tự chạy file run.reg đã được điền fullpath trong đó

1 : get_value <line 52> 
## Trả về giá trị của value có tên là name_value trong key có vị trí tại full_path
## Hàm thực thi dựa trên hàm  QueryValueEx() của winreg
## Ý nghĩa hàm QueryValueEx() truy vấn giá trị của value_name 
## trong một regis_key đang được mở

2 : set_value <line 90> đầu vào gồm full_path, name_value, 
## value và v_type <thể hiện value được đưa vào ở dạng nào> 
## v_type in ['REG_BINARY'<chuỗi nhị phân>, 'REG_DWORD'<số nguyên HEX 8 bit>, 'REG_QWORD'<số nguyên HEX 16 bit>]
## Nếu fullpath truyền vào chưa tồn tại một key tương ứng thì sẽ tự tạo key với name tương ứng
## Hàm thực thi dựa trên hàm SetValueEx() của winreg
## Ý nghĩa hàm SetValueEx() thay đổi giá trị của regis_name thông qua tham số value đầu vào
## trong một regis_key đang được mở 

3 : delete_value <line 118> đầu vào gồm full_path và name_value
## Xóa đi value với tên name_value tại vị trí key full_path
## Hàm thực thi dựa trên hàm DeleteValue() của winreg
## Ý nghĩa hàm DeleteValue() của winreg sẽ xóa value có tên value_name
## trong một regis_key đang được mở 

4 : create_key <line 129> đầu vào full_path là vị trí key cần tạo
## Hàm thực thi dựa trên hàm CreateKey() của winreg
## Ý nghĩa hàm CreateKey() sẽ tạo key tại vị trí full_path 
## nếu đã tồn tại key thì hàm thực thi như open

5 : delete_key <line 139> đầu vào full_path là vị trí key cần xóa
## Hàm thực thi dựa trên hàm DeleteKey() của winreg
## Ý nghĩa hàm DeleteKey() sẽ xóa key tại vị trí full_path
## Nhưng sẽ không thể xóa được key có sub key nếu muốn xóa được key có sub key
## hãy tiến hàng xóa các subkey hiện có trong key rồi xóa key
'''

'''
Hàm registry <line 148>
    Là hàm thực thi chính với việc phân loại các ID phù hợp để thực thi phù hợp
    Hàm có gọi các hàm còn lại có trong file nên khi dẫn xuất dùng trong các file khác nên dẫn xuất toàn bộ các hàm
    Các tham số đầu vào:
        full_path thường là vị trí của key muốn tạo/xóa/tạo, sửa, xóa value/truy xuất value
        name_value là tên value muốn tạo/xóa/truy xuất
        value là giá trị muốn gán/tạo cho value có tên value_name 
        v_type là kiểu giá trị định dạng của value
'''

##Các giá trị ví dụ
full_path = r'HKEY_CURRENT_USER\Control Panel\Demo'
name_value = r'Demo_name'
value = r'2A' # HEX thì 2 * 16 + 10 = 42
v_type = r'REG_DWORD'

#Tạo một key với fullpath
registry(4, full_path)

#Tạo một value trong key đã tạo với tên của value là name_value
# Nếu chưa tồn tại key với full_path thì tự động tạo key tương ứng 
# Nếu chưa tồn tại value thì sẽ tự tạo một value với tên là name_value
# và gán giá trị value 
registry(2, full_path, name_value, value, v_type)

#Lấy giá trị từ value và key
registry(1, full_path, name_value)

#Xóa value từ key
registry(3, full_path, name_value)

#Xóa key đã tạo
registry(5, full_path)


