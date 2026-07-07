# Documento explicativo — Proyecto: Gráficos estadísticos (Tkinter + Matplotlib)

## 1. Descripción del problema
Se requiere una aplicación que permita al usuario:

- Ingresar una lista de números desde una interfaz gráfica.
- Calcular métricas estadísticas básicas a partir de esos datos:
  - **Media (promedio)**
  - **Mediana**
  - **Moda** (incluyendo el caso de múltiples modas)
- Visualizar los datos mediante un gráfico seleccionado por el usuario:
  - Barras
  - Líneas
  - Pastel

Además, la aplicación debe:

- Validar la entrada para evitar fallos cuando el usuario ingresa texto no numérico.
- Manejar restricciones específicas de cada tipo de gráfico:
  - Para **pastel**, los valores deben ser **no negativos**.
  - Para **pastel**, la **suma** de los valores debe ser **mayor que 0**.


## 2. Enfoque de la solución
La solución se implementa con una interfaz **Tkinter** que integra **Matplotlib** en la misma ventana.

### 2.1 Componentes principales
- **Interfaz Tkinter**:
  - Campo de entrada de números (texto libre).
  - Selector de tipo de gráfico mediante Radiobuttons.
  - Botón “Generar gráfico”.
  - Panel de salida con:
    - Media
    - Mediana
    - Moda
  - Área gráfica (canvas de Matplotlib embebido).

- **Capa lógica (funciones puras)**:
  - `parse_numbers(raw: str)`
    - Convierte el texto ingresado a una lista de `float`.
    - Soporta separadores por coma, punto y coma (convertido a coma) y espacios.
  - `compute_stats(nums)`
    - Calcula media, mediana y moda.
    - La moda se maneja manualmente para cubrir casos con múltiples valores empatados.
  - `render_plot(ax, nums, chart_type)`
    - Dibuja el gráfico según el tipo seleccionado.
    - Aplica validaciones para el caso de pastel.

- **Integración Matplotlib**:
  - `Figure` + `Axes` se renderizan con `FigureCanvasTkAgg` dentro de Tkinter.

### 2.2 Flujo de ejecución
1. El usuario ingresa una cadena con números.
2. Al presionar “Generar gráfico”, se ejecuta `on_generate()`.
3. Se intenta parsear la entrada con `parse_numbers()`.
   - Si la lista queda vacía → warning.
   - Si hay texto no numérico → error.
4. Se calculan estadísticas con `compute_stats()`.
5. Se actualizan los labels de media/mediana/moda.
6. Se dibuja el gráfico con `render_plot()`.
   - Si el tipo es pastel y hay valores inválidos → error.
7. Se actualiza un estado informativo (`status`).


## 3. Proceso de desarrollo (bitácora)
> Bitácora reconstruida desde la evolución funcional del código actual (entrada → cálculos → gráficos → validaciones → UX).

### Iteración 1 — Prototipo de interfaz y gráfico embebido
- Se creó una ventana Tkinter.
- Se integró un canvas de Matplotlib (embebido) para mostrar gráficos dentro de la misma UI.

**Resultado:** se pudo mostrar un gráfico, pero aún no existía una lógica completa de entrada y estadísticas.

### Iteración 2 — Entrada de datos y parseo robusto
- Se implementó `parse_numbers()`.
- Se habilitó el soporte de múltiples separadores (coma, espacio y `;`).
- Se maneja la conversión a `float` con errores informativos si hay valores no numéricos.

**Resultado:** la app tolera diferentes formatos de ingreso.

### Iteración 3 — Estadísticas: media y mediana
- Se agregó `compute_stats()` para calcular:
  - media usando `statistics.fmean`
  - mediana usando `statistics.median`

**Resultado:** el usuario ve métricas básicas junto al gráfico.

### Iteración 4 — Moda: caso único y múltiples modas
- Se amplió `compute_stats()` para calcular moda con `Counter`.
- Se contempló el caso de múltiples valores que comparten la frecuencia máxima.

**Resultado:** el componente de moda es más completo y no falla en escenarios no triviales.

### Iteración 5 — Tipos de gráfico (barras, líneas, pastel)
- Se implementó `render_plot()` con 3 modos:
  - Barras
  - Líneas (con marcadores)
  - Pastel

**Resultado:** el usuario elige la visualización según su preferencia.

### Iteración 6 — Validaciones específicas para pastel
- Se agregaron reglas antes de dibujar `pie`:
  - rechazar valores negativos
  - rechazar suma total = 0

**Resultado:** se evita que Matplotlib lance errores en escenarios inválidos.

### Iteración 7 — UX y manejo de errores
- Se agregaron ventanas de mensaje con `messagebox` para:
  - datos vacíos
  - entrada inválida
  - errores específicos del gráfico
- Se actualizaron etiquetas y el estado luego de generar exitosamente.

**Resultado:** experiencia de usuario consistente y mensajes claros.


## 4. Conclusión
El proyecto resuelve el problema de representar datos numéricos con estadística descriptiva y visualización en una aplicación de escritorio. La combinación de funciones de lógica (`parse_numbers`, `compute_stats`, `render_plot`) con una UI Tkinter clara permite mantener el código organizado y facilita futuras mejoras como:

- admitir formatos adicionales de entrada
- agregar más estadísticas (varianza, desviación estándar, percentiles)
- soportar histogramas o boxplots

