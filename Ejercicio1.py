'''Simule el funcionamiento de una cola de impresión en una oficina donde varios empleados
envían documentos para ser impresos. Cada documento tiene un nombre, el usuario que lo
envió y el número de páginas. El sistema debe permitir agregar documentos a la cola,
procesarlos en orden de llegada y mostrar cuál es el documento que se está imprimiendo
actualmente. Analice con los estudiantes cómo se evita el desorden en el uso compartido de
un recurso limitado.'''

from collections import deque
from datetime import datetime

# =============================
# MODELO DE DATOS
# =============================

class Documento:
    # Representa un documento a imprimir
    def __init__(self, nombre, usuario, paginas):
        self.nombre = nombre              # Nombre del documento
        self.usuario = usuario            # Usuario que envió el documento
        self.paginas = paginas            # Número de páginas
        self.fecha_envio = datetime.now() # Fecha y hora de envío

    def __str__(self):
        # Representación en texto del documento
        return (f"{self.fecha_envio.strftime('%Y-%m-%d %H:%M:%S')} | "
                f"Documento: {self.nombre} | Usuario: {self.usuario} | Páginas: {self.paginas}")

# =============================
# LÓGICA DE NEGOCIO
# =============================

class ColaImpresion:
    # Maneja la cola de impresión y el historial
    def __init__(self):
        self.cola = deque()    # Cola de documentos por imprimir
        self.historial = []    # Historial de documentos impresos

    def agregar_documento(self, documento):
        # Agrega un documento a la cola
        self.cola.append(documento)
        return f"Documento agregado a la cola: {documento}"

    def procesar_siguiente(self):
        # Imprime el siguiente documento en la cola
        if not self.cola:
            return "No hay documentos en la cola para imprimir."
        documento = self.cola.popleft()
        self.historial.append(documento)
        return f"Imprimiendo... {documento}"

    def ver_documento_actual(self):
        # Muestra el documento que está primero en la cola
        if self.cola:
            return f"Documento en espera: {self.cola[0]}"
        else:
            return "No hay documentos en proceso."

    def ver_cola(self):
        # Devuelve la lista de documentos en la cola
        if self.cola:
            # str() se usa para convertir cada documento a su representación en texto
            return [str(doc) for doc in self.cola]
        else:
            return ["La cola está vacía."]

    def ver_historial(self):
        # Devuelve la lista de documentos ya impresos
        if self.historial:
            return [str(doc) for doc in self.historial]
        else:
            return ["No hay historial aún."]

# =============================
# INTERFAZ DE CONSOLA
# =============================

def mostrar_menu():
    # Muestra el menú de opciones al usuario con un encabezado decorativo
    print("\n" + "="*45)
    print("SISTEMA DE COLA DE IMPRESIÓN".center(45))
    print("="*45)
    print("1. Agregar documento")
    print("2. Ver documento en espera")
    print("3. Imprimir siguiente documento")
    print("4. Ver cola de impresión")
    print("5. Ver historial de impresiones")
    print("6. Salir")

def solicitar_documento():
    # Solicita los datos de un documento al usuario
    try:
        nombre = input("Ingrese el nombre del documento: ").strip()
        usuario = input("Ingrese el nombre del usuario: ").strip()
        paginas = int(input("Ingrese el número de páginas: ").strip())
        if not nombre or not usuario:
            print("El nombre del documento y el usuario no pueden estar vacíos.")
            return None
        if paginas <= 0:
            print("El número de páginas debe ser mayor que cero.")
            return None
        return Documento(nombre, usuario, paginas)
    except ValueError:
        print("Error: Ingrese un número entero válido para las páginas.")
        return None
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")
        return None

# =============================
# FUNCIÓN PRINCIPAL
# =============================

def main():
    # Función principal del programa
    cola_impresion = ColaImpresion()
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción (1-6): ").strip()
        match opcion:
            case '1':
                documento = solicitar_documento()
                if documento:
                    print(cola_impresion.agregar_documento(documento))
            case '2':
                print(cola_impresion.ver_documento_actual())
            case '3':
                print(cola_impresion.procesar_siguiente())
            case '4':
                print("\nCola de impresión:")
                for doc in cola_impresion.ver_cola():
                    print(f"- {doc}")
            case '5':
                print("\nHistorial de documentos impresos:")
                for doc in cola_impresion.ver_historial():
                    print(f"- {doc}")
            case '6':
                print("\nCerrando el sistema de impresión. ¡Hasta pronto!")
                break
            case _:
                print("Opción no válida. Intente nuevamente.")

# =============================
# PUNTO DE ENTRADA
# =============================

if __name__ == "__main__":
    main()
