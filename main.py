import numpy as np
import cv2
import mediapipe as mp
from math import hypot
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import screen_brightness_control as sbc
import os
import sys

# Thiết lập mã hóa UTF-8 cho terminal
if sys.platform.startswith('win'):
    # Cho Windows
    os.system('chcp 65001')

class GestureControlSystem:
    def __init__(self):
        # Khoi tao webcam
        self.cap = cv2.VideoCapture(0)
        
        # Khoi tao MediaPipe Hands
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
            static_image_mode=False,
            model_complexity=1,
            min_detection_confidence=0.75,
            min_tracking_confidence=0.75,
            max_num_hands=2
        )
        self.mpDraw = mp.solutions.drawing_utils
        
        # Khoi tao dieu khien thiet bi am thanh
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self.volume = cast(interface, POINTER(IAudioEndpointVolume))
        self.volMin, self.volMax = self.volume.GetVolumeRange()[:2]
        
        # Gia tri ban dau
        self.volbar = 400
        self.volper = 0
        
        # Che do dieu khien: 0 cho am luong, 1 cho do sang
        self.mode = 0
        self.modes = ["Dieu khien am luong", "Dieu khien do sang man hinh"]
        
        # Kich thuoc nut menu
        self.menu_height = 50
        self.button_width = 200
        
        # Co de kiem soat trang thai chay
        self.running = True
        
        # Thiết lập font cho tiếng Việt
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        
        # Kích thước cửa sổ
        self.window_width = 720
        self.window_height = 576
        
    def process_volume_control(self, img, lmList):
        # Xu ly dieu khien am luong bang cu chi tay
        # Lay dau ngon cai (landmark 4) va dau ngon ut (landmark 20)
        x1, y1 = lmList[4][1], lmList[4][2]  # Dau ngon cai
        x2, y2 = lmList[20][1], lmList[20][2]  # Dau ngon ut
        
        # Ve vong tron o cac dau ngon va mot duong thang giua chung
        cv2.circle(img, (x1, y1), 13, (255, 0, 0), cv2.FILLED)
        cv2.circle(img, (x2, y2), 13, (255, 0, 0), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 3)
        
        # Tinh khoang cach giua cac dau ngon
        length = hypot(x2 - x1, y2 - y1)
        
        # Dieu chinh cac gia tri nay dua tren kich thuoc tay va khoang cach camera
        min_distance = 50  # Khoang cach toi thieu du kien
        max_distance = 300  # Khoang cach toi da du kien
        
        # Anh xa khoang cach tay den pham vi am luong
        vol = np.interp(length, [min_distance, max_distance], [self.volMin, self.volMax])
        self.volbar = np.interp(length, [min_distance, max_distance], [400, 150])
        self.volper = np.interp(length, [min_distance, max_distance], [0, 100])
        
        # Dat am luong he thong
        self.volume.SetMasterVolumeLevel(vol, None)
        
        # Ve thanh am luong
        cv2.rectangle(img, (50, 150), (85, 400), (0, 0, 255), 4)
        cv2.rectangle(img, (50, int(self.volbar)), (85, 400), (0, 0, 255), cv2.FILLED)
        cv2.putText(img, f"Am luong: {int(self.volper)}%", (10, 70), self.font, 1, (0, 255, 98), 3)
        
    def process_brightness_control(self, img, lmList):
        # Xu ly dieu khien do sang bang cu chi tay
        # Lay dau ngon cai (landmark 4) va dau ngon ut (landmark 20)
        x1, y1 = lmList[4][1], lmList[4][2]  # Dau ngon cai
        x2, y2 = lmList[20][1], lmList[20][2]  # Dau ngon ut
        
        # Ve vong tron o cac dau ngon va mot duong thang giua chung
        cv2.circle(img, (x1, y1), 13, (0, 255, 0), cv2.FILLED)
        cv2.circle(img, (x2, y2), 13, (0, 255, 0), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 3)
        
        # Tinh khoang cach giua cac dau ngon
        length = hypot(x2 - x1, y2 - y1)
        
        # Anh xa khoang cach tay den pham vi do sang
        brightness_level = np.interp(length, [15, 220], [0, 100])
        
        # Dat do sang
        sbc.set_brightness(int(brightness_level))
        
        # Hien thi muc do sang
        cv2.putText(img, f"Do sang: {int(brightness_level)}%", (10, 70), self.font, 1, (0, 255, 98), 3)

    def display_terminal_menu(self):
        # Hien thi menu trong terminal cho nguoi dung chon che do
        os.system('cls' if os.name == 'nt' else 'clear')  # Xoa man hinh terminal
        print("===== HỆ THỐNG ĐIỀU KHIỂN CỬ CHỈ =====")
        print("Chọn chế độ điều khiển:")
        print("1. Điều khiển âm lượng")
        print("2. Điều khiển độ sáng")
        print("0. Thoát chương trình")
        
        choice = input("Nhập lựa chọn của bạn: ")
        
        if choice == '1':
            self.mode = 0
            return True
        elif choice == '2':
            self.mode = 1
            return True
        elif choice == '0':
            self.running = False
            return False
        else:
            print("Lựa chọn không hợp lệ. Vui lòng thử lại.")
            input("Nhấn Enter để tiếp tục...")
            return self.display_terminal_menu()
    
    def run(self):
        # Ham chinh de chay chuong trinh
        while self.running:
            # Hien thi menu terminal va cho nguoi dung chon che do
            if not self.display_terminal_menu():
                break
                
            # Hien thi thong bao che do da chon
            print(f"Đã chọn chế độ: {self.modes[self.mode]}")
            print("Đang khởi chạy giao diện điều khiển cử chỉ...")
            print("Nhấn 'q' để quay lại menu chọn chế độ")
            
            # Khoi dong giao dien dieu khien cu chi
            self.run_gesture_interface()
            
    def run_gesture_interface(self):
        # Chay giao dien dieu khien cu chi voi webcam
        # Tao cua so co ten va thiet lap kich thuoc
        cv2.namedWindow('He Thong Dieu Khien Cu Chi', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('He Thong Dieu Khien Cu Chi', self.window_width, self.window_height)
        
        while True:
            success, img = self.cap.read()
            if not success:
                print("Không thể chụp ảnh từ camera")
                break
                
            # Lat hinh anh de tuong tac truc quan hon
            img = cv2.flip(img, 1)
                
            # Chuyen doi sang RGB cho MediaPipe
            imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            
            # Xu ly hinh anh
            results = self.hands.process(imgRGB)

            lmList = []
            if results.multi_hand_landmarks:
                # Lay ban tay dau tien duoc phat hien
                handLandmarks = results.multi_hand_landmarks[0]
                
                # Trich xuat tat ca cac diem moc
                for id, lm in enumerate(handLandmarks.landmark):
                    h, w, _ = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    lmList.append([id, cx, cy])
                
                # Ve cac diem moc ban tay
                self.mpDraw.draw_landmarks(img, handLandmarks, self.mpHands.HAND_CONNECTIONS)
            
            # Xu ly dua tren che do da chon neu phat hien ban tay
            if len(lmList) >= 21:  # Dam bao chung ta co du cac diem moc (0-20)
                if self.mode == 0:  # Dieu khien am luong
                    self.process_volume_control(img, lmList)
                else:  # Dieu khien do sang
                    self.process_brightness_control(img, lmList)
            else:
                # Hien thi thong bao trang thai neu khong co ban tay hoac khong du diem moc
                cv2.putText(img, "Khong phat hien ban tay", (10, 100), self.font, 1, (0, 0, 255), 2)
                
            # Hien thi che do hien tai o goc tren
            status_text = f"Che do: {self.modes[self.mode]}"
            cv2.putText(img, status_text, (10, 30), self.font, 0.8, (255, 255, 255), 2)
            
            # Hien thi huong dan thoat
            cv2.putText(img, "Nhan 'q' de quay lai menu", (10, img.shape[0] - 20), self.font, 0.8, (255, 255, 255), 2)
            
            # Hien thi hinh anh
            cv2.imshow('He Thong Dieu Khien Cu Chi', img)
            
            # Thoat khoi vong lap khi nhan 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Dong cua so nhung khong giai phong camera
        cv2.destroyAllWindows()
        
    def cleanup(self):
        # Giai phong tai nguyen khi ket thuc chuong trinh
        if self.cap is not None:
            self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    # Tao doi tuong va chay chuong trinh
    try:
        # Thiết lập mã hóa UTF-8 cho đầu ra terminal
        if sys.stdout.encoding != 'utf-8':
            sys.stdout.reconfigure(encoding='utf-8')
        
        app = GestureControlSystem()
        app.run()
    except KeyboardInterrupt:
        print("\nChương trình đã bị ngắt bởi người dùng")
    except Exception as e:
        print(f"Lỗi: {e}")
    finally:
        # Dam bao tai nguyen duoc giai phong
        if 'app' in locals():
            app.cleanup()
        print("Chương trình đã kết thúc")