import socket


def get_local_ip():
    try:
        # Cria um socket DGRAM
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
    except Exception as e:
        print(f"Erro ao obter o endereço IP local: {e}")
        ip = "127.0.0.1"
    return ip