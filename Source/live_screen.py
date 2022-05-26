from PIL import ImageGrab
import io
import traceback 


def capture_screen():
    try:
        img=ImageGrab.grab()
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='PNG')
        data = img_bytes.getvalue()
        return data
    except Exception as e:
        traceback.print_exc() 
        print(str(e))
        print('Lỗi chụp màn hình!')    
        return 0
    