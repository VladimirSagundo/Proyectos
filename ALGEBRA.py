import tkinter as tk
from tkinter import ttk

def solve_cramer(matrix, vector):
    n = len(matrix)
    det_A = determinant(matrix)

    if det_A == 0:
        return None

    solutions = []
    for i in range(n):
        # Reemplazar la columna i de la matriz por el vector
        temp_matrix = replace_column(matrix, vector, i)
        x_i = determinant(temp_matrix) / det_A
        solutions.append(x_i)

    return solutions

def determinant(matrix):
    n = len(matrix)

    if n == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]

    det = 0
    for j in range(n):
        submatrix = []
        for i in range(1, n):
            submatrix.append(matrix[i][0:j] + matrix[i][j+1:])
        det += ((-1) ** j) * matrix[0][j] * determinant(submatrix)

    return det

def replace_column(matrix, vector, column):
    temp_matrix = []
    for i in range(len(matrix)):
        temp_row = matrix[i].copy()
        temp_row[column] = vector[i]
        temp_matrix.append(temp_row)
    return temp_matrix

def show_solution(matrix, vector):
    det_A = determinant(matrix)

    if det_A == 0:
        solution_text.set("Solución paso a paso", "La matriz no tiene solución.")
        return

    solution_str = "Solución paso a paso:\n"
    for i in range(len(matrix)):
        temp_matrix = replace_column(matrix, vector, i)
        x_i = determinant(temp_matrix) / det_A
        solution_str += "Paso {}: x{} = {:.3f}\n".format(i+1, i+1, x_i)

    solution_text.set("Solución paso a paso", solution_str)

def solve_button_click():
    matrix_values = []
    for i in range(size):
        row = []
        for j in range(size):
            entry_value = matrix_entries[i][j].get()
            row.append(float(entry_value))
        matrix_values.append(row)

    vector_values = []
    for i in range(size):
        entry_value = vector_entries[i].get()
        vector_values.append(float(entry_value))

    solutions = solve_cramer(matrix_values, vector_values)

    if solutions is None:
        solution_text.set("LA MATRÍZ NO TIENE SOLUCIÓN")
    else:
        solution_str = "LAS SOLUCIÓN ES:\n"
        for i, sol in enumerate(solutions):
            solution_str += "x{} = {:.3f}\n".format(i+1, sol)
        solution_text.set(solution_str)


# Crear la ventana principal
window = tk.Tk()
window.title("MÉTODO DE CRAMER")
window.geometry("800x500")
window['bg'] = '#383838'
entry=0

def validate_entry(char):
    return char in "0123456789"
validatecommand = window.register(validate_entry)

validate_command = window.register(validate_entry)

def limit_entry_length(entry, limit):
    def limit_length(event):
        if len(entry.get()) >= limit and event.keysym != 'BackSpace':
            return "break"
    entry.bind("<Key>", limit_length)
# Etiqueta y campo de entrada para el tamaño de la matriz
size_label = tk.Label(window, text="- Bienvenidos -", font="Times 40", fg="white")
size_label['bg'] = '#383838'
size_label.place(x=230, y=50)
size_label = tk.Label(window, text="Ingresa el tamaño de la matriz que quieres obtener:", fg="white")
size_label['bg'] = '#585858'
size_label.place(x=240, y=190)
def numero(char):
    return char in "0123456789"
validatecommand = window.register(numero)
tamaño=["3", "4", "5", "6", "7", "8"]
size_entry = ttk.Combobox(window, values=tamaño, state="readonly", justify="center", width=3)
size_entry.set("3")
size_entry.place(x=520, y=190)

# Botón para crear la matriz y el vector
create_button = tk.Button(window, text="Crear matriz", command=lambda: create_matrix_vector(), fg="white", borderwidth=10)
create_button.place(x=350, y= 280)
create_button['bg'] = '#585858'

# Variables para almacenar los valores de las entradas
matrix_entries = []
vector_entries = []
size = 0

def create_matrix_vector():
    global size, matrix_entries, vector_entries

    size = int(size_entry.get())

    # Cerrar la ventana principal
    window.destroy()

    # Crear la nueva ventana para la matriz y el vector
    matrix_window = tk.Tk()
    matrix_window.title("MÉTODO DE CRAMER - Matriz y Vector")
    matrix_window.geometry("800x500")
    matrix_window['bg'] = '#383838'

    def validate_entry(char):
       return char in "0123456789-"
    validatecommand = window.register(validate_entry)
    

    validate_command = matrix_window.register(validate_entry)

    def limit_entry_length(entry, limit):
        def limit_length(event):
            if len(entry.get()) >= limit and event.keysym != 'BackSpace':
                return "break"
        entry.bind("<Key>", limit_length)

    # Crear las nuevas entradas
    for i in range(size):
        entry_row = []
        for j in range(size):
            entry = tk.Entry(matrix_window, width=10, validate="key", validatecommand=(validate_command, "%S"))
            entry.grid(row=i+2, column=j, padx=5, pady=5)
            limit_entry_length(entry, 5)  # Limitamos a 5 dígitos
            entry_row.append(entry)
        matrix_entries.append(entry_row)

        vector_entry = tk.Entry(matrix_window, width=10, validate="key", validatecommand=(validate_command, "%S"))
        vector_entry.grid(row=i+2, column=size, padx=5, pady=5)
        limit_entry_length(vector_entry, 5)  # Limitamos a 5 dígitos
        vector_entries.append(vector_entry)

    # Botón para resolver
    solve_button = tk.Button(matrix_window, text="Resolver", command=solve_button_click, fg="white")
    solve_button['bg'] = '#585858'
    solve_button.grid(row=size+2, column=0, columnspan=size+1, padx=5, pady=5)

    # Etiqueta para mostrar la solución
    global solution_text
    solution_text = tk.StringVar()
    solution_text.set("")
    solution_label = tk.Label(matrix_window, textvariable=solution_text)
    solution_label.grid(row=size+3, column=0, columnspan=size+1, padx=5, pady=5)

    # Ejecutar la nueva ventana
    ancho_ventana = 800
    alto_ventana = 500
    x_ventana = matrix_window.winfo_screenwidth() // 2 - ancho_ventana // 2
    y_ventana = matrix_window.winfo_screenheight() // 2 - alto_ventana // 2
    posicion = str(ancho_ventana) + "x" + str(alto_ventana) + "+" + str(x_ventana) + "+" + str(y_ventana)
    matrix_window.geometry(posicion)
    matrix_window.resizable(width=0, height=0)
        # Centrar todo el contenido
    for child in matrix_window.winfo_children():
        child.grid_configure(padx=10, pady=10)
        if isinstance(child, tk.Button):
            child.configure(font="bold")
    
    matrix_window.mainloop()

# Ejecutar la ventana principal
ancho_ventana = 800
alto_ventana = 500
x_ventana = window.winfo_screenwidth() // 2 - ancho_ventana // 2
y_ventana = window.winfo_screenheight() // 2 - alto_ventana // 2
posicion = str(ancho_ventana) + "x" + str(alto_ventana) + "+" + str(x_ventana) + "+" + str(y_ventana)
window.geometry(posicion)
window.resizable(width=0, height=0)
window.mainloop()
