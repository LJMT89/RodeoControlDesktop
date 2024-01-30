import subprocess

def get_pid_list(port):
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

def kill_processes_by_port(port):
    pid_list = get_pid_list(port)
    print(f"Estos son los PIDS asociados al puerto {port}: {pid_list}")
    if pid_list:
        print(f"Procesos encontrados asociados al puerto {port}: {', '.join(pid_list)}")
        for pid in pid_list:
            try:
                subprocess.run(['taskkill', '/F', '/PID', pid], check=True)
                print(f"Proceso con PID {pid} terminado exitosamente.")
            except subprocess.CalledProcessError:
                print(f"No se pudo terminar el proceso con PID {pid}.")
    else:
        print(f"No se encontraron procesos asociados al puerto {port}.")

if __name__ == "__main__":
    port = 8000  # Puerto a matar procesos
    kill_processes_by_port(port)
