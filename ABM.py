import sqlite3
import tkinter as tk

# Conectar a una base de datos (la base de datos se creará si no existe)
conexion = sqlite3.connect('mi_base_de_datos2.db')

# Crear un cursor para ejecutar comandos SQL
cursor = conexion.cursor()

# Crear una tabla
cursor.execute('''
    CREATE TABLE IF NOT EXISTS productos (
        codigo INTEGER PRIMARY KEY,
        nombre TEXT NOT NULL,
        precio REAL NOT NULL
    )
''')
# Confirmar los cambios
conexion.commit()

#######################################################################################
def mostrar_menu_principal():
    limpiar_ventana()
    etiqueta_menu = tk.Label(ventana, text="Menú Principal", font=("Arial", 24))
    etiqueta_menu.grid(row=0, column=0, columnspan=2, pady=20)
    
    boton_salir = tk.Button(ventana, text="Salir", command=ventana.destroy)
    boton_salir.grid(row=2, column=0, columnspan=2, pady=10)
#######################################################################################
def salir():
    ventana.destroy()
#######################################################################################
def mostrar_menu_principal():
    # Limpia la ventana y muestra el menú principal
    for widget in ventana.winfo_children():
        widget.destroy()
    
    tk.Label(ventana, text="Menú Principal", font=("Arial", 24)).pack(pady=20)
    tk.Button(ventana, text="Salir", command=ventana.quit).pack(pady=10)
    
#######################################################################################
#BUSCA DUPLICADOS
def duplicados(dato):
    # Crear un cursor
    cursor = conexion.cursor()
    
    # Ejecutar consulta con parámetro
    if dato.isdigit():  # Verifica si el parámetro es un número (id)
        cursor.execute('''
        SELECT * FROM productos WHERE codigo = ?
        ''', (dato,))
    else:
        cursor.execute('''
        SELECT * FROM productos WHERE nombre = ?
        ''', (dato,))
        
    # Recuperar todos los resultados
    resultados = cursor.fetchall()
    
    # Cerrar el cursor
    cursor.close()
    
    # Determinar si hay resultados
    if not resultados:  # Si la lista está vacía
        return 1  # No hay duplicados
    else:
        return 2  # Hay duplicados

#######################################################################################
#SE BUSCA EL DATO
def busqueda(nombre_producto,resultado_text_widget):
    # Ejecutar consulta con parámetro
    if nombre_producto.isdigit():  # Verifica si el parámetro es un número (id)
        cursor.execute('''
        SELECT * FROM productos WHERE codigo= ?
        ''', (nombre_producto,))
    else:
        cursor.execute('''
        SELECT * FROM productos WHERE nombre = ?
        ''', (nombre_producto,))
        
    # Recuperar todos los resultados
    resultados = cursor.fetchall()
    
    # Limpiar el widget de texto antes de mostrar nuevos resultados
    resultado_text_widget.delete(1.0, tk.END)

    # Mostrar los resultados en el widget de texto
    for fila in resultados:
        resultado_text_widget.insert(tk.END, f"{fila}\n")

#FUNCION CONSULTAR
def consultar_dato():
    limpiar_ventana()
    entrada = tk.Entry(ventana)
    entrada.grid(row=1, column=1, padx=2, pady=0)

    # Crear un widget Text para mostrar los resultados
    resultado_text_widget = tk.Text(ventana, height=10, width=50)
    resultado_text_widget.grid(row=7, column=0, columnspan=2, padx=10, pady=10)
    
    # Definir la función que obtendrá el valor de la entrada
    def obtener_valor():
        producto = entrada.get()
        busqueda(producto,resultado_text_widget)

    boton_consultar = tk.Button(ventana, text="Consultar", command=obtener_valor)
    boton_consultar.grid(row=1, column=0, padx=0, pady=0)
    boton_consulta = tk.Button(ventana, text="menu", command=menu_principal)
    boton_consulta.grid(row=2, column=0 ,padx=0, pady=0)
    
#######################################################################################
#SE CARGAN LOS DATOS
def ingresar(producto,precio,codigo,resultado_text_widget):
    num=duplicados(producto)
    resultado_text_widget.delete(1.0, tk.END)
    if num==1:
        cursor.execute('''
            INSERT INTO productos (codigo,nombre, precio)
         VALUES (?,?, ?)
        ''', (codigo,producto, precio))

        # Confirmar los cambios
        conexion.commit()
       
        resultado_text_widget.insert(tk.END, f"Agegado con Exito\n")
    else:
        
        resultado_text_widget.insert(tk.END, f"Ya existe este producto\n")
#######################################################################################
def limpiar_ventana():
    for widget in ventana.grid_slaves():
        widget.destroy()
#######################################################################################    
#FUNCION AGREGAR
def agregar_datos():
    limpiar_ventana()
    # Crear y posicionar etiquetas y entradas
    etiqueta = tk.Label(ventana, text="producto")
    etiqueta.grid(row=2, column=0, padx=10, pady=5, sticky="e")
    entrada = tk.Entry(ventana)
    entrada.grid(row=2, column=1, padx=10, pady=5)

    etiqueta = tk.Label(ventana, text="Precio")
    etiqueta.grid(row=3, column=0, padx=10, pady=5, sticky="e")
    entrada2 = tk.Entry(ventana)
    entrada2.grid(row=3, column=1, padx=10, pady=5)
    
    etiqueta = tk.Label(ventana, text="Codigo")
    etiqueta.grid(row=4, column=0, padx=10, pady=5, sticky="e")
    entrada3 = tk.Entry(ventana)
    entrada3.grid(row=4, column=1, padx=10, pady=5)

    # Crear un widget Text para mostrar los resultados
    resultado_text_widget = tk.Text(ventana, height=10, width=50)
    resultado_text_widget.grid(row=7, column=0, columnspan=2, padx=10, pady=10)
    
    # Definir la función que obtendrá el valor de la entrada
    def obtener_valor():
        producto = entrada.get()
        precio=entrada2.get()
        codigo=entrada3.get()
        ingresar(producto,precio,codigo,resultado_text_widget)

    boton_consultar = tk.Button(ventana, text="Agregar", command=obtener_valor)
    boton_consultar.grid(row=6, column=0, padx=0, pady=0)
    boton_consulta = tk.Button(ventana, text="menu", command=menu_principal)
    boton_consulta.grid(row=5, column=0 ,padx=0, pady=0)
#######################################################################################

#ELIMINAR PRODUCTO
def borrar(producto,resultado_text_widget):
    # Eliminar datos
    if producto.isdigit:
        cursor.execute('''
            DELETE FROM productos
            WHERE codigo = ?
        ''', (producto,))
    else:
        cursor.execute('''
            DELETE FROM productos
            WHERE nombre = ?
        ''', (producto,))
    # Confirmar los cambios
    conexion.commit()
     # Limpiar el widget de texto antes de mostrar nuevos resultados
     
    #hacer validacion
    resultado_text_widget.delete(1.0, tk.END)
    resultado_text_widget.insert(tk.END, f"Eliminado con Exito\n")

def bajar_dato():
    limpiar_ventana()
    # Crear y posicionar etiquetas y entradas
    etiqueta = tk.Label(ventana, text="producto")
    etiqueta.grid(row=2, column=0, padx=10, pady=5, sticky="e")
    entrada = tk.Entry(ventana)
    entrada.grid(row=2, column=1, padx=10, pady=5)
    
    # Crear un widget Text para mostrar los resultados
    resultado_text_widget = tk.Text(ventana, height=10, width=50)
    resultado_text_widget.grid(row=7, column=0, columnspan=2, padx=10, pady=10)
    
    # Definir la función que obtendrá el valor de la entrada
    def obtener_valor():
        producto = entrada.get()
        borrar(producto,resultado_text_widget)
    
    boton_consultar = tk.Button(ventana, text="Eliminar", command=obtener_valor)
    boton_consultar.grid(row=6, column=0, padx=0, pady=0)
    boton_consulta = tk.Button(ventana, text="menu", command=menu_principal)
    boton_consulta.grid(row=5, column=0 ,padx=0, pady=0)

#######################################################################################
def actualizar_datos(campo, nuevo_valor, producto, resultado_text_widget):
    # Conectar a la base de datos
   
    cursor = conexion.cursor()

    if campo == "codigo":
        cursor.execute('''
            UPDATE productos
            SET codigo = ?
            WHERE nombre = ?
        ''', (nuevo_valor, producto))
    elif campo == "nombre":
        cursor.execute('''
            UPDATE productos
            SET nombre = ?
            WHERE nombre = ?
        ''', (nuevo_valor, producto))
    elif campo == "precio":
        cursor.execute('''
            UPDATE productos
            SET precio = ?
            WHERE nombre = ?
        ''', (nuevo_valor, producto))
    else:
        resultado_text_widget.delete('1.0', 'end')
        resultado_text_widget.insert('end', "Campo a modificar no válido.")
       

    conexion.commit()
        
    if cursor.rowcount == 0:
        resultado_text_widget.delete('1.0', 'end')
        resultado_text_widget.insert('end', "No se encontró el producto o no se actualizó.")
    else:
        resultado_text_widget.delete('1.0', 'end')
        resultado_text_widget.insert('end', f"Producto '{producto}' actualizado exitosamente.")
            
    cursor.close()

# Función para modificar un producto
def modificar(producto, resultado_text_widget):
    
    resultado_text_widget.delete(1.0, tk.END)
    
    if duplicados(producto) == 1:
        resultado_text_widget.insert(tk.END, "No existe ese producto\n")

    etiqueta = tk.Label(ventana, text="¿Qué desea modificar (precio, codigo, nombre)?")
    etiqueta.grid(row=2, column=0, padx=10, pady=5, sticky="e")
    
    campo_a_modificar = tk.StringVar()
    entrada_campo = tk.Entry(ventana, textvariable=campo_a_modificar)
    entrada_campo.grid(row=2, column=1, padx=10, pady=5)
    
    etiqueta_valor = tk.Label(ventana, text="Valor nuevo:")
    etiqueta_valor.grid(row=3, column=0, padx=10, pady=5, sticky="e")
    
    entrada_nuevo_valor = tk.Entry(ventana)
    entrada_nuevo_valor.grid(row=3, column=1, padx=10, pady=5)
    
    def obtener_valor():
        campo = campo_a_modificar.get()
        nuevo_valor = entrada_nuevo_valor.get()
        actualizar_datos(campo, nuevo_valor, producto, resultado_text_widget)
    
    boton_modificar = tk.Button(ventana, text="Modificar", command=obtener_valor)
    boton_modificar.grid(row=4, column=0, columnspan=2, pady=10)

# Función para modificar un dato
def modificar_dato():
    limpiar_ventana()
    etiqueta = tk.Label(ventana, text="Ingrese el producto a modificar (nombre)")
    etiqueta.grid(row=2, column=0, padx=10, pady=5, sticky="e")
    
    entrada = tk.Entry(ventana)
    entrada.grid(row=2, column=1, padx=10, pady=5)
    
    resultado_text_widget = tk.Text(ventana, height=10, width=50)
    resultado_text_widget.grid(row=7, column=0, columnspan=2, padx=10, pady=10)
    
    def obtener_valor():
        producto = entrada.get()
        modificar(producto, resultado_text_widget)
    band=1
    if band==1:
        boton_consultar = tk.Button(ventana, text="Buscar", command=obtener_valor)
        boton_consultar.grid(row=6, column=0, columnspan=2, pady=10)
        band=2
    boton_consulta = tk.Button(ventana, text="menu", command=menu_principal)
    boton_consulta.grid(row=6, column=0, padx=0, pady=0)
    
#######################################################################################
def obtener_datos_de_bd():
    # Conectar a la base de datos (ajusta el nombre del archivo a tu base de datos)
    conn = sqlite3.connect('mi_base_de_datos2.db')
    cursor = conn.cursor()
    
    # Ejecutar una consulta para obtener todos los productos
    cursor.execute("SELECT codigo,nombre, precio FROM productos")
    
    # Recuperar todos los datos
    productos = cursor.fetchall()
    
    # Cerrar la conexión a la base de datos
    conn.close()
    
    return productos

def mostrar_datos():
    limpiar_ventana()
    
    # Obtener datos de la base de datos
    productos = obtener_datos_de_bd()

    # Crear el widget Text
    resultado_text_widget = tk.Text(ventana, height=25, width=50)
    resultado_text_widget.grid(row=7, column=0, columnspan=5, padx=10, pady=10)

    # Formatear los datos de los productos como un string
    datos = "Codigo\tNombre\tPrecio\n"
    datos += "-"*50 + "\n"  # Línea divisoria
    for producto in productos:
        codigo, nombre, precio = producto
        datos += f"{codigo}\t{nombre}\t${precio}\n"

    # Insertar los datos en el widget Text
    resultado_text_widget.insert(tk.END, datos)

    # Crear el botón
    boton_consulta = tk.Button(ventana, text="menu", command=menu_principal)
    boton_consulta.grid(row=1, column=2, padx=5, pady=5, sticky='ew')

    # Configurar las columnas para que se expandan
    ventana.grid_columnconfigure(0, weight=1)
    ventana.grid_columnconfigure(1, weight=1)
    ventana.grid_columnconfigure(2, weight=1)
    ventana.grid_columnconfigure(3, weight=1)
    ventana.grid_columnconfigure(4, weight=1)

    # Configurar la fila para que se expanda verticalmente
    ventana.grid_rowconfigure(1, weight=1)

#######################################################################################
def menu_principal():
    limpiar_ventana()
    ventana.title("Programa final")
    ventana.geometry("500x500")

    # Etiqueta del menú principal
    etiqueta_menu = tk.Label(ventana, text="Menú Principal", font=("Arial", 16))
    etiqueta_menu.grid(row=0, column=0, columnspan=5, padx=10, pady=20, sticky='n')

    # Botones
    boton_alta = tk.Button(ventana, text="Alta", command=agregar_datos)
    boton_alta.grid(row=1, column=0, padx=5, pady=5, sticky='ew')

    boton_baja = tk.Button(ventana, text="Baja", command=bajar_dato)
    boton_baja.grid(row=1, column=1, padx=5, pady=5, sticky='ew')

    boton_consulta = tk.Button(ventana, text="Consulta", command=consultar_dato)
    boton_consulta.grid(row=1, column=2, padx=5, pady=5, sticky='ew')

    boton_modificar = tk.Button(ventana, text="Modificar", command=modificar_dato)
    boton_modificar.grid(row=1, column=3, padx=5, pady=5, sticky='ew')

    boton_productos = tk.Button(ventana, text="Productos", command=mostrar_datos)
    boton_productos.grid(row=1, column=4, padx=5, pady=5, sticky='ew')

    # Botón para salir
    boton_salir = tk.Button(ventana, text="Salir", command=ventana.destroy)
    boton_salir.grid(row=2, column=0, columnspan=5, padx=5, pady=5, sticky='ew')

    # Widget de texto para resultados
    resultado_text_widget = tk.Text(ventana, height=10, width=45)
    resultado_text_widget.grid(row=3, column=0, columnspan=5, padx=10, pady=10)
    resultado_text_widget.insert('end', "Hola, Bienvenido al programa")

    # Configurar columnas para que se expandan uniformemente
    for i in range(5):
        ventana.grid_columnconfigure(i, weight=1)

    # Configurar filas para que se expandan
    ventana.grid_rowconfigure(1, weight=1)
    ventana.grid_rowconfigure(2, weight=1)
    ventana.grid_rowconfigure(3, weight=1)
    
#######################################################################################
ventana = tk.Tk()    
# Ejecutar el bucle principal
limpiar_ventana()
menu_principal()
ventana.mainloop()
# Cerrar el cursor y la conexión
cursor.close()
conexion.close()