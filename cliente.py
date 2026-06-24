import requests
import socket
import json

BASE_URL = "http://127.0.0.1:5000"

SOCKET_HOST = "127.0.0.1"
SOCKET_PORT = 6000


def mostrar_respuesta(response):
    try:
        print(response.json())
    except Exception:
        print(response.text)


def mostrar_datos(datos):
    print(json.dumps(datos, indent=4, ensure_ascii=False))


def enviar_por_socket(datos):
    """
    Envía una tarea al servidor por socket TCP y recibe el resultado.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
        cliente.settimeout(5)
        cliente.connect((SOCKET_HOST, SOCKET_PORT))

        mensaje = json.dumps(datos, ensure_ascii=False) + "\n"
        cliente.sendall(mensaje.encode("utf-8"))

        respuesta = b""

        while not respuesta.endswith(b"\n"):
            parte = cliente.recv(4096)
            if not parte:
                break
            respuesta += parte

    return json.loads(respuesta.decode("utf-8").strip())


def registrar_usuario():
    usuario = input("Usuario: ").strip()
    contrasena = input("Contraseña: ")
    response = requests.post(
        f"{BASE_URL}/registro",
        json={"usuario": usuario, "contraseña": contrasena},
        timeout=5,
    )
    mostrar_respuesta(response)


def iniciar_sesion():
    usuario = input("Usuario: ").strip()
    contrasena = input("Contraseña: ")
    response = requests.post(
        f"{BASE_URL}/login",
        json={"usuario": usuario, "contraseña": contrasena},
        timeout=5,
    )
    datos = response.json()
    print(datos)
    if datos.get("estado") == "success":
        return datos["usuario_id"]
    return None


def ver_bienvenida():
    response = requests.get(f"{BASE_URL}/tareas", timeout=5)
    print(response.text)


def listar_tareas(usuario_id):
    respuesta = enviar_por_socket({
        "accion": "listar",
        "usuario_id": usuario_id,
    })
    mostrar_datos(respuesta)


def crear_tarea(usuario_id):
    titulo = input("Título de la tarea: ").strip()
    respuesta = enviar_por_socket({
        "accion": "crear",
        "usuario_id": usuario_id,
        "titulo": titulo,
    })
    mostrar_datos(respuesta)


def eliminar_tarea():
    try:
        tarea_id = int(input("ID de la tarea a eliminar: "))
    except ValueError:
        print("Debe ingresar un número válido.")
        return

    respuesta = enviar_por_socket({
        "accion": "eliminar",
        "tarea_id": tarea_id,
    })
    mostrar_datos(respuesta)


def menu_tareas(usuario_id):
    while True:
        print("\n--- Menú de tareas ---")
        print("1. Ver bienvenida GET /tareas")
        print("2. Listar mis tareas")
        print("3. Crear tarea")
        print("4. Eliminar tarea")
        print("5. Cerrar sesión")
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            ver_bienvenida()
        elif opcion == "2":
            listar_tareas(usuario_id)
        elif opcion == "3":
            crear_tarea(usuario_id)
        elif opcion == "4":
            eliminar_tarea()
        elif opcion == "5":
            break
        else:
            print("Opción inválida.")


def main():
    while True:
        print("\n=== Cliente de consola ===")
        print("1. Registrar usuario")
        print("2. Iniciar sesión")
        print("3. Salir")
        opcion = input("Seleccione una opción: ").strip()

        try:
            if opcion == "1":
                registrar_usuario()
            elif opcion == "2":
                usuario_id = iniciar_sesion()
                if usuario_id:
                    menu_tareas(usuario_id)
            elif opcion == "3":
                break
            else:
                print("Opción inválida.")
        except requests.ConnectionError:
            print("No se pudo conectar al servidor. Iniciá servidor.py primero.")
        except requests.Timeout:
            print("La solicitud tardó demasiado tiempo.")
        except socket.timeout:
            print("La conexión por socket tardó demasiado tiempo.")
        except ConnectionRefusedError:
            print("No se pudo conectar al servidor. Iniciá servidor.py primero.")
        except json.JSONDecodeError:
            print("El servidor devolvió una respuesta inválida.")


if __name__ == "__main__":
    main()
