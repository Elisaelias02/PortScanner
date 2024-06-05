
# PortScanner

Este es un escáner de puertos simple con una interfaz gráfica de usuario (GUI) construida usando Python y tkinter. El escáner verifica un rango especificado de puertos en una dirección IP o nombre de host objetivo e intenta identificar el servicio que se ejecuta en cada puerto abierto obteniendo el banner del servicio.

## Características

- Escanea un rango de puertos (50-85) en una dirección IP o nombre de host objetivo.
- Muestra el banner del servicio para cada puerto abierto.
- Interfaz gráfica de usuario fácil de usar construida con tkinter.
## Requisitos

- Python 3.x
- Biblioteca tkinter (usualmente incluida en las instalaciones estándar de Python)
## Cómo usar

Clonar el repositorio

```bash
git clone https://github.com/tuusuario/port-scanner.git
cd port-scanner
```

Ejecutar el Script

```bash
python3 port_scanner.py

```
## Descripción del código 

Aquí tienes una breve descripción de las partes principales del código:

##Obtención del Banner del Servicio

La función banner_grab intenta conectarse a un puerto especificado y obtener el banner del servicio:

```python
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
```

##Escaneo de Puertos

La función scan_ports escanea un rango de puertos (50-85) en el objetivo y registra los puertos abiertos junto con el banner del servicio:

```python
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
```

##Configuración de la GUI

La función start_scan inicia el escaneo cuando se hace clic en el botón "Start Scan":

```python
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
```

##Configuración de la Ventana Principal

El script configura la ventana principal y sus elementos:

```python
root = tk.Tk()
root.title("Port Scanner")
root.geometry("500x400")

tk.Label(root, text="Enter the IP address or hostname:").pack(pady=10)
entry_target = tk.Entry(root, width=50)
entry_target.pack(pady=5)

scan_button = tk.Button(root, text="Start Scan", command=start_scan)
scan_button.pack(pady=10)

output_text = scrolledtext.ScrolledText(root, width=60, height=15, state=tk.DISABLED)
output_text.pack(pady=10)

output_text.tag_config("open", foreground="green")

root.mainloop()
```