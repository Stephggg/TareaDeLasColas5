import time
import threading
import random
from collections import deque
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

# =============================
# MODELO DE DATOS
# =============================

class Llamada:
    def __init__(self, nombre_cliente, motivo):
        self.nombre_cliente = nombre_cliente
        self.motivo = motivo
        self.hora_entrada = datetime.now()
        self.hora_salida = None

    def __str__(self):
        texto = (f"{self.hora_entrada.strftime('%H:%M:%S')} | Cliente: {self.nombre_cliente} | "
                 f"Motivo: {self.motivo}")
        if self.hora_salida:
            texto += f" | Terminada: {self.hora_salida.strftime('%H:%M:%S')}"
        return texto

# =============================
# LÓGICA DE NEGOCIO
# =============================

class CallCenter:
    def __init__(self, agentes_disponibles=5):
        self.cola_llamadas = deque()
        self.en_atencion = []
        self.historial = []
        self.lock = threading.Lock()
        self.agentes_disponibles = agentes_disponibles
        self.ocupados = 0

    def agregar_llamada(self, llamada):
        self.cola_llamadas.append(llamada)
        return f"Llamada registrada: {llamada}"

    def atender_llamada(self, update_callback=None):
        if self.ocupados >= self.agentes_disponibles:
            return "Todos los agentes están ocupados. Espere un momento..."
        if not self.cola_llamadas:
            return "No hay llamadas en espera."
        llamada = self.cola_llamadas.popleft()
        self.ocupados += 1
        hilo = threading.Thread(target=self._procesar_llamada, args=(llamada, update_callback))
        hilo.daemon = True
        hilo.start()
        return f"Atendiendo llamada de {llamada.nombre_cliente}..."

    def _procesar_llamada(self, llamada, update_callback=None):
        with self.lock:
            self.en_atencion.append(llamada)
            if update_callback:
                update_callback()
        tiempo = random.randint(7, 20)  # 7 a 20 segundos
        time.sleep(tiempo)
        with self.lock:
            self.en_atencion.remove(llamada)
            llamada.hora_salida = datetime.now()
            self.historial.append(llamada)
            self.ocupados -= 1
            if update_callback:
                update_callback()

    def ver_llamada_actual(self):
        if self.en_atencion:
            return [str(llamada) for llamada in self.en_atencion]
        else:
            return ["No hay llamadas siendo atendidas en este momento."]

    def ver_llamadas_pendientes(self):
        if self.cola_llamadas:
            return [str(llamada) for llamada in self.cola_llamadas]
        else:
            return ["No hay llamadas pendientes."]

    def ver_historial(self):
        if self.historial:
            return [str(llamada) for llamada in self.historial]
        else:
            return ["Aún no se han atendido llamadas."]

# =============================
# INTERFAZ GRÁFICA (Tkinter)
# =============================

class CallCenterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("📞 Call Center - Simulador de Atención de Llamadas")
        self.root.geometry("800x600")
        self.root.configure(bg="#e6f2ff")

        self.call_center = CallCenter(agentes_disponibles=4)  # Cambiado a 4 agentes

        # Encabezado bonito
        header = tk.Label(root, text="📞 Call Center - Simulador de Atención", font=("Arial", 22, "bold"), bg="#3399ff", fg="white", pady=10)
        header.pack(fill=tk.X)

        # Frame de botones
        btn_frame = tk.Frame(root, bg="#e6f2ff")
        btn_frame.pack(pady=10)

        self.btn_nueva = ttk.Button(btn_frame, text="Registrar nueva llamada", command=self.registrar_llamada)
        self.btn_nueva.grid(row=0, column=0, padx=8)

        self.btn_atender = ttk.Button(btn_frame, text="Atender siguiente llamada", command=self.atender_llamada)
        self.btn_atender.grid(row=0, column=1, padx=8)

        self.btn_actual = ttk.Button(btn_frame, text="Ver llamadas en atención", command=self.mostrar_en_atencion)
        self.btn_actual.grid(row=0, column=2, padx=8)

        self.btn_pendientes = ttk.Button(btn_frame, text="Ver llamadas pendientes", command=self.mostrar_pendientes)
        self.btn_pendientes.grid(row=0, column=3, padx=8)

        self.btn_historial = ttk.Button(btn_frame, text="Ver historial", command=self.mostrar_historial)
        self.btn_historial.grid(row=0, column=4, padx=8)

        # Área de texto para mostrar información
        self.text_area = tk.Text(root, height=25, font=("Consolas", 11), bg="#f7fbff", fg="#003366")
        self.text_area.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Estado de agentes
        self.status_label = tk.Label(root, text="Agentes disponibles: 4", font=("Arial", 12, "bold"), bg="#e6f2ff", fg="#006699")
        self.status_label.pack(pady=5)

        self.actualizar_estado()

    def actualizar_estado(self):
        libres = self.call_center.agentes_disponibles - self.call_center.ocupados
        self.status_label.config(text=f"Agentes disponibles: {libres} / {self.call_center.agentes_disponibles}")

    def registrar_llamada(self):
        nombre = simpledialog.askstring("Registrar llamada", "Nombre del cliente:")
        if not nombre:
            return
        motivos = ["Consulta de saldo", "Problema técnico", "Información de productos", "Otro"]
        motivo = simpledialog.askstring("Registrar llamada", f"Motivo de la llamada:\n1. Consulta de saldo\n2. Problema técnico\n3. Información de productos\n4. Otro\n\nEscriba el motivo o elija un número:")
        if motivo in ["1", "2", "3"]:
            motivo = motivos[int(motivo)-1]
        elif motivo == "4" or motivo is None or motivo.strip() == "":
            motivo = simpledialog.askstring("Otro motivo", "Escriba el motivo de la llamada:")
            if not motivo:
                return
        llamada = Llamada(nombre, motivo)
        msg = self.call_center.agregar_llamada(llamada)
        self.mostrar_pendientes()
        messagebox.showinfo("Llamada registrada", msg)
        self.actualizar_estado()

    def atender_llamada(self):
        msg = self.call_center.atender_llamada(self.refrescar_todo)
        messagebox.showinfo("Atención", msg)
        self.refrescar_todo()

    def mostrar_en_atencion(self):
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, "Llamadas en atención:\n\n")
        for l in self.call_center.ver_llamada_actual():
            self.text_area.insert(tk.END, f"- {l}\n")
        self.actualizar_estado()

    def mostrar_pendientes(self):
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, "Llamadas pendientes:\n\n")
        for l in self.call_center.ver_llamadas_pendientes():
            self.text_area.insert(tk.END, f"- {l}\n")
        self.actualizar_estado()

    def mostrar_historial(self):
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, "Historial de llamadas atendidas:\n\n")
        for l in self.call_center.ver_historial():
            self.text_area.insert(tk.END, f"- {l}\n")
        self.actualizar_estado()

    def refrescar_todo(self):
        # Refresca todas las vistas para mostrar el estado actualizado
        self.mostrar_en_atencion()
        self.mostrar_pendientes()
        self.mostrar_historial()
        self.actualizar_estado()

# =============================
# PUNTO DE ENTRADA
# =============================

if __name__ == "__main__":
    root = tk.Tk()
    app = CallCenterGUI(root)
    root.mainloop()