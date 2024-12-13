import psycopg2

def connect_db():
    return psycopg2.connect(
        user='postgres',
        password='123456',
        host='127.0.0.1',
        port='5432',
        database='my_database'
    )

def create_record():
    conexion = connect_db()
    cursor = conexion.cursor()
    
    alias = input('Ingresa el alias: ')
    nombre = input('Ingresa el nombre: ')
    edad = input('Ingresa la edad: ')

    sql = 'INSERT INTO personajes (alias, nombre, edad) VALUES (%s, %s, %s)'
    datos = (alias, nombre, edad)

    cursor.execute(sql, datos)
    conexion.commit()

    print(f'Registro insertado: {cursor.rowcount}')

    cursor.close()
    conexion.close()

def read_all_records():
    conexion = connect_db()
    cursor = conexion.cursor()

    sql = 'SELECT * FROM personajes'
    cursor.execute(sql)

    registros = cursor.fetchall()
    for fila in registros:
        print(fila)

    cursor.close()
    conexion.close()

def read_single_record():
    conexion = connect_db()
    cursor = conexion.cursor()

    idpersonaje = input('Ingresa el ID del registro a mostrar: ')
    sql = 'SELECT * FROM personajes WHERE idpersonaje = %s'

    cursor.execute(sql, (idpersonaje,))
    registro = cursor.fetchone()

    print(registro)

    cursor.close()
    conexion.close()

def update_record():
    conexion = connect_db()
    cursor = conexion.cursor()

    idpersonaje = input('Ingresa el ID del personaje a editar: ')
    alias = input('Ingresa el alias: ')
    nombre = input('Ingresa el nombre: ')
    edad = input('Ingresa la edad: ')

    sql = 'UPDATE personajes SET alias = %s, nombre = %s, edad = %s WHERE idpersonaje = %s'
    datos = (alias, nombre, edad, idpersonaje)

    cursor.execute(sql, datos)
    conexion.commit()

    print(f'Registro actualizado: {cursor.rowcount}')

    cursor.close()
    conexion.close()

def delete_record():
    conexion = connect_db()
    cursor = conexion.cursor()

    idpersonaje = input('Ingresa el ID del registro a eliminar: ')
    sql = 'DELETE FROM personajes WHERE idpersonaje = %s'

    cursor.execute(sql, (idpersonaje,))
    conexion.commit()

    print(f'Registros eliminados: {cursor.rowcount}')

    cursor.close()
    conexion.close()

def menu():
    while True:
        print("\n--- CRUD con PostgreSQL ---")
        print("1. Crear un nuevo personaje")
        print("2. Leer todos los personajes")
        print("3. Leer un personaje por ID")
        print("4. Actualizar un personaje")
        print("5. Eliminar un personaje")
        print("6. Salir")

        opcion = input("Selecciona una opción: ")

        if opcion == '1':
            create_record()
        elif opcion == '2':
            read_all_records()
        elif opcion == '3':
            read_single_record()
        elif opcion == '4':
            update_record()
        elif opcion == '5':
            delete_record()
        elif opcion == '6':
            print("Saliendo...")
            break
        else:
            print("Opción no válida. Intenta de nuevo.")

if __name__ == '__main__':
    menu()
