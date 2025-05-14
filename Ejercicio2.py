'''Cree un sistema que simule la atención de llamadas en un Call Center. 
Cada llamada debe ingresar a una cola con datos como el nombre del cliente 
y el motivo de la llamada. A medida que los agentes estén disponibles, 
se debe atender al siguiente cliente en orden de llegada.'''

import time # Simula el tiempo de atención
import threading # Permite el uso de hilos
from collections import deque # Estructura de datos para la cola
from datetime import datetime # Maneja la fecha y hora

# =============================
# MODELO DE DATOS
# =============================

class Llamada:
    # Representa una llamada entrante al call center
    def __init__(self, nombre_cliente, motivo):
        self.nombre_cliente = nombre_cliente  # Nombre del cliente que llama
        self.motivo = motivo                  # Motivo de la llamada
        self.hora_entrada = datetime.now()    # Hora en que entra la llamada
        self.hora_salida = None               # Hora en que termina la llamada

    def __str__(self):
        # Representación en texto de la llamada
        texto = (f"{self.hora_entrada.strftime('%H:%M:%S')} | Cliente: {self.nombre_cliente} | "
                 f"Motivo: {self.motivo}")
        if self.hora_salida:
            texto += f" | Terminada: {self.hora_salida.strftime('%H:%M:%S')}"
        return texto

# =============================
# LÓGICA DE NEGOCIO
# =============================

class CallCenter:
    # Simula la gestión de llamadas y agentes en el call center
    def __init__(self, agentes_disponibles=2):
        self.cola_llamadas = deque()      # Cola de llamadas en espera
        self.en_atencion = []             # Llamadas que están siendo atendidas
        self.historial = []               # Llamadas ya atendidas
        self.lock = threading.Lock()      # Bloqueo para acceso seguro entre hilos
        self.agentes_disponibles = agentes_disponibles  # Número de agentes disponibles
        self.ocupados = 0                 # Número de agentes ocupados

    def agregar_llamada(self, llamada):
        # Agrega una llamada a la cola de espera
        self.cola_llamadas.append(llamada)
        return f" Llamada registrada: {llamada}"

    def atender_llamada(self):
        # Atiende la siguiente llamada si hay agentes libres
        if self.ocupados >= self.agentes_disponibles:
            return " Todos los agentes están ocupados. Espere un momento..."
        if not self.cola_llamadas:
            return " No hay llamadas en espera."
        # Toma la siguiente llamada y la atiende en un hilo aparte
        llamada = self.cola_llamadas.popleft()
        self.ocupados += 1
        hilo = threading.Thread(target=self._procesar_llamada, args=(llamada,))
        hilo.start()
        return f" Atendiendo llamada de {llamada.nombre_cliente}..."

    def _procesar_llamada(self, llamada):
        # Simula el proceso de atención de una llamada
        with self.lock:
            self.en_atencion.append(llamada)
            print(f"\n Llamada en curso: {llamada}")
        # Simula una duración aleatoria entre 8 y 15 segundos
        tiempo = 8 + (hash(llamada.nombre_cliente) % 8)  # 8 + 0..7 = 8..15
        time.sleep(tiempo)
        with self.lock:
            self.en_atencion.remove(llamada)
            llamada.hora_salida = datetime.now()  # Guardar hora de finalización
            self.historial.append(llamada)
            self.ocupados -= 1
            print(f" Llamada finalizada con {llamada.nombre_cliente} ({llamada.motivo}) a las {llamada.hora_salida.strftime('%H:%M:%S')}.")

    def ver_llamada_actual(self):
        # Devuelve las llamadas que están siendo atendidas actualmente
        if self.en_atencion:
            return [str(llamada) for llamada in self.en_atencion]
        else:
            return [" No hay llamadas siendo atendidas en este momento."]

    def ver_llamadas_pendientes(self):
        # Devuelve las llamadas que están en espera
        if self.cola_llamadas:
            return [str(llamada) for llamada in self.cola_llamadas]
        else:
            return [" No hay llamadas pendientes."]

    def ver_historial(self):
        # Devuelve el historial de llamadas ya atendidas
        if self.historial:
            return [str(llamada) for llamada in self.historial]
        else:
            return [" Aún no se han atendido llamadas."]

# =============================
# INTERFAZ DE CONSOLA
# =============================

def mostrar_menu():
    # Muestra el menú de opciones al usuario
    print("\n=== MENÚ CALL CENTER ===")
    print("1. Registrar nueva llamada")
    print("2. Atender siguiente llamada")
    print("3. Ver llamadas en atención")
    print("4. Ver llamadas pendientes")
    print("5. Ver historial de llamadas")
    print("6. Salir")

def crear_llamada():
    # Solicita los datos de una llamada al usuario
    nombre = input("Nombre del cliente: ").strip()
    if not nombre:
        print("El nombre es obligatorio.")
        return None

    # Opciones de motivo
    motivos = [
        "Consulta de saldo",
        "Problema técnico",
        "Información de productos",
        "Otro"
    ]
    print("Seleccione el motivo de la llamada:")
    for i, motivo in enumerate(motivos, 1):
        print(f"{i}. {motivo}")
    try:
        opcion = int(input("Ingrese el número de la opción: ").strip())
        if opcion < 1 or opcion > len(motivos):
            print("Opción inválida.")
            return None
        if motivos[opcion - 1] == "Otro":
            motivo = input("Escriba el motivo de la llamada: ").strip()
            if not motivo:
                print("Debe ingresar un motivo.")
                return None
        else:
            motivo = motivos[opcion - 1]
    except ValueError:
        print("Debe ingresar un número válido.")
        return None

    return Llamada(nombre, motivo)

# =============================
# FUNCIÓN PRINCIPAL
# =============================

def main():
    # Función principal del programa
    call_center = CallCenter(agentes_disponibles=2)
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción (1-6): ").strip()
        if opcion == '1':
            llamada = crear_llamada()
            if llamada:
                print(call_center.agregar_llamada(llamada))
        elif opcion == '2':
            print(call_center.atender_llamada())
        elif opcion == '3':
            print("\n Llamadas en atención:")
            for l in call_center.ver_llamada_actual():
                print(f"- {l}")
        elif opcion == '4':
            print("\n Llamadas pendientes:")
            for l in call_center.ver_llamadas_pendientes():
                print(f"- {l}")
        elif opcion == '5':
            print("\n Historial de llamadas atendidas:")
            for l in call_center.ver_historial():
                print(f"- {l}")
        elif opcion == '6':
            print("\n Finalizando simulador de Call Center.")
            break
        else:
            print(" Opción inválida. Intente de nuevo.")

# =============================
# PUNTO DE ENTRADA
# =============================

if __name__ == "__main__":
    main()


