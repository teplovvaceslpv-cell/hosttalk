from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import webbrowser
import socket
import subprocess
import threading
import platform
import os
import sys
import shutil

# --- Импорты только для Windows ---
if platform.system() == "Windows":
    import pystray
    from PIL import Image
    from pystray import MenuItem as dihtem
    import ctypes

# --- Настройки ---
HOSTTALK0INFO0VER = 1.0
pref0admintoall = True
pref0showall = False

# --- Папка для хранения данных ---
if platform.system() == "Windows":
    APPDATAAHH = os.getenv("APPDATA")
    if APPDATAAHH is None:
        APPDATAAHH = os.getcwd()
else:
    APPDATAAHH = os.getcwd()

APPROOT = os.path.join(APPDATAAHH, "HostTalk")
os.makedirs(APPROOT, exist_ok=True)

def exe():
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))

temp0dih0server = exe()

def packurbagsahh(dih, seconddih):
    os.makedirs(seconddih, exist_ok=True)
    for dihh in os.listdir(dih):
        sdih = os.path.join(dih, dihh)
        ddih = os.path.join(seconddih, dihh)
        if not os.path.exists(ddih):
            if os.path.isdir(sdih):
                shutil.copytree(sdih, ddih)
            else:
                shutil.copy2(sdih, ddih)

packurbagsahh(os.path.join(temp0dih0server, "static"),
              os.path.join(APPROOT, "static"))
packurbagsahh(os.path.join(temp0dih0server, "templates"),
              os.path.join(APPROOT, "templates"))

# --- Windows Tray Functions ---
if platform.system() == "Windows":
    ker = ctypes.WinDLL("kernel32")
    use = ctypes.WinDLL("user32")
    SH = 5
    HI = 0

    def consolepi():
        return ker.GetConsoleWindow()

    def hideall():
        h = consolepi()
        if h:
            use.ShowWindow(h, HI)

    def showall():
        h = consolepi()
        if h:
            use.ShowWindow(h, SH)

    def traySH(ic, it):
        h = consolepi()
        if h:
            use.ShowWindow(h, SH)

    def trayQU(ic, it):
        try:
            s.stop()
        except:
            pass
        ic.stop()
        os._exit(0)

    def trayIC():
        img = Image.open(os.path.join(exe(), 'icon.ico'))
        menu = (
            dihtem("show console", traySH),
            dihtem("quit", trayQU)
        )
        icon = pystray.Icon("HostTalk", img, "HostTalk Server", menu)
        icon.run()

# --- Функция получения IP и SSID ---
def cityboii():
    se = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        se.connect(('8.8.8.8', 80))
        ip = se.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        se.close()

    ssid = "Server/Cloud"
    try:
        if platform.system() == 'Windows':
            ssid = subprocess.check_output(
                ['powershell', "-Command", "(Get-NetConnectionProfile | Where-object {$_.InterfaceAlias -like '*Wi-Fi*'}).Name"],
                text=True).strip()
        elif platform.system() == "Linux":
            ssid = subprocess.check_output(['iwgetid', "-r"], text=True).strip()
        elif platform.system() == 'Darwin':
            ssid = subprocess.check_output(
                ['/System/Library/PrivateFrameworks/Apple80211.framework/Version/Current/Resources/airport', "-I"],
                text=True).split('SSID: ')[1].splitlines()[0]
    except Exception as e:
        print(f'[LOG] Could not get Wi-Fi SSID: {e}')
        
    return ip, ssid

# --- Flask и SocketIO ---
app = Flask(__name__, template_folder=os.path.join(APPROOT, "templates"), static_folder=os.path.join(APPROOT, "static"))
app.config["AUTH"] = "local"
s = SocketIO(app, cors_allowed_origins="*")

mainchat = []
users = {}

@app.route('/', methods=["GET"])
def w():
    return render_template('index.html')

# --- ИСПРАВЛЕННЫЙ ОБРАБОТЧИК (принимает объект) ---
@s.on("join")
def usrn(data):
    # Извлекаем имя из объекта, который присылает фронтенд (например, {name: "Вася"})
    username = data.get('name') if isinstance(data, dict) else str(data)
    
    users[request.sid] = username
    print(f"│ User connected : {username}")
    
    # Отправляем историю чата при подключении
    for msg in mainchat:
        emit("mainchat", msg)

@s.on("mainchat")
def chat(msg):
    dihname = users.get(request.sid, 'unknown')
    # Формируем объект для отправки на фронтенд
    d = {'name': dihname, "msg": msg}
    
    mainchat.append(d)
    mainchat[:] = mainchat[-20:] # Храним последние 20 сообщений
    
    # Отправляем всем
    emit("mainchat", d, broadcast=True)
    
    if pref0showall:
        print(f"│ Notification : {dihname} sent a message '{msg}'")
    else:
        print(f"│ Notification : {dihname} sent a message (hidden)")

@s.on("disconnect")
def sybau():
    print(f"│ User disconnected : {users.get(request.sid, request.sid)}")
    users.pop(request.sid, None)

@app.route('/api/ip')
def ip():
    ip, ssid = cityboii()
    return jsonify({"ip": ip, "ssid": ssid})

@s.on("shut")
def off():
    if pref0admintoall:
        print(f"│ {users.get(request.sid, request.sid)} shut down the server.")
        s.stop()
    else:
        print(f"│ {users.get(request.sid, request.sid)} tried to shut down the server.")
        print(f"│ Permission denied.")

if __name__ == '__main__':
    if platform.system() == "Windows":
        if consolepi():
            hideall()
        threading.Thread(target=trayIC, daemon=True).start()

    print(
        f"""
        `7MMF'  `7MMF'                   mm       MMP""MM""YMM      `7MM  `7MM      
          MM      MM                     MM       P'   MM   `7        MM    MM     
          MM      MM  ,pW"Wq.  ,pP"Ybd mmMMmm          MM   ,6"Yb.    MM    MM  ,MP'
          MMmmmmmmMM 6W'   `Wb 8I   `"   MM            MM  8)   MM    MM    MM ;Y   
          MM      MM 8M     M8 `YMMMa.   MM            MM   ,pm9MM    MM    MM;Mm   
          MM      MM YA.   ,A9 L.   I8   MM            MM  8M   MM    MM    MM `Mb. 
        .JMML.  .JMML.`Ybmd9'  M9mmmP'   `Mbmo       .JMML.`Moo9^Yo..JMML..JMML. YA.
                                                                                       {HOSTTALK0INFO0VER}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━                                                                  
""")

    sss, ssss = cityboii()
    print("│ Server : running")
    print(f"│ Local access : http://127.0.0.1:6767/")
    print(f"│ Lan access (other devices/wifi): http://{sss}:6767/")
    print(f"│ Wifi SSID : {ssss}")
    print(" ")
    print(f"│ Opening : http://{sss}:6767/")
    webbrowser.open_new_tab(f'http://{sss}:6767/')
    print('')
    s.run(app, host="0.0.0.0", port=6767, debug=False)