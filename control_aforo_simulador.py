import time
import sqlite3
import logging

# Configuración de logging
logging.basicConfig(filename="aforo.log", level=logging.INFO)

# Conectar a la base de datos (SQLite)
conn = sqlite3.connect("aforo.db")  # Si no existe, SQLite crea el archivo aforo.db
cursor = conn.cursor()

# Crear la tabla si no existe
cursor.execute('''CREATE TABLE IF NOT EXISTS contador (id INTEGER PRIMARY KEY, count INTEGER)''')
cursor.execute('''INSERT OR IGNORE INTO contador (id, count) VALUES (1, 0)''')  # Inserta solo si no existe
conn.commit()

# Función para obtener el número actual de personas
def get_current_count():
    cursor.execute('SELECT count FROM contador WHERE id=1')
    return cursor.fetchone()[0]

# Función para actualizar el número de personas
def update_count(new_count):
    cursor.execute('UPDATE contador SET count=? WHERE id=1', (new_count,))
    conn.commit()

# Variables de configuración
contador = get_current_count()  # Recupera el valor actual desde la base de datos
tiempo_max = 12.0  # tiempo máximo en segundos entre sensores
activaciones = []  # guarda el orden y tiempo de activación

# Mensaje de inicio
print("=== Simulador de Control de Aforo ===")
print("Instrucciones:")
print("- Escribí '1' si se activó el Sensor 1")
print("- Escribí '2' si se activó el Sensor 2")
print("- Escribí 'q' para salir\n")

try:
    while True:
        # Obtener la entrada del sensor
        sensor = input("Sensor activado (1/2): ").strip()

        # Finalizar el programa si se ingresa 'q'
        if sensor == 'q':
            print("Programa finalizado.")
            break

        # Validación de entrada
        if sensor not in ['1', '2']:
            print("⚠️ Entrada inválida. Usá solo '1', '2' o 'q'.")
            continue

        # Guardar activaciones con el tiempo
        activaciones.append((int(sensor), time.time()))

        # Procesar las activaciones
        if len(activaciones) == 2:
            primero, t1 = activaciones[0]
            segundo, t2 = activaciones[1]

            if t2 - t1 > tiempo_max:
                print("⏱️ Tiempo excedido entre sensores. Ignorado.")
            else:
                if primero == 1 and segundo == 2:
                    contador += 1
                    print(f"➡️ Persona ENTRÓ. Total: {contador}")
                    update_count(contador)  # Actualiza el contador en la base de datos
                elif primero == 2 and segundo == 1:
                    contador -= 1
                    print(f"⬅️ Persona SALIÓ. Total: {contador}")
                    update_count(contador)  # Actualiza el contador en la base de datos
                else:
                    print("🤷 Orden no reconocido.")

            activaciones = []  # Reiniciar para la próxima detección

except KeyboardInterrupt:
    print("\n🛑 Interrupción manual. Programa cerrado.")
finally:
    conn.close()  # Cerrar conexión a base de datos
    input("\nPresioná Enter para salir...")  # Mantiene la consola abierta al hacer doble clic
