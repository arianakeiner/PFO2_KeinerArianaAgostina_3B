# PFO 2 - Sistema de Gestión de Tareas con API y Base de Datos

## Descripción
Este proyecto implementa una API REST con Flask para un sistema simple de gestión de tareas.
El servidor permite registrar usuarios, iniciar sesión y acceder a una pantalla HTML de bienvenida en "tareas".
Además, se agregan endpoints simples para crear, listar y eliminar tareas desde un cliente de consola.

El proyecto utiliza SQLite para la persistencia de datos y Werkzeug para guardar contraseñas hasheadas, evitando almacenarlas en texto plano.

## Estructura del proyecto

```txt
pfo2_sistema_tareas/
├── servidor.py
├── cliente.py
├── README.md
```

## Requisitos

- Python 3 instalado.
- pip instalado.

## Instalación

1. Crear y activar un entorno virtual:

```bash
python -m venv venv
```

En Windows:

```bash
venv\Scripts\activate
```

En macOS/Linux:

```bash
source venv/bin/activate
```

2. Instalar dependencias:

```bash
pip install -r requirements.txt
```

## Ejecución del servidor

En una terminal, ejecutar:

```bash
python servidor.py
```

## Ejecución del cliente de consola

En otra terminal, ejecutar:

```bash
python cliente.py
```

Desde el cliente se puede:

1. Registrar un usuario.
2. Iniciar sesión.
3. Ver la bienvenida de `/tareas`.
4. Crear tareas.
5. Listar tareas.
6. Eliminar tareas.
