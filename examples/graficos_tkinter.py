import tkinter as tk
from tkinter import ttk, messagebox

import matplotlib
matplotlib.use("TkAgg")

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from collections import Counter
import statistics


def parse_numbers(raw: str):
    """Parsea una lista de números a partir de texto.

    Acepta separadores por coma, espacio o salto de línea.
    Ejemplos:
      "10, 20, 30" -> [10, 20, 30]
      "10 20 30"   -> [10, 20, 30]
    """
    if not raw or not raw.strip():
        return []

    cleaned = raw.replace(";", ",")
    parts = []
    for chunk in cleaned.split(","):
        chunk = chunk.strip()
        if not chunk:
            continue
        # dentro del chunk, también aceptamos separadores por espacios
        for sub in chunk.split():
            sub = sub.strip()
            if sub:
                parts.append(sub)

    nums = []
    for p in parts:
        try:
            # Permitimos enteros o decimales
            nums.append(float(p))
        except ValueError:
            raise ValueError(f"Valor no numérico: {p!r}")

    return nums


def format_number(x: float):
    # Formatea para que enteros se vean como enteros
    if x is None:
        return ""
    if abs(x - round(x)) < 1e-9:
        return str(int(round(x)))
    return f"{x:.6g}"


def compute_stats(nums):
    nums_sorted = sorted(nums)

    mean_val = statistics.fmean(nums_sorted)
    median_val = statistics.median(nums_sorted)

    counts = Counter(nums_sorted)
    if not counts:
        mode_val = None
        modes = []
    else:
        max_count = max(counts.values())
        # estadística 'statistics.mode' falla si no hay moda única; manejamos manual
        modes = [v for v, c in counts.items() if c == max_count and max_count > 1]

        mode_val = None if not modes else modes

    # Nota: si hay múltiples modas, devolvemos todas
    return {
        "media": mean_val,
        "mediana": median_val,
        "moda": mode_val,
        "modas": modes,
    }


def render_plot(ax, nums, chart_type: str):
    ax.clear()

    if not nums:
        ax.set_title("Sin datos")
        return

    if chart_type == "barras":
        x = list(range(1, len(nums) + 1))
        ax.bar(x, nums, color="#4C78A8")
        ax.set_xlabel("Índice")
        ax.set_ylabel("Valor")

    elif chart_type == "lineas":
        x = list(range(1, len(nums) + 1))
        ax.plot(x, nums, marker="o", linewidth=2, color="#54A24B")
        ax.set_xlabel("Índice")
        ax.set_ylabel("Valor")

    elif chart_type == "pastel":
        # Matplotlib pie requiere cantidades no negativas en la práctica.
        if any(v < 0 for v in nums):
            raise ValueError("Para un gráfico pastel los valores deben ser no negativos.")

        # Evitamos el caso de suma 0 (pie no se puede normalizar)
        total = sum(nums)
        if total == 0:
            raise ValueError("Para un gráfico pastel la suma de los valores debe ser mayor que 0.")

        labels = [str(i) for i in range(1, len(nums) + 1)]
        ax.pie(nums, labels=labels, autopct="%1.1f%%", startangle=90)
        ax.axis("equal")

    else:
        raise ValueError("Tipo de gráfico no reconocido")


def main():
    root = tk.Tk()
    root.title("Gráficos estadísticos (Tkinter + Matplotlib)")
    root.geometry("1050x680")

    # Layout
    root.rowconfigure(1, weight=1)
    root.columnconfigure(0, weight=1)

    header = ttk.Frame(root)
    header.grid(row=0, column=0, sticky="ew", padx=12, pady=10)
    header.columnconfigure(0, weight=1)

    ttk.Label(header, text="Ingrese una lista de números (separados por coma o espacio):").grid(
        row=0, column=0, sticky="w"
    )

    input_frame = ttk.Frame(root)
    input_frame.grid(row=1, column=0, sticky="nsew", padx=12)
    input_frame.rowconfigure(0, weight=0)
    input_frame.rowconfigure(1, weight=1)
    input_frame.columnconfigure(0, weight=1)
    input_frame.columnconfigure(1, weight=0)

    # Izquierda: entrada + gráfico
    left = ttk.Frame(input_frame)
    left.grid(row=1, column=0, sticky="nsew", padx=(0, 10))
    left.rowconfigure(2, weight=1)
    left.columnconfigure(0, weight=1)

    ttk.Label(left, text="Lista de datos").grid(row=0, column=0, sticky="w")

    data_var = tk.StringVar()
    data_entry = ttk.Entry(left, textvariable=data_var)
    data_entry.grid(row=1, column=0, sticky="ew", pady=(4, 8))
    data_entry.insert(0, "10, 20, 20, 35")

    controls = ttk.Frame(left)
    controls.grid(row=2, column=0, sticky="ew")
    controls.columnconfigure(0, weight=1)

    ttk.Label(controls, text="Tipo de gráfico:").grid(row=0, column=0, sticky="w")

    chart_var = tk.StringVar(value="barras")
    rb_barras = ttk.Radiobutton(controls, text="Barras", value="barras", variable=chart_var)
    rb_lineas = ttk.Radiobutton(controls, text="Líneas", value="lineas", variable=chart_var)
    rb_pastel = ttk.Radiobutton(controls, text="Pastel", value="pastel", variable=chart_var)

    rb_barras.grid(row=0, column=1, sticky="w", padx=10)
    rb_lineas.grid(row=0, column=2, sticky="w")
    rb_pastel.grid(row=0, column=3, sticky="w")

    btn = ttk.Button(controls, text="Generar gráfico", command=lambda: on_generate())
    btn.grid(row=0, column=4, sticky="e", padx=(15, 0))

    # Área de Matplotlib
    fig = Figure(figsize=(7, 4.6), dpi=100)
    ax = fig.add_subplot(111)
    ax.set_title("Gráfico")

    canvas = FigureCanvasTkAgg(fig, master=left)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.grid(row=3, column=0, sticky="nsew", pady=(10, 0))
    left.rowconfigure(3, weight=1)

    # Derecha: estadísticas
    right = ttk.Frame(input_frame)
    right.grid(row=1, column=1, sticky="ns")
    right.columnconfigure(0, weight=1)

    ttk.Label(right, text="Estadísticas", font=("TkDefaultFont", 12, "bold")).grid(
        row=0, column=0, sticky="w", pady=(0, 10)
    )

    stats_box = ttk.Frame(right, padding=10)
    stats_box.grid(row=1, column=0, sticky="n")

    ttk.Label(stats_box, text="Media:").grid(row=0, column=0, sticky="w")
    media_value = ttk.Label(stats_box, text="-")
    media_value.grid(row=0, column=1, sticky="e")

    ttk.Label(stats_box, text="Mediana:").grid(row=1, column=0, sticky="w", pady=(6, 0))
    mediana_value = ttk.Label(stats_box, text="-")
    mediana_value.grid(row=1, column=1, sticky="e", pady=(6, 0))

    ttk.Label(stats_box, text="Moda:").grid(row=2, column=0, sticky="w", pady=(6, 0))
    moda_value = ttk.Label(stats_box, text="-")
    moda_value.grid(row=2, column=1, sticky="e", pady=(6, 0))

    stats_box.columnconfigure(1, weight=1)

    status = ttk.Label(root, text="")
    status.grid(row=2, column=0, sticky="ew", padx=12, pady=(0, 10))

    def on_generate():
        raw = data_var.get()
        try:
            nums = parse_numbers(raw)
            if not nums:
                messagebox.showwarning("Datos", "Ingrese al menos un número.")
                return

            stats = compute_stats(nums)

            media_value.config(text=format_number(stats["media"]))
            mediana_value.config(text=format_number(stats["mediana"]))

            modes = stats["modas"]
            if not modes:
                moda_value.config(text="Sin moda (todas aparecen una vez)")
            else:
                # Si hay varios valores con la misma frecuencia máxima, los mostramos
                modes_sorted = sorted(modes)
                moda_value.config(text=", ".join(format_number(v) for v in modes_sorted))

            try:
                render_plot(ax, nums, chart_var.get())
            except ValueError as e:
                messagebox.showerror("Error en el gráfico", str(e))
                return

            chart_name = chart_var.get()
            ax.set_title(f"Gráfico: {chart_name}")
            fig.tight_layout()
            canvas.draw()

            status.config(text=f"Datos cargados: {len(nums)} valores")

        except ValueError as e:
            messagebox.showerror("Entrada inválida", str(e))

    # Primera carga
    on_generate()

    root.mainloop()


if __name__ == "__main__":
    main()

