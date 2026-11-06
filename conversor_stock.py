import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox

def procesar_excel():
    # 1. Abrir ventana para elegir el Excel desordenado
    archivo_origen = filedialog.askopenfilename(
        title="Seleccionar el Excel del proveedor",
        filetypes=[("Archivos Excel", "*.xls *.xlsx")]
    )
    
    if not archivo_origen:
        return

    try:
        # 2. Elegir dónde guardar el Excel ya formateado
        archivo_destino = filedialog.asksaveasfilename(
            title="Guardar stock limpio como",
            defaultextension=".xlsx",
            filetypes=[("Archivos Excel", "*.xlsx")]
        )
        
        if not archivo_destino:
            return

        # 3. Ejecutar la lógica de limpieza y extracción
        df = pd.read_excel(archivo_origen, sheet_name=0) 
        
        # Aislar las columnas exactas del proveedor
        extracted = df[['LISTA DE PRECIOS GENERALES', 'Unnamed: 10', 'Unnamed: 11', 'Unnamed: 1']].copy()
        extracted.columns = ['Nombre', 'Precio dueño', 'Precio venta', 'Cantidad']
        
        # Detectar rubros y rellenar hacia abajo
        is_category = extracted['Nombre'].notna() & extracted['Precio dueño'].isna()
        extracted['Rubro'] = np.where(is_category, extracted['Nombre'], np.nan)
        extracted['Rubro'] = extracted['Rubro'].ffill()
        
        # Filtrar solo productos, crear columna 'Código' y ordenar
        final_df = extracted[extracted['Precio dueño'].notna() & extracted['Nombre'].notna()].copy()
        final_df['Código'] = ''
        final_df = final_df[['Código', 'Nombre', 'Rubro', 'Precio dueño', 'Precio venta', 'Cantidad']]
        final_df['Cantidad'] = final_df['Cantidad'].fillna(0).astype(int)
        
        # 4. Exportar el archivo final
        final_df.to_excel(archivo_destino, index=False)
        
        messagebox.showinfo("Proceso Exitoso", f"El archivo se ordenó y guardó correctamente en:\n{archivo_destino}")
        
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un problema al procesar los datos:\n{e}")

# Interfaz gráfica principal mejorada
root = tk.Tk()
root.title("Conversor de Stock - Ivan Enrique")
root.geometry("450x220")
root.configure(bg="#f4f4f9") # Color de fondo claro
root.eval('tk::PlaceWindow . center')

# Marco central para agrupar los elementos
frame = tk.Frame(root, bg="#f4f4f9")
frame.pack(expand=True)

titulo = tk.Label(frame, text="Transformar Excel del proveedor\nal formato del sistema web", font=("Segoe UI", 12, "bold"), bg="#f4f4f9", fg="#333333", pady=15)
titulo.pack()

btn_procesar = tk.Button(frame, text="Seleccionar Excel y Procesar", command=procesar_excel, font=("Segoe UI", 10, "bold"), bg="#0078D7", fg="white", cursor="hand2", padx=20, pady=8, relief="flat")
btn_procesar.pack(pady=10)

root.mainloop()
