'''Implemente un sistema de turnos en una farmacia, donde los pacientes son 
atendidos en el orden en que llegan. Cada paciente tiene un nombre y un tipo 
de servicio (compra, consulta, receta). El sistema debe permitir registrar 
nuevos pacientes, atender al siguiente en la fila y mostrar los turnos pendientes.'''

from collections import deque
from datetime import datetime
import time
import random  # Agrega esto al inicio junto con los otros imports

# =============================
# MODELO DE DATOS
# =============================

class Paciente:
    # Representa a un paciente que solicita un turno en la farmacia
    def __init__(self, nombre, servicio):
        self.nombre = nombre                  # Nombre del paciente
        self.servicio = servicio              # Tipo de servicio solicitado
        self.hora_turno = datetime.now()      # Hora en que se registró el turno

    def __str__(self):
        # Representación en texto del paciente y su turno
        return f"{self.hora_turno.strftime('%H:%M:%S')} | Nombre: {self.nombre} | Servicio: {self.servicio}"

# =============================
# LÓGICA DE NEGOCIO
# =============================

class Farmacia:
    # Maneja la cola de turnos, la atención y el historial de pacientes
    def __init__(self):
        self.cola_turnos = deque()    # Cola de pacientes esperando turno
        self.en_atencion = None       # Paciente que está siendo atendido
        self.historial = []           # Lista de pacientes ya atendidos

    def registrar_paciente(self, paciente):
        # Agrega un paciente a la cola de turnos
        self.cola_turnos.append(paciente)
        return f" Turno registrado: {paciente}"

    def atender_siguiente(self):
        # Atiende al siguiente paciente en la cola
        if self.en_atencion:
            return f"Ya hay un paciente en atención: {self.en_atencion.nombre} ({self.en_atencion.servicio})"
        if not self.cola_turnos:
            return " No hay pacientes en espera."
        self.en_atencion = self.cola_turnos.popleft()
        print(f"\n Atendiendo a: {self.en_atencion}")
        tiempo = random.randint(7, 15)  # Tiempo aleatorio entre 7 y 15 segundos
        time.sleep(tiempo)
        self.historial.append(self.en_atencion)
        print(f" Atención finalizada para {self.en_atencion.nombre}")
        self.en_atencion = None
        return ""

    def ver_turnos_pendientes(self):
        # Devuelve la lista de pacientes en espera
        if self.cola_turnos:
            return [str(p) for p in self.cola_turnos]
        return [" No hay turnos pendientes."]

    def ver_historial(self):
        # Devuelve la lista de pacientes ya atendidos
        if self.historial:
            return [str(p) for p in self.historial]
        return [" Aún no se ha atendido ningún paciente."]

# =============================
# INTERFAZ DE CONSOLA
# =============================

def mostrar_menu():
    # Muestra el menú de opciones al usuario
    print("\n=== SISTEMA DE TURNOS - FARMACIA ===")
    print("1. Registrar nuevo paciente")
    print("2. Atender siguiente paciente")
    print("3. Ver turnos pendientes")
    print("4. Ver historial de atención")
    print("5. Salir")

def elegir_servicio():
    # Permite al usuario elegir el tipo de servicio para el paciente
    servicios = {
        '1': 'Compra',
        '2': 'Consulta',
        '3': 'Receta'
    }
    print("\nSeleccione el tipo de servicio:")
    for clave, nombre in servicios.items():
        print(f"{clave}. {nombre}")
    opcion = input("Opción (1-3): ").strip()
    return servicios.get(opcion, None)

def crear_paciente():
    # Solicita los datos del paciente y crea un objeto Paciente
    nombre = input("Nombre del paciente: ").strip()
    if not nombre:
        print(" El nombre no puede estar vacío.")
        return None
    servicio = elegir_servicio()
    if not servicio:
        print(" Opción de servicio inválida.")
        return None
    return Paciente(nombre, servicio)

# =============================
# FUNCIÓN PRINCIPAL
# =============================

def main():
    # Función principal que ejecuta el sistema de turnos
    farmacia = Farmacia()
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción (1-5): ").strip()
        if opcion == '1':
            paciente = crear_paciente()
            if paciente:
                print(farmacia.registrar_paciente(paciente))
        elif opcion == '2':
            resultado = farmacia.atender_siguiente()
            if resultado:
                print(resultado)
        elif opcion == '3':
            print("\n Turnos pendientes:")
            for p in farmacia.ver_turnos_pendientes():
                print(f"- {p}")
        elif opcion == '4':
            print("\n Historial de pacientes atendidos:")
            for p in farmacia.ver_historial():
                print(f"- {p}")
        elif opcion == '5':
            print("\n Cerrando sistema de turnos de farmacia.")
            break
        else:
            print(" Opción inválida. Intente de nuevo.")

# =============================
# PUNTO DE ENTRADA
# =============================

if __name__ == "__main__":
    main()


