'''Diseñe un programa que simule cómo un microprocesador atiende procesos 
en una cola de ejecución. Cada proceso tiene un identificador, un nombre 
y una duración estimada en milisegundos. A medida que el procesador queda 
libre, atiende al siguiente proceso en orden de llegada (FIFO - First In, First Out). 
El sistema debe permitir agregar procesos a la cola, mostrar el proceso en ejecución
y visualizar los procesos pendientes.'''

import time
from collections import deque
from datetime import datetime

# =============================
# MODELO DE DATOS
# =============================

class Proceso:
    # Representa un proceso que será ejecutado por el microprocesador
    def __init__(self, id_proceso, nombre, duracion_ms):
        self.id_proceso = id_proceso              # Identificador único del proceso
        self.nombre = nombre                      # Nombre del proceso
        self.duracion_ms = duracion_ms            # Duración estimada en milisegundos
        self.fecha_creacion = datetime.now()      # Fecha y hora de creación del proceso

    def __str__(self):
        # Representación en texto del proceso
        return (f"{self.fecha_creacion.strftime('%H:%M:%S')} | "
                f"ID: {self.id_proceso} | Nombre: {self.nombre} | Duración: {self.duracion_ms} ms")

# =============================
# LÓGICA DE SIMULACIÓN
# =============================

class Microprocesador:
    # Simula la cola de procesos y su ejecución en el microprocesador
    def __init__(self):
        self.cola = deque()      # Cola de procesos pendientes (FIFO)
        self.historial = []      # Lista de procesos ya ejecutados

    def agregar_proceso(self, proceso):
        # Agrega un proceso a la cola de ejecución
        self.cola.append(proceso)
        return f" Proceso agregado: {proceso}"

    def ejecutar_proceso(self):
        # Ejecuta el siguiente proceso en la cola (si hay alguno)
        if not self.cola:
            return " No hay procesos en la cola."
        proceso = self.cola.popleft()
        print(f"\n Ejecutando proceso: {proceso}")
        time.sleep(proceso.duracion_ms / 1000.0)  # Simula el tiempo de ejecución real
        self.historial.append(proceso)
        return f" Proceso {proceso.id_proceso} terminado."

    def ver_proceso_actual(self):
        # Muestra el proceso que está primero en la cola (el próximo a ejecutar)
        if self.cola:
            return f" Proceso en espera para ejecutar: {self.cola[0]}"
        else:
            return " No hay procesos en la cola."

    def ver_procesos_pendientes(self):
        # Devuelve la lista de procesos pendientes en la cola
        if self.cola:
            return [str(p) for p in self.cola]
        else:
            return [" No hay procesos pendientes."]

    def ver_historial(self):
        # Devuelve la lista de procesos que ya fueron ejecutados
        if self.historial:
            return [str(p) for p in self.historial]
        else:
            return [" Historial vacío."]

# =============================
# INTERFAZ DE CONSOLA
# =============================

def mostrar_menu():
    # Muestra el menú de opciones al usuario
    print("\n=== Menú del Microprocesador ===")
    print("1. Agregar nuevo proceso")
    print("2. Ver proceso actual")
    print("3. Ejecutar siguiente proceso")
    print("4. Ver procesos pendientes")
    print("5. Ver historial de procesos ejecutados")
    print("6. Salir")

def crear_proceso():
    # Solicita los datos de un nuevo proceso al usuario
    try:
        id_proceso = input("ID del proceso: ").strip()
        nombre = input("Nombre del proceso: ").strip()
        duracion = int(input("Duración estimada (ms): ").strip())
        if not id_proceso or not nombre:
            print(" El ID y el nombre no pueden estar vacíos.")
            return None
        if duracion <= 0:
            print(" La duración debe ser un número positivo.")
            return None
        return Proceso(id_proceso, nombre, duracion)
    except ValueError:
        print(" Duración inválida. Debe ser un número entero positivo.")
        return None

# =============================
# FUNCIÓN PRINCIPAL
# =============================

def main():
    # Función principal que ejecuta el simulador del microprocesador
    cpu = Microprocesador()
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción (1-6): ").strip()
        if opcion == '1':
            # Agregar un nuevo proceso a la cola
            proceso = crear_proceso()
            if proceso:
                print(cpu.agregar_proceso(proceso))
        elif opcion == '2':
            # Ver el proceso que está primero en la cola
            print(cpu.ver_proceso_actual())
        elif opcion == '3':
            # Ejecutar el siguiente proceso en la cola
            print(cpu.ejecutar_proceso())
        elif opcion == '4':
            # Ver todos los procesos pendientes en la cola
            print("\n Procesos pendientes:")
            for p in cpu.ver_procesos_pendientes():
                print(f"- {p}")
        elif opcion == '5':
            # Ver el historial de procesos ejecutados
            print("\n Historial de procesos ejecutados:")
            for p in cpu.ver_historial():
                print(f"- {p}")
        elif opcion == '6':
            # Salir del simulador
            print("\n Cerrando simulador de microprocesador.")
            break
        else:
            print(" Opción no válida. Intente nuevamente.")

# =============================
# PUNTO DE ENTRADA
# =============================

if __name__ == "__main__":
    main()