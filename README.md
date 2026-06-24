# PFO 3 - Rediseño como Sistema Distribuido Cliente-Servidor

## Descripción

Este proyecto toma como base el sistema desarrollado en la PFO 2 y lo adapta a una arquitectura distribuida utilizando sockets.

El servidor permite registrar usuarios, iniciar sesión y acceder a una pantalla HTML de bienvenida en "tareas".
Además, se agregan endpoints simples para crear, listar y eliminar tareas desde un cliente de consola.

El proyecto utiliza SQLite para la persistencia de datos y Werkzeug para guardar contraseñas hasheadas, evitando almacenarlas en texto plano.

## Estructura del proyecto

```txt
pfo3_sistema_distribuido/
├── servidor.py
├── cliente.py
├── README.md
```

## Requisitos

* Python 3 instalado.
* pip instalado.
* Librerías Flask y Requests.

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
pip install flask requests
```

## Ejecución del servidor

En una terminal, ejecutar:

```bash
python servidor.py
```

Al iniciar, el servidor levanta dos servicios:

* API Flask en `http://127.0.0.1:5000`
* Servidor TCP por sockets en `127.0.0.1:6000`

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
