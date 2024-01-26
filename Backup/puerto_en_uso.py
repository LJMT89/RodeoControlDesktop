import socket

def puerto_en_uso(numero_puerto):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    resultado = sock.connect_ex(('localhost', numero_puerto))
    sock.close()
    return resultado == 0

# Ejemplo: Verificar si el puerto 8000 está en uso
puerto = 8000

if puerto_en_uso(puerto):
    print(f"El puerto {puerto} está en uso.")
else:
    print(f"El puerto {puerto} no está en uso.")
