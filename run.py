import socket
import os
hostname = socket.gethostname()
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
ip_address = s.getsockname()[0]
os.system = ('cmd /k "python manage.py runserver"')
print ("running the surver")
print(ip_address)
