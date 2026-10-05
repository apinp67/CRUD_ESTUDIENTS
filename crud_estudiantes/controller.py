"""
CONTROLADOR (C de MVC)
======================
Conecta la Vista con el Modelo y organiza las acciones del programa.
"""

from model import EstudianteRepository, CedulaDuplicadaError, DatosInvalidosError
from view import EstudianteView


class EstudianteController:
    def __init__(self):
        self.repositorio = EstudianteRepository()
        self.vista = EstudianteView()

    def ejecutar(self):
        opciones = {
            "1": self.crear_estudiante,
            "2": self.listar_estudiantes,
            "3": self.buscar_por_id,
            "4": self.buscar_por_cedula,
            "5": self.buscar_por_nombre,
            "6": self.actualizar_estudiante,
            "7": self.eliminar_estudiante,
            "8": self.listar_por_carrera,
            "9": self.mostrar_aprobados,
            "10": self.mostrar_reprobados,
        }

        while True:
            self.vista.mostrar_menu()
            opcion = self.vista.pedir_opcion()

            if opcion == "0":
                self.vista.mostrar_mensaje("Programa finalizado.")
                break

            accion = opciones.get(opcion)
            if accion is None:
                self.vista.mostrar_error("Opción no válida.")
                continue

            try:
                accion()
            except (CedulaDuplicadaError, DatosInvalidosError) as error:
                self.vista.mostrar_error(str(error))
            except Exception as error:
                self.vista.mostrar_error(f"Ocurrió un error inesperado: {error}")

    def crear_estudiante(self):
        datos = self.vista.pedir_datos_estudiante()
        estudiante = self.repositorio.crear(*datos)
        self.vista.mostrar_mensaje(
            f"Estudiante registrado correctamente. ID asignado: {estudiante.id}"
        )

    def listar_estudiantes(self):
        estudiantes = self.repositorio.leer_todos()
        self.vista.mostrar_lista_estudiantes(estudiantes)

    def buscar_por_id(self):
        id_estudiante = self.vista.pedir_id()
        if id_estudiante is None:
            self.vista.mostrar_error("El ID debe ser numérico.")
            return
        self.vista.mostrar_estudiante(
            self.repositorio.leer_por_id(id_estudiante)
        )

    def buscar_por_cedula(self):
        cedula = self.vista.pedir_cedula()
        self.vista.mostrar_estudiante(
            self.repositorio.buscar_por_cedula(cedula)
        )

    def buscar_por_nombre(self):
        texto = self.vista.pedir_texto_busqueda()
        resultados = self.repositorio.buscar_por_nombre(texto)
        self.vista.mostrar_lista_estudiantes(
            resultados, "Resultados de la búsqueda"
        )

    def actualizar_estudiante(self):
        id_estudiante = self.vista.pedir_id()
        if id_estudiante is None:
            self.vista.mostrar_error("El ID debe ser numérico.")
            return

        estudiante = self.repositorio.leer_por_id(id_estudiante)
        if estudiante is None:
            self.vista.mostrar_error("Estudiante no encontrado.")
            return

        print("\nDeje un campo vacío si no desea cambiarlo.")
        cedula = self.vista.pedir_campo_opcional("Cédula", estudiante.cedula)
        nombres = self.vista.pedir_campo_opcional("Nombres", estudiante.nombres)
        apellidos = self.vista.pedir_campo_opcional("Apellidos", estudiante.apellidos)
        carrera = self.vista.pedir_campo_opcional("Carrera", estudiante.carrera)
        semestre = self.vista.pedir_campo_opcional("Semestre", estudiante.semestre)
        promedio = self.vista.pedir_campo_opcional("Promedio", f"{estudiante.promedio:.2f}")

        campos = {
            "cedula": cedula,
            "nombres": nombres,
            "apellidos": apellidos,
            "carrera": carrera,
            "semestre": semestre,
            "promedio": promedio,
        }
        campos = {clave: valor for clave, valor in campos.items() if valor is not None}

        if not campos:
            self.vista.mostrar_mensaje("No se realizaron cambios.")
            return

        if self.repositorio.actualizar(id_estudiante, **campos):
            self.vista.mostrar_mensaje("Estudiante actualizado correctamente.")

    def eliminar_estudiante(self):
        id_estudiante = self.vista.pedir_id()
        if id_estudiante is None:
            self.vista.mostrar_error("El ID debe ser numérico.")
            return

        estudiante = self.repositorio.leer_por_id(id_estudiante)
        if estudiante is None:
            self.vista.mostrar_error("Estudiante no encontrado.")
            return

        nombre = f"{estudiante.nombres} {estudiante.apellidos}"
        if self.vista.confirmar(f"¿Seguro que desea eliminar a {nombre}?"):
            self.repositorio.eliminar(id_estudiante)
            self.vista.mostrar_mensaje("Estudiante eliminado correctamente.")
        else:
            self.vista.mostrar_mensaje("Operación cancelada.")

    def listar_por_carrera(self):
        carrera = self.vista.pedir_carrera()
        resultados = self.repositorio.listar_por_carrera(carrera)
        self.vista.mostrar_lista_estudiantes(
            resultados, f"Estudiantes de la carrera: {carrera}"
        )

    def mostrar_aprobados(self):
        resultados = self.repositorio.listar_por_estado(True)
        self.vista.mostrar_lista_estudiantes(resultados, "Estudiantes aprobados")

    def mostrar_reprobados(self):
        resultados = self.repositorio.listar_por_estado(False)
        self.vista.mostrar_lista_estudiantes(resultados, "Estudiantes reprobados")
