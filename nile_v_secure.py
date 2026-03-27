import cv2
import os
import pandas as pd
from deepface import DeepFace
from datetime import datetime
import customtkinter as ctk
from PIL import Image, ImageTk
import pyttsx3
import threading
import sys




FACES_DIR = "stored_faces"
LOG_FILE = "attendance_log.csv"
if not os.path.exists(FACES_DIR): os.makedirs(FACES_DIR)


engine = pyttsx3.init()
def speak(text):
    def run_speak():
        try:
            engine.say(text)
            engine.runAndWait()
        except: pass
    threading.Thread(target=run_speak, daemon=True).start()


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class AttendanceApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("NileCortex V-SECURE PRO")
        self.geometry("1150x800")
        ctk.set_appearance_mode("dark")

        # متغيرات النظام
        self.cap = None
        self.is_scanning = False
        self.frame_count = 0 
        self.last_box = None
        self.last_name = ""
        self.last_voice_time = datetime.now()

        # --- القائمة الجانبية 
        self.sidebar = ctk.CTkFrame(self, width=240, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")

       
        self.brand_label = ctk.CTkLabel(self.sidebar, text="NileCortex", 
                                       font=("Orbitron", 28, "bold"), 
                                       text_color="#3498db")
        self.brand_label.pack(pady=(40, 5))
        
        self.sub_brand = ctk.CTkLabel(self.sidebar, text="V-SECURE AI SYSTEM", 
                                     font=("Arial", 10, "bold"), 
                                     text_color="#95a5a6")
        self.sub_brand.pack(pady=(0, 30))


        try:
            self.after(200, lambda: self.iconbitmap(resource_path("nile_icon.ico")))
            self.logo_img = ctk.CTkImage(light_image=Image.open(resource_path("logo.png")),
                                        dark_image=Image.open(resource_path("logo.png")),
                                        size=(120, 120))
            self.logo_label = ctk.CTkLabel(self.sidebar, image=self.logo_img, text="")
            self.logo_label.pack(pady=10)
        except: pass

        # 2. أزرار التحكم
        self.btn_scan = ctk.CTkButton(self.sidebar, text="🔍 LIVE SCANNER", 
                                     command=self.show_scanner, height=45, fg_color="#2980b9", hover_color="#3498db")
        self.btn_scan.pack(pady=10, padx=20)
        
        self.btn_reg = ctk.CTkButton(self.sidebar, text="👤 REGISTER FACE", 
                                    command=self.show_registration, height=45, fg_color="#2c3e50")
        self.btn_reg.pack(pady=10, padx=20)
        
        self.btn_dash = ctk.CTkButton(self.sidebar, text="📊 ANALYTICS", 
                                     command=self.show_dashboard, height=45, fg_color="#2c3e50")
        self.btn_dash.pack(pady=10, padx=20)

        
        self.dev_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.dev_frame.pack(side="bottom", pady=40)
        
        ctk.CTkLabel(self.dev_frame, text="Developed & Engineered by:", 
                    font=("Arial", 11, "italic"), text_color="#7f8c8d").pack()
        ctk.CTkLabel(self.dev_frame, text="OSMAN IBRAHIM", 
                    font=("Arial", 16, "bold"), text_color="#3498db").pack()

        # 
        self.main_frame = ctk.CTkFrame(self, corner_radius=15, fg_color="#1e1e1e")
        self.main_frame.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        self.show_scanner()

    def stop_camera(self):
        if self.cap:
            self.cap.release()
            self.cap = None
        self.is_scanning = False
        self.last_box = None

    def log_attendance(self, name):
        date_now = datetime.now().strftime("%Y-%m-%d")
        time_now = datetime.now().strftime("%H:%M:%S")
        if not os.path.exists(LOG_FILE):
            pd.DataFrame(columns=["Name", "Date", "Time"]).to_csv(LOG_FILE, index=False)
        df = pd.read_csv(LOG_FILE)
        is_already_logged = ((df['Name'] == name) & (df['Date'] == date_now) & (df['Time'].str.startswith(time_now[:5]))).any()
        if not is_already_logged:
            pd.DataFrame([[name, date_now, time_now]], columns=["Name", "Date", "Time"]).to_csv(LOG_FILE, mode='a', header=False, index=False)
            if (datetime.now() - self.last_voice_time).total_seconds() > 10:
                speak(f"Welcome back {name}")
                self.last_voice_time = datetime.now()

    def show_dashboard(self):
        self.stop_camera()
        for widget in self.main_frame.winfo_children(): widget.destroy()
        ctk.CTkLabel(self.main_frame, text="SYSTEM ANALYTICS & LOGS", font=("Arial", 24, "bold")).pack(pady=20)
        if os.path.exists(LOG_FILE):
            df = pd.read_csv(LOG_FILE)
            if not df.empty:
                df['Full_Time'] = pd.to_datetime(df['Date'] + ' ' + df['Time'])
                summary = df.groupby('Name').agg(First_In=('Full_Time', 'min'), Last_In=('Full_Time', 'max'), Total=('Name', 'count')).reset_index()
                table_frame = ctk.CTkScrollableFrame(self.main_frame, width=850, height=500); table_frame.pack(pady=20, padx=20, fill="both", expand=True)
                headers = ["NAME", "FIRST ENROLLMENT", "LATEST ACTIVITY", "VISITS"]
                for i, h in enumerate(headers): ctk.CTkLabel(table_frame, text=h, font=("Arial", 13, "bold"), text_color="#3498db").grid(row=0, column=i, padx=25, pady=10)
                for index, row in summary.iterrows():
                    ctk.CTkLabel(table_frame, text=row['Name']).grid(row=index+1, column=0, padx=25, pady=8)
                    ctk.CTkLabel(table_frame, text=row['First_In'].strftime('%Y-%m-%d %H:%M')).grid(row=index+1, column=1, padx=25, pady=8)
                    ctk.CTkLabel(table_frame, text=row['Last_In'].strftime('%Y-%m-%d %H:%M')).grid(row=index+1, column=2, padx=25, pady=8)
                    ctk.CTkLabel(table_frame, text=str(row['Total'])).grid(row=index+1, column=3, padx=25, pady=8)

    def show_scanner(self):
        self.stop_camera()
        for widget in self.main_frame.winfo_children(): widget.destroy()
        self.video_label = ctk.CTkLabel(self.main_frame, text="", width=640, height=480, fg_color="#000000", corner_radius=10); self.video_label.pack(pady=10)
        self.cap = cv2.VideoCapture(0)
        self.is_scanning = True
        self.update_scanner()

    def update_scanner(self):
        if self.is_scanning and self.cap:
            ret, frame = self.cap.read()
            if ret:
                self.frame_count += 1
                if self.frame_count % 10 == 0:
                    try:
                        small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
                        results = DeepFace.find(img_path=small_frame, db_path=FACES_DIR, model_name='VGG-Face', detector_backend='opencv', enforce_detection=False, silent=True)
                        if len(results) > 0 and not results[0].empty:
                            match = results[0].iloc[0]
                            self.last_name = os.path.basename(match['identity']).split('.')[0]
                            self.last_box = [int(v * 2) for v in [match['source_x'], match['source_y'], match['source_w'], match['source_h']]]
                            self.log_attendance(self.last_name)
                        else: self.last_box = None
                    except: self.last_box = None
                if self.last_box:
                    x, y, w, h = self.last_box
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (46, 204, 113), 3)
                    cv2.putText(frame, f"VERIFIED: {self.last_name}", (x, y-15), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (46, 204, 113), 2)
                img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB); img = Image.fromarray(img); img_tk = ImageTk.PhotoImage(image=img)
                self.video_label.configure(image=img_tk); self.video_label._image = img_tk
            self.after(10, self.update_scanner)

    def show_registration(self):
        self.stop_camera()
        for widget in self.main_frame.winfo_children(): widget.destroy()
        ctk.CTkLabel(self.main_frame, text="BIOMETRIC REGISTRATION", font=("Arial", 24, "bold")).pack(pady=20)
        self.entry_name = ctk.CTkEntry(self.main_frame, placeholder_text="Enter Full Name", width=400, height=45); self.entry_name.pack(pady=10)
        self.reg_video_label = ctk.CTkLabel(self.main_frame, text="", width=480, height=360, fg_color="#000000", corner_radius=10); self.reg_video_label.pack(pady=10)
        ctk.CTkButton(self.main_frame, text="CAPTURE BIOMETRICS", command=self.save_id, width=400, height=50, fg_color="#2ecc71").pack(pady=20)
        self.cap = cv2.VideoCapture(0); self.is_scanning = True; self.update_registration_preview()

    def update_registration_preview(self):
        if self.is_scanning and self.cap:
            ret, frame = self.cap.read()
            if ret:
                img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB); img = Image.fromarray(img).resize((480, 360)); img_tk = ImageTk.PhotoImage(image=img)
                self.reg_video_label.configure(image=img_tk); self.reg_video_label._image = img_tk
            self.after(10, self.update_registration_preview)

    def save_id(self):
        name = self.entry_name.get().strip()
        if name and self.cap:
            ret, frame = self.cap.read()
            if ret:
                file_path = os.path.join(FACES_DIR, f"{name}.jpg")
                cv2.imwrite(file_path, frame)
                speak(f"Hello {name}, welcome to NileCortex. Your profile is saved.")
                self.log_attendance(name)
                ctk.CTkLabel(self.main_frame, text=f"✅ ENROLLED SUCCESSFULLY: {name}", text_color="#2ecc71").pack()

if __name__ == "__main__":
    app = AttendanceApp()
    app.mainloop()
