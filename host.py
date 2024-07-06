import socket
hostname = socket.gethostname()

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
ip_address = s.getsockname()[0]
ip_address2 =  socket.gethostbyname(socket.gethostname()+'.')

if __name__ == '__main__' :
    print(hostname)
    print(ip_address)
    print(ip_address2)

