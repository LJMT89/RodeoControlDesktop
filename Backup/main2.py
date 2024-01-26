import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QPlainTextEdit, QFileDialog
from PyQt5.QtCore import QProcess, Qt

class ShellScriptRunner(QWidget):
    def __init__(self):
        super().__init__()

        self.process = None  # Guarda una referencia al proceso para poder detenerlo
        self.output_text_edit = None

        self.init_ui()

    def init_ui(self):
        # Interfaz de usuario
        self.setWindowTitle('Shell Script Runner')
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()

        self.output_text_edit = QPlainTextEdit(self)
        self.output_text_edit.setReadOnly(True)
        layout.addWidget(self.output_text_edit)

        run_button = QPushButton('Run Shell Script', self)
        run_button.clicked.connect(self.run_shell_script)
        layout.addWidget(run_button)

        stop_button = QPushButton('Stop Script Execution', self)
        stop_button.clicked.connect(self.stop_script_execution)
        layout.addWidget(stop_button)

        self.setLayout(layout)

    def run_shell_script(self):
        # options = QFileDialog.Options()
        # options |= QFileDialog.ReadOnly
        # script_path, _ = QFileDialog.getOpenFileName(self, "Seleccionar script .sh", "", "Scripts Shell (*.sh);;Todos los archivos (*)", options=options)
        script_path = '/home/jose/Escritorio/lanzar_rodeo.sh'

        if script_path:
            self.output_text_edit.clear()
            self.process = QProcess(self)
            self.process.setProcessChannelMode(QProcess.MergedChannels)
            self.process.readyReadStandardOutput.connect(self.read_output)
            self.process.finished.connect(self.script_finished)
            self.process.start(f'bash {script_path}')

    def read_output(self):
        output = self.process.readAllStandardOutput().data().decode('utf-8')
        self.output_text_edit.appendPlainText(output)

    def script_finished(self, exit_code, exit_status):
        self.output_text_edit.appendPlainText(f"Script execution finished with exit code {exit_code}")

    def stop_script_execution(self):
        self.process_deactivate = QProcess(self)
        self.process_kill_port = QProcess(self)
        self.process_deactivate.start('deactivate')
        if self.process and self.process.state() == QProcess.Running:
            # Envía la señal de terminación al proceso
            self.process.terminate()
        self.process_kill_port.start('fuser -k 8000/tcp')
        if self.process_deactivate and self.process_deactivate.state() == QProcess.Running:
            # Envía la señal de terminación al proceso
            self.process_deactivate.terminate()
        if self.process_kill_port and self.process_kill_port.state() == QProcess.Running:
            # Envía la señal de terminación al proceso
            self.process_kill_port.terminate()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ShellScriptRunner()
    window.show()
    sys.exit(app.exec_())
