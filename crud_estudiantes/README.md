# CRUD de Estudiantes - MVC

Proyecto sencillo en Python para gestionar estudiantes usando Programación Orientada a Objetos y el patrón MVC.

## Archivos
- `main.py`: inicia el programa.
- `controller.py`: conecta la vista con el modelo.
- `view.py`: muestra el menú y solicita datos.
- `model.py`: contiene la clase Estudiante, validaciones, CRUD y manejo del JSON.
- `estudiantes.json`: guarda los estudiantes para conservarlos aunque se cierre el programa.

## Funciones principales
- Registrar estudiantes.
- Listar estudiantes.
- Buscar por ID, cédula, nombre o apellido.
- Actualizar estudiantes.
- Eliminar estudiantes.
- Filtrar por carrera.
- Mostrar aprobados y reprobados.

## Colecciones usadas
- `list`: lista principal de estudiantes.
- `dict`: índice de estudiantes por ID.
- `set`: control de cédulas repetidas.
- `tuple`: resultados de consultas.

## Ejecutar
Desde la carpeta del proyecto:

```bash
python main.py
```

Los cambios se guardan automáticamente en `estudiantes.json`.
