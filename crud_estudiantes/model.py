"""
MODELO (M de MVC)
=================
Contiene la clase Estudiante y el repositorio EstudianteRepository.

Colecciones utilizadas:
1. list  -> almacena los estudiantes.
2. dict  -> permite buscar rápido por ID.
3. set   -> evita cédulas duplicadas.
4. tuple -> devuelve resultados de consulta sin modificarlos directamente.

Persistencia:
Los datos se guardan en estudiantes.json para que no se pierdan al cerrar el programa.
"""

import json
import os


class CedulaDuplicadaError(Exception):
    pass


class DatosInvalidosError(Exception):
    pass


class Estudiante:
    def __init__(self, id_estudiante, cedula, nombres, apellidos,
                 carrera, semestre, promedio):
        self.id = id_estudiante
        self.cedula = cedula
        self.nombres = nombres
        self.apellidos = apellidos
        self.carrera = carrera
        self.semestre = semestre
        self.promedio = promedio

    def actualizar(self, cedula=None, nombres=None, apellidos=None,
                   carrera=None, semestre=None, promedio=None):
        if cedula is not None:
            self.cedula = cedula
        if nombres is not None:
            self.nombres = nombres
        if apellidos is not None:
            self.apellidos = apellidos
        if carrera is not None:
            self.carrera = carrera
        if semestre is not None:
            self.semestre = semestre
        if promedio is not None:
            self.promedio = promedio

    def estado(self):
        return "APROBADO" if self.promedio >= 7 else "REPROBADO"

    def a_tupla(self):
        return (
            self.id, self.cedula, self.nombres, self.apellidos,
            self.carrera, self.semestre, self.promedio, self.estado()
        )

    def a_diccionario(self):
        return {
            "id": self.id,
            "cedula": self.cedula,
            "nombres": self.nombres,
            "apellidos": self.apellidos,
            "carrera": self.carrera,
            "semestre": self.semestre,
            "promedio": self.promedio
        }

    def __str__(self):
        return (
            f"ID: {self.id} | Cédula: {self.cedula} | "
            f"{self.nombres} {self.apellidos} | Carrera: {self.carrera} | "
            f"Semestre: {self.semestre} | Promedio: {self.promedio:.2f} | "
            f"Estado: {self.estado()}"
        )


class EstudianteRepository:
    def __init__(self, archivo_json=None):
        self._estudiantes = []
        self._indice_por_id = {}
        self._cedulas_registradas = set()
        self._siguiente_id = 1

        if archivo_json is None:
            carpeta_actual = os.path.dirname(os.path.abspath(__file__))
            archivo_json = os.path.join(carpeta_actual, "estudiantes.json")

        self._archivo_json = archivo_json
        self._cargar_datos()

    # ---------------- Persistencia JSON ----------------
    def _cargar_datos(self):
        if not os.path.exists(self._archivo_json):
            self._guardar_datos()
            return

        try:
            with open(self._archivo_json, "r", encoding="utf-8") as archivo:
                datos = json.load(archivo)
        except (json.JSONDecodeError, OSError):
            datos = []

        if not isinstance(datos, list):
            datos = []

        for item in datos:
            try:
                estudiante = Estudiante(
                    int(item["id"]),
                    str(item["cedula"]),
                    str(item["nombres"]),
                    str(item["apellidos"]),
                    str(item["carrera"]),
                    int(item["semestre"]),
                    float(item["promedio"])
                )
            except (KeyError, TypeError, ValueError):
                continue

            self._estudiantes.append(estudiante)
            self._indice_por_id[estudiante.id] = estudiante
            self._cedulas_registradas.add(estudiante.cedula)

        if self._estudiantes:
            self._siguiente_id = max(e.id for e in self._estudiantes) + 1

    def _guardar_datos(self):
        datos = [estudiante.a_diccionario() for estudiante in self._estudiantes]
        with open(self._archivo_json, "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, indent=4, ensure_ascii=False)

    # ---------------- Validaciones ----------------
    def _validar_texto(self, valor, campo):
        if not valor or not valor.strip():
            raise DatosInvalidosError(f"El campo {campo} no puede estar vacío.")
        return valor.strip()

    def _validar_cedula(self, cedula):
        cedula = cedula.strip()
        if not cedula.isdigit() or len(cedula) != 10:
            raise DatosInvalidosError("La cédula debe contener exactamente 10 números.")
        return cedula

    def _validar_semestre(self, semestre):
        try:
            semestre = int(semestre)
        except (TypeError, ValueError):
            raise DatosInvalidosError("El semestre debe ser un número entero.")
        if semestre < 1 or semestre > 10:
            raise DatosInvalidosError("El semestre debe estar entre 1 y 10.")
        return semestre

    def _validar_promedio(self, promedio):
        try:
            promedio = float(promedio)
        except (TypeError, ValueError):
            raise DatosInvalidosError("El promedio debe ser un número.")
        if promedio < 0 or promedio > 10:
            raise DatosInvalidosError("El promedio debe estar entre 0 y 10.")
        return promedio

    # ---------------- CREATE ----------------
    def crear(self, cedula, nombres, apellidos, carrera, semestre, promedio):
        cedula = self._validar_cedula(cedula)
        nombres = self._validar_texto(nombres, "nombres")
        apellidos = self._validar_texto(apellidos, "apellidos")
        carrera = self._validar_texto(carrera, "carrera")
        semestre = self._validar_semestre(semestre)
        promedio = self._validar_promedio(promedio)

        if cedula in self._cedulas_registradas:
            raise CedulaDuplicadaError(f"La cédula '{cedula}' ya está registrada.")

        estudiante = Estudiante(
            self._siguiente_id, cedula, nombres, apellidos,
            carrera, semestre, promedio
        )

        self._estudiantes.append(estudiante)
        self._indice_por_id[estudiante.id] = estudiante
        self._cedulas_registradas.add(cedula)
        self._siguiente_id += 1
        self._guardar_datos()
        return estudiante

    # ---------------- READ ----------------
    def leer_todos(self):
        return tuple(self._estudiantes)

    def leer_por_id(self, id_estudiante):
        return self._indice_por_id.get(id_estudiante)

    def buscar_por_cedula(self, cedula):
        cedula = cedula.strip()
        for estudiante in self._estudiantes:
            if estudiante.cedula == cedula:
                return estudiante
        return None

    def buscar_por_nombre(self, texto):
        texto = texto.strip().lower()
        return tuple(
            e for e in self._estudiantes
            if texto in e.nombres.lower() or texto in e.apellidos.lower()
        )

    def listar_por_carrera(self, carrera):
        carrera = carrera.strip().lower()
        return tuple(
            e for e in self._estudiantes
            if carrera in e.carrera.lower()
        )

    def listar_por_estado(self, aprobado=True):
        return tuple(
            e for e in self._estudiantes
            if (e.promedio >= 7) == aprobado
        )

    # ---------------- UPDATE ----------------
    def actualizar(self, id_estudiante, **campos):
        estudiante = self._indice_por_id.get(id_estudiante)
        if estudiante is None:
            return False

        if "cedula" in campos:
            nueva_cedula = self._validar_cedula(campos["cedula"])
            if nueva_cedula != estudiante.cedula:
                if nueva_cedula in self._cedulas_registradas:
                    raise CedulaDuplicadaError(
                        f"La cédula '{nueva_cedula}' ya está registrada."
                    )
                self._cedulas_registradas.discard(estudiante.cedula)
                self._cedulas_registradas.add(nueva_cedula)
            campos["cedula"] = nueva_cedula

        if "nombres" in campos:
            campos["nombres"] = self._validar_texto(campos["nombres"], "nombres")
        if "apellidos" in campos:
            campos["apellidos"] = self._validar_texto(campos["apellidos"], "apellidos")
        if "carrera" in campos:
            campos["carrera"] = self._validar_texto(campos["carrera"], "carrera")
        if "semestre" in campos:
            campos["semestre"] = self._validar_semestre(campos["semestre"])
        if "promedio" in campos:
            campos["promedio"] = self._validar_promedio(campos["promedio"])

        estudiante.actualizar(**campos)
        self._guardar_datos()
        return True

    # ---------------- DELETE ----------------
    def eliminar(self, id_estudiante):
        estudiante = self._indice_por_id.pop(id_estudiante, None)
        if estudiante is None:
            return False

        self._estudiantes.remove(estudiante)
        self._cedulas_registradas.discard(estudiante.cedula)
        self._guardar_datos()
        return True

    def total_estudiantes(self):
        return len(self._estudiantes)
