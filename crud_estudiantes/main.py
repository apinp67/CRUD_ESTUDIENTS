"""Punto de entrada del programa."""

from controller import EstudianteController


def main():
    aplicacion = EstudianteController()
    aplicacion.ejecutar()


if __name__ == "__main__":
    main()
