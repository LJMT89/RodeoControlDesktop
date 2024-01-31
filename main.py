import sys, os, socket, subprocess
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QTextEdit, QPlainTextEdit, QFileDialog, QDesktopWidget
from PyQt5.QtCore import QProcess, Qt
from PyQt5.QtGui import QIcon, QPixmap

basedir = os.path.dirname(__file__)

class LanzarServidor(QMainWindow):
    def __init__(self):
        super().__init__()

        self.process = None  # Guarda una referencia al proceso para poder detenerlo
        self.process_deactivate = None
        self.process_kill_port = None
        self.txt_consola = None
        self.script_path = "D:\\IDEAFIX\\RodeoControl\\Repositorio\\Escritorio\\RodeoControlDesktop\\bin\\runserver.bat"
        self.ip_local = ''
        self.puerto = 8000
        # Configuración del ícono de la aplicación
        # Ruta del archivo de imagen
        ruta_imagen = os.path.join(basedir, "image", "la_travesada_48.ico")
        # Crear un QPixmap a partir del archivo de imagen
        pixmap = QPixmap(ruta_imagen)
        # Crear un QIcon a partir del QPixmap
        icono = QIcon(pixmap)

        self.init_ui()

    def init_ui(self):
        # Interfaz de usuario
        self.ui_ppal = uic.loadUi(os.path.join(basedir, "ui", "principal.ui"), self)

        # Personalizar el marco de las ventanas para que solo muestre un título
        self.ui_ppal.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint | Qt.WindowTitleHint | Qt.WindowMinimizeButtonHint)

        # Elementos ui principal
        self.txt_consola = self.ui_ppal.txt_consola
        self.lbl_ip_local = self.ui_ppal.lbl_ip_local
        self.btn_lanzar_server = self.ui_ppal.btn_lanzar_server
        self.btn_detener_server = self.ui_ppal.btn_detener_server
        self.btn_enlinea = self.ui_ppal.btn_enlinea
        self.btn_desconectado = self.ui_ppal.btn_desconectado
        self.btn_minimizar = self.ui_ppal.btn_minimizar
        self.btn_salir = self.ui_ppal.btn_salir

        #Controladores ui principal
        self.btn_lanzar_server.clicked.connect(self.run_shell_script)
        self.btn_detener_server.clicked.connect(self.stop_script_execution)
        self.btn_minimizar.clicked.connect(self.ui_ppal.showMinimized)
        self.btn_salir.clicked.connect(self.salir_function)
        self.lbl_ip_local.setText('......')

        self.btn_detener_server.setEnabled(False)

    def run_shell_script(self):
        self.btn_lanzar_server.setEnabled(False)
        self.btn_salir.setEnabled(False)
        self.btn_detener_server.setEnabled(True)
        self.ip_local = self.obtener_ip_local()
        if self.ip_local:
            self.ip_local = f'{self.ip_local}:8000'
        else:
            self.ip_local = "Sin conexión"
        
        if self.puerto_en_uso(self.puerto):
            self.kill_port(self.puerto)
        
        self.txt_consola.clear()
        self.process = QProcess(self)
        self.process.setProcessChannelMode(QProcess.MergedChannels)
        self.process.readyReadStandardOutput.connect(self.read_output)
        self.process.finished.connect(self.script_finished)
        self.process.start("cmd", ["/c", self.script_path])

    def read_output(self):
        self.btn_desconectado.setVisible(False)
        self.lbl_ip_local.setText(self.ip_local)
        output = self.process.readAllStandardOutput().data().decode('utf-8')
        self.txt_consola.appendPlainText(output)

    def script_finished(self, exit_code, exit_status):
        self.btn_desconectado.setVisible(True)
        self.btn_lanzar_server.setEnabled(True)
        self.btn_salir.setEnabled(True)
        self.btn_detener_server.setEnabled(False)
        self.lbl_ip_local.setText('......')
        self.txt_consola.appendPlainText(f"Script execution finished with exit code {exit_code}")

    def stop_script_execution(self):
        self.desactivar_venv()
        if self.process and self.process.state() == QProcess.Running:
            # Envía la señal de terminación al proceso
            self.process.terminate()
        self.kill_port(self.puerto)

    def obtener_ip_local(self):
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
    
    def puerto_en_uso(self, numero_puerto):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        resultado = sock.connect_ex(('localhost', numero_puerto))
        sock.close()
        return resultado == 0
    
    def desactivar_venv(self):
        self.process_deactivate = QProcess(self)
        self.process_deactivate.start('deactivate')
        if self.process_deactivate and self.process_deactivate.state() == QProcess.Running:
            # Envía la señal de terminación al proceso
            self.process_deactivate.terminate()
    
    def get_pid_list(self, port):
        pid_list = []
        netstat_output = subprocess.check_output(['netstat', '-ano'])
        netstat_lines = netstat_output.decode(errors='ignore').split('\n')
        for line in netstat_lines:
            if f":{port}" in line:
                parts = line.split()
                if len(parts) >= 2:
                    pid = parts[-1]
                    if pid.isdigit():
                        pid_list.append(pid)
        return pid_list
    
    def kill_port(self, port):
        pid_list = self.get_pid_list(port)
        # print(f"Estos son los PIDS asociados al puerto {port}: {pid_list}")
        if pid_list:
            # print(f"Procesos encontrados asociados al puerto {port}: {', '.join(pid_list)}")
            for pid in pid_list:
                try:
                    subprocess.run(['taskkill', '/F', '/PID', pid], check=True)
                    print(f"Proceso con PID {pid} terminado exitosamente.")
                except subprocess.CalledProcessError:
                    print(f"No se pudo terminar el proceso con PID {pid}.")
        else:
            print(f"No se encontraron procesos asociados al puerto {port}.")

    #Función que finaliza la aplicación - Salir
    def salir_function(self):
        self.btn_salir.setEnabled(False)
        print("Finalizando")
        sys.exit()


if __name__ == '__main__':
	app = QApplication(sys.argv)
	window = LanzarServidor()
	# Obtener el tamaño de la pantalla
	screen = QDesktopWidget().screenGeometry()
	# Obtener el tamaño de la ventana
	size = window.geometry()
	# Calcular la posición para centrado en la pantalla
	x = int((screen.width() - size.width()) / 2)
	y = int((screen.height() - size.height()) / 2)
	# Mover la ventana a la posición calculada
	window.move(x, y)
	window.show()
	sys.exit(app.exec_())
