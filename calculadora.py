import tkinter as tk
from tkinter import messagebox


class CalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora con Gramática")
        self.root.geometry("1200x600")  # Ajustar el tamaño de la ventana
        self.root.configure(bg="#F4F4F4")

        # Marco principal
        main_frame = tk.Frame(self.root, bg="#F4F4F4")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Marco izquierdo (Calculadora)
        calculator_frame = tk.Frame(main_frame, bg="#F4F4F4")
        calculator_frame.pack(side="left", fill="y", padx=10, pady=10)

        # Encabezado
        header_label = tk.Label(
            calculator_frame, text="Calculadora con Gramática", font=("Arial", 20, "bold"), bg="#F4F4F4", fg="#333"
        )
        header_label.pack(pady=10)

        # Input y resultado
        self.input_var = tk.StringVar()
        self.result_var = tk.StringVar()

        self.input_entry = tk.Entry(
            calculator_frame, textvariable=self.input_var, font=("Arial", 18), width=30, bd=2, relief="solid"
        )
        self.input_entry.pack(pady=5)

        self.result_label = tk.Label(
            calculator_frame, textvariable=self.result_var, font=("Arial", 16, "italic"), bg="#F4F4F4", fg="#555"
        )
        self.result_label.pack(pady=5)

        # Botones
        button_frame = tk.Frame(calculator_frame, bg="#F4F4F4")
        button_frame.pack(pady=10)

        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
            ('0', 4, 0), ('.', 4, 1), ('+', 4, 2), ('=', 4, 3),
        ]

        for (text, row, col) in buttons:
            button = tk.Button(
                button_frame,
                text=text,
                font=("Arial", 16),
                width=5,
                height=2,
                bg="#FFFFFF",
                fg="#333333",
                relief="raised",
                command=lambda t=text: self.on_button_click(t),
            )
            button.grid(row=row, column=col, padx=5, pady=5)

        # Botón de limpiar
        clear_button = tk.Button(
            button_frame,
            text="C",
            font=("Arial", 16),
            width=5,
            height=2,
            bg="#FF6F61",
            fg="white",
            relief="raised",
            command=self.clear,
        )
        clear_button.grid(row=5, column=0, columnspan=4, sticky="nsew", padx=5, pady=5)

        # Marco derecho (Árbol de derivación)
        tree_frame = tk.Frame(main_frame, bg="#F4F4F4")
        tree_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        tree_label = tk.Label(
            tree_frame, text="Árbol de Derivación", font=("Arial", 16, "bold"), bg="#F4F4F4", fg="#333"
        )
        tree_label.pack(pady=10)

        self.tree_canvas = tk.Canvas(tree_frame, width=600, height=500, bg="white", bd=2, relief="solid")
        self.tree_canvas.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(tree_frame, orient="vertical", command=self.tree_canvas.yview)
        scrollbar.pack(side="right", fill="y")

        self.tree_canvas.configure(yscrollcommand=scrollbar.set)

    def on_button_click(self, char):
        if char == '=':
            try:
                expression = self.input_var.get()
                self.calculate_result(expression)
                self.draw_tree(expression)
            except Exception as e:
                messagebox.showerror("Error", str(e))
        else:
            self.input_var.set(self.input_var.get() + char)

    def calculate_result(self, expression):
        """Calcula el resultado de la expresión ingresada."""
        try:
            result = eval(expression)  # Evalúa la operación matemática
            self.result_var.set(f"Resultado: {result}")
        except Exception as e:
            self.result_var.set("Error en la operación")
            raise e

    def draw_tree(self, expression):
        """Dibuja el árbol de derivación en el Canvas."""
        self.tree_canvas.delete("all")  # Limpia el Canvas
        x_start = 300  # Coordenada X inicial
        y_start = 20   # Coordenada Y inicial
        node_radius = 20

        def draw_node(x, y, text, parent_coords=None):
            """Dibuja un nodo y conecta con el nodo padre."""
            self.tree_canvas.create_oval(x - node_radius, y - node_radius, x + node_radius, y + node_radius, fill="#87CEEB", outline="#333")
            self.tree_canvas.create_text(x, y, text=text, font=("Arial", 12))
            if parent_coords:
                self.tree_canvas.create_line(parent_coords[0], parent_coords[1] + node_radius, x, y - node_radius, width=2)

        def parse_expr(expr, x, y, parent_coords=None):
            """Genera el árbol de derivación."""
            if '+' in expr:
                draw_node(x, y, 'C', parent_coords)
                draw_node(x - 100, y + 80, 'N', (x, y))
                draw_node(x, y + 80, '+', (x, y))
                draw_node(x + 100, y + 80, 'N', (x, y))

                left, right = expr.split('+', 1)
                parse_expr(left.strip(), x - 100, y + 160, (x - 100, y + 80))
                parse_expr(right.strip(), x + 100, y + 160, (x + 100, y + 80))

            elif '-' in expr:
                draw_node(x, y, 'C', parent_coords)
                draw_node(x - 100, y + 80, 'N', (x, y))
                draw_node(x, y + 80, '-', (x, y))
                draw_node(x + 100, y + 80, 'N', (x, y))

                left, right = expr.split('-', 1)
                parse_expr(left.strip(), x - 100, y + 160, (x - 100, y + 80))
                parse_expr(right.strip(), x + 100, y + 160, (x + 100, y + 80))

            elif '*' in expr:
                draw_node(x, y, 'C', parent_coords)
                draw_node(x - 100, y + 80, 'N', (x, y))
                draw_node(x, y + 80, '*', (x, y))
                draw_node(x + 100, y + 80, 'N', (x, y))

                left, right = expr.split('*', 1)
                parse_expr(left.strip(), x - 100, y + 160, (x - 100, y + 80))
                parse_expr(right.strip(), x + 100, y + 160, (x + 100, y + 80))

            elif '/' in expr:
                draw_node(x, y, 'C', parent_coords)
                draw_node(x - 100, y + 80, 'N', (x, y))
                draw_node(x, y + 80, '/', (x, y))
                draw_node(x + 100, y + 80, 'N', (x, y))

                left, right = expr.split('/', 1)
                parse_expr(left.strip(), x - 100, y + 160, (x - 100, y + 80))
                parse_expr(right.strip(), x + 100, y + 160, (x + 100, y + 80))

            else:
                draw_node(x, y, 'N', parent_coords)
                for i, char in enumerate(expr):
                    draw_node(x + (i - len(expr)//2) * 40, y + 80, 'D', (x, y))
                    draw_node(x + (i - len(expr)//2) * 40, y + 160, char, (x + (i - len(expr)//2) * 40, y + 80))

        parse_expr(expression, x_start, y_start)

        # Ajustar área desplazable del Canvas
        self.tree_canvas.configure(scrollregion=self.tree_canvas.bbox("all"))

    def clear(self):
        """Limpia la entrada y el resultado."""
        self.input_var.set("")
        self.result_var.set("")
        self.tree_canvas.delete("all")


if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()
