import requests

BASE_URL = "http://127.0.0.1:5000"


def mostrar_respuesta(response):
    try:
        print(response.json())
    except Exception:
        print(response.text)


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
    response = requests.get(f"{BASE_URL}/tareas/{usuario_id}", timeout=5)
    mostrar_respuesta(response)


def crear_tarea(usuario_id):
    titulo = input("Título de la tarea: ").strip()
    response = requests.post(
        f"{BASE_URL}/tareas",
        json={"usuario_id": usuario_id, "titulo": titulo},
        timeout=5,
    )
    mostrar_respuesta(response)


def eliminar_tarea():
    try:
        tarea_id = int(input("ID de la tarea a eliminar: "))
    except ValueError:
        print("Debe ingresar un número válido.")
        return

    response = requests.delete(f"{BASE_URL}/tareas/{tarea_id}", timeout=5)
    mostrar_respuesta(response)


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


if __name__ == "__main__":
    main()
