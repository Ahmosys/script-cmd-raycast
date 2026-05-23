import socket

# Configurez l'IP et le port de l'ampoule
bulb_ip = "192.168.1.67"
bulb_port = 55443

# Connectez-vous à l'ampoule
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((bulb_ip, bulb_port))

# Écoutez les messages
while True:
    data = sock.recv(1024)
    if data:
        print("Log reçu:", data.decode('utf-8'))
