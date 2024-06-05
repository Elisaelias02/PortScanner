import sys
import socket
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, scrolledtext

# Banner de servicios
def banner_grab(ip, port):
    try:
        s = socket.socket()
        s.settimeout(2)
        s.connect((ip, port))
        banner = s.recv(1024).decode().strip()
        s.close()  # Asegurarse de cerrar el socket
        return banner
    except:
        return "Cannot retrieve the service"

# Función de escaneo de puertos
def scan_ports(target):
    results = []
    try:
        for port in range(50, 85):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket.setdefaulttimeout(1)
            result = s.connect_ex((target, port))
            if result == 0:
                banner = banner_grab(target, port)
                results.append(f"Port {port} is open. Service: {banner}")
            s.close()
    except Exception as e:
        results.append(f"Error: {str(e)}")
    return results

# Función para iniciar el escaneo
def start_scan():
    target = entry_target.get()
    if not target:
        messagebox.showerror("Error", "Please enter an IP address or hostname.")
        return
    
    try:
        target_ip = socket.gethostbyname(target)
    except socket.gaierror:
        messagebox.showerror("Error", "Hostname could not be resolved.")
        return
    except Exception as e:
        messagebox.showerror("Error", f"Unknown error: {str(e)}")
        return

    output_text.config(state=tk.NORMAL)
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, "-" * 50 + "\n")
    output_text.insert(tk.END, f"Scanning target: {target_ip}\n")
    output_text.insert(tk.END, f"Time started: {str(datetime.now())}\n")
    output_text.insert(tk.END, "-" * 50 + "\n")
    
    results = scan_ports(target_ip)
    
    for result in results:
        if "open" in result:
            output_text.insert(tk.END, result + "\n", "open")
        else:
            output_text.insert(tk.END, result + "\n")
    
    output_text.config(state=tk.DISABLED)

# Configuración de la ventana principal
root = tk.Tk()
root.title("Port Scanner")
root.geometry("500x400")

# Entrada del objetivo
tk.Label(root, text="Enter the IP address or hostname:").pack(pady=10)
entry_target = tk.Entry(root, width=50)
entry_target.pack(pady=5)

# Botón de escaneo
scan_button = tk.Button(root, text="Start Scan", command=start_scan)
scan_button.pack(pady=10)

# Área de salida
output_text = scrolledtext.ScrolledText(root, width=60, height=15, state=tk.DISABLED)
output_text.pack(pady=10)

# Configuración de colores
output_text.tag_config("open", foreground="green")

# Iniciar el bucle principal de la ventana
root.mainloop()