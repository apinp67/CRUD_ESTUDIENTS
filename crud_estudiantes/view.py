"""
VISTA (V de MVC)
================
Se encarga de mostrar menús y pedir datos por consola.
"""


class EstudianteView:
    def mostrar_menu(self):
        print("\n" + "=" * 55)
        print("          SISTEMA DE GESTIÓN DE ESTUDIANTES")
        print("=" * 55)
        print("1. Registrar estudiante")
        print("2. Listar estudiantes")
        print("3. Buscar estudiante por ID")
        print("4. Buscar estudiante por cédula")
        print("5. Buscar estudiante por nombre o apellido")
        print("6. Actualizar estudiante")
        print("7. Eliminar estudiante")
        print("8. Listar estudiantes por carrera")
        print("9. Mostrar estudiantes aprobados")
        print("10. Mostrar estudiantes reprobados")
        print("0. Salir")
        print("=" * 55)

    def pedir_opcion(self):
        return input("Seleccione una opción: ").strip()

    def pedir_datos_estudiante(self):
        print("\n--- Datos del estudiante ---")
        cedula = input("Cédula: ").strip()
        nombres = input("Nombres: ").strip()
        apellidos = input("Apellidos: ").strip()
        carrera = input("Carrera: ").strip()
        semestre = input("Semestre (1-10): ").strip()
        promedio = input("Promedio (0-10): ").strip()
        return cedula, nombres, apellidos, carrera, semestre, promedio

    def pedir_id(self, mensaje="ID del estudiante: "):
        valor = input(mensaje).strip()
        return int(valor) if valor.isdigit() else None

    def pedir_cedula(self):
        return input("Cédula del estudiante: ").strip()

    def pedir_texto_busqueda(self):
        return input("Ingrese nombre o apellido: ").strip()

    def pedir_carrera(self):
        return input("Ingrese la carrera: ").strip()

    def pedir_campo_opcional(self, etiqueta, actual):
        nuevo = input(f"{etiqueta} [{actual}] (Enter para no cambiar): ").strip()
        return nuevo if nuevo else None

    def mostrar_mensaje(self, mensaje):
        print(f"\n>> {mensaje}")

    def mostrar_error(self, mensaje):
        print(f"\n[ERROR] {mensaje}")

    def mostrar_estudiante(self, estudiante):
        if estudiante:
            print("\n--- Estudiante encontrado ---")
            print(estudiante)
        else:
            print("\nEstudiante no encontrado.")

    def mostrar_lista_estudiantes(self, estudiantes, titulo="Lista de estudiantes"):
        print(f"\n--- {titulo} ---")
        if not estudiantes:
            print("No hay estudiantes para mostrar.")
            return

        for estudiante in estudiantes:
            print(estudiante)
        print(f"Total: {len(estudiantes)} estudiante(s)")

    def confirmar(self, mensaje):
        respuesta = input(f"{mensaje} (s/n): ").strip().lower()
        return respuesta == "s"
