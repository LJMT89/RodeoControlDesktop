import socket

def obtener_ip_local():
    try:
        # Crear un socket y obtener la dirección IP local
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0.1)  # Configurar un tiempo de espera para evitar bloqueo
        s.connect(("8.8.8.8", 80))  # Se conecta a una IP externa (puede ser cualquier IP)
        ip_local = s.getsockname()[0]
        s.close()
        return ip_local
    except Exception as e:
        print(f"Error al obtener la IP local: {e}")
    
    return None

# Mostrar la dirección IP local en consola
ip_local = obtener_ip_local()

if ip_local:
    print("La dirección IP local es:", ip_local)
else:
    print("No se pudo obtener la dirección IP local.")
