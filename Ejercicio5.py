'''Imagina un servidor de archivos en una red donde varios usuarios 
solicitan acceso a un mismo archivo compartido para su lectura. 
Para evitar conflictos o bloqueos, las solicitudes se atienden en el 
orden en que llegan. Diseña un programa en Python que simule este 
comportamiento utilizando una cola. El programa debe permitir registrar 
solicitudes de acceso (nombre del usuario y archivo solicitado), mostrar 
qué usuario está accediendo al archivo y eliminar la solicitud una vez atendida. 
También debe permitir consultar la lista de solicitudes pendientes.
'''

from collections import deque
from datetime import datetime

# =============================
# MODELO DE DATOS
# =============================

class SolicitudAcceso:
    # Representa una solicitud de acceso a un archivo por parte de un usuario
    def __init__(self, usuario, archivo):
        self.usuario = usuario                        # Nombre del usuario que solicita acceso
        self.archivo = archivo                        # Nombre del archivo solicitado
        self.fecha_solicitud = datetime.now()         # Fecha y hora de la solicitud

    def __str__(self):
        # Representación en texto de la solicitud
        return (f"{self.fecha_solicitud.strftime('%Y-%m-%d %H:%M:%S')} | "
                f"Usuario: {self.usuario} | Archivo: {self.archivo}")

# =============================
# LÓGICA DE NEGOCIO
# =============================

class ServidorArchivos:
    # Simula la gestión de solicitudes de acceso a archivos en un servidor
    def __init__(self):
        self.cola_solicitudes = deque()   # Cola de solicitudes pendientes
        self.historial = []               # Historial de solicitudes atendidas

    def registrar_solicitud(self, solicitud):
        # Agrega una nueva solicitud a la cola
        self.cola_solicitudes.append(solicitud)
        return f"Solicitud registrada: {solicitud}"

    def atender_solicitud(self):
        # Atiende la siguiente solicitud en la cola (FIFO)
        if not self.cola_solicitudes:
            return " No hay solicitudes pendientes."
        solicitud = self.cola_solicitudes.popleft()
        self.historial.append(solicitud)
        return f" Atendiendo solicitud: {solicitud}"

    def ver_solicitud_actual(self):
        # Muestra la solicitud que está siendo atendida actualmente (primera en la cola)
        if self.cola_solicitudes:
            return f" Solicitud en proceso: {self.cola_solicitudes[0]}"
        else:
            return " No hay solicitudes en proceso."

    def ver_solicitudes_pendientes(self):
        # Devuelve la lista de solicitudes pendientes en la cola
        if self.cola_solicitudes:
            return [str(s) for s in self.cola_solicitudes]
        else:
            return [" No hay solicitudes pendientes."]

    def ver_historial(self):
        # Devuelve el historial de solicitudes ya atendidas
        if self.historial:
            return [str(s) for s in self.historial]
        else:
            return [" Historial vacío."]

# =============================
# INTERFAZ DE CONSOLA
# =============================

def mostrar_menu():
    # Muestra el menú de opciones al usuario
    print("\n=== Menú del Servidor de Archivos ===")
    print("1. Registrar nueva solicitud de acceso")
    print("2. Ver solicitud en proceso")
    print("3. Atender siguiente solicitud")
    print("4. Ver solicitudes pendientes")
    print("5. Ver historial de accesos atendidos")
    print("6. Salir")

def solicitar_datos():
    # Solicita los datos necesarios para registrar una solicitud de acceso
    try:
        usuario = input("Ingrese el nombre del usuario: ").strip()
        archivo = input("Ingrese el nombre del archivo solicitado: ").strip()
        if not usuario or not archivo:
            print(" Los campos no pueden estar vacíos.")
            return None
        return SolicitudAcceso(usuario, archivo)
    except Exception as e:
        print(f" Error inesperado: {e}")
        return None

# =============================
# FUNCIÓN PRINCIPAL
# =============================

def main():
    # Función principal que ejecuta el simulador del servidor de archivos
    servidor = ServidorArchivos()
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción (1-6): ").strip()

        if opcion == '1':
            # Registrar una nueva solicitud de acceso
            solicitud = solicitar_datos()
            if solicitud:
                print(servidor.registrar_solicitud(solicitud))

        elif opcion == '2':
            # Ver la solicitud que está siendo atendida actualmente
            print(servidor.ver_solicitud_actual())

        elif opcion == '3':
            # Atender la siguiente solicitud en la cola
            print(servidor.atender_solicitud())

        elif opcion == '4':
            # Mostrar todas las solicitudes pendientes
            print("\n Solicitudes pendientes:")
            for solicitud in servidor.ver_solicitudes_pendientes():
                print(f"- {solicitud}")

        elif opcion == '5':
            # Mostrar el historial de solicitudes atendidas
            print("\n Historial de accesos atendidos:")
            for solicitud in servidor.ver_historial():
                print(f"- {solicitud}")

        elif opcion == '6':
            # Salir del simulador
            print("\n Cerrando el servidor de archivos. ¡Hasta pronto!")
            break

        else:
            print(" Opción no válida. Intente nuevamente.")

# =============================
# PUNTO DE ENTRADA
# =============================

if __name__ == "__main__":
    main()