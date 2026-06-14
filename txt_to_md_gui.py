#!/usr/bin/env python3
# text_to_md_gui.py - Convierte texto (pegado o desde archivo) a bloque markdown
# Versión optimizada con mejoras de funcionalidad y UX

import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
import ttkbootstrap as tb
from ttkbootstrap.constants import *
import os

class TextToMarkdownApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Convertidor a Markdown (texto o archivo)")
        self.root.geometry("800x700")
        self.root.minsize(600, 500)
        
        # Variable para ruta (opcional)
        self.file_path = tk.StringVar()
        
        self.create_widgets()
        self.bind_shortcuts()
        
    def create_widgets(self):
        """Crea la interfaz gráfica con dos pestañas"""
        # Pestañas para elegir modo
        self.notebook = tb.Notebook(self.root)
        self.notebook.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        # ========== PESTAÑA 1: Pegar texto directamente ==========
        self.tab_paste = tb.Frame(self.notebook)
        self.notebook.add(self.tab_paste, text="📝 Pegar texto", sticky="nsew")
        
        # Instrucciones
        tb.Label(
            self.tab_paste,
            text="Pega tu texto aquí (código, email, documento, etc.):",
            font=("Helvetica", 10, "bold")
        ).pack(anchor=W, padx=10, pady=(10, 0))
        
        # Área de texto con scroll - CORREGIDO: usar tk.scrolledtext.ScrolledText
        self.paste_text = ScrolledText(self.tab_paste, height=20, wrap=tk.WORD)
        self.paste_text.pack(fill=BOTH, expand=True, padx=10, pady=5)
        
        # Botón de conversión
        tb.Button(
            self.tab_paste,
            text="Convertir texto pegado a .md (Ctrl+S)",
            command=self.convert_from_paste,
            bootstyle="success"
        ).pack(pady=10)
        
        # ========== PESTAÑA 2: Cargar archivo .txt ==========
        self.tab_file = tb.Frame(self.notebook)
        self.notebook.add(self.tab_file, text="📂 Cargar archivo", sticky="nsew")
        
        # Frame superior: seleccionar archivo
        top_frame = tb.Frame(self.tab_file, padding=10)
        top_frame.pack(fill=X, padx=5)
        
        tb.Label(top_frame, text="Archivo .txt:", font=("Helvetica", 9, "bold")).pack(side=LEFT, padx=5)
        tb.Entry(top_frame, textvariable=self.file_path, width=45, state="readonly").pack(side=LEFT, padx=5, fill=X, expand=True)
        tb.Button(top_frame, text="Examinar...", command=self.load_file, bootstyle="primary", width=12).pack(side=LEFT, padx=5)
        
        # Instrucciones de vista previa
        tb.Label(
            self.tab_file,
            text="Vista previa del contenido original:",
            font=("Helvetica", 10, "bold")
        ).pack(anchor=W, padx=10, pady=(10, 0))
        
        # Área de texto con scroll - CORREGIDO: usar tk.scrolledtext.ScrolledText
        self.text_area = ScrolledText(self.tab_file, height=20, wrap=tk.WORD, state="disabled")
        self.text_area.pack(fill=BOTH, expand=True, padx=10, pady=5)
        
        # Botón de conversión
        tb.Button(
            self.tab_file,
            text="Convertir archivo a .md (Ctrl+S)",
            command=self.convert_from_file,
            bootstyle="success"
        ).pack(pady=10)
        
        # ========== BARRA DE ESTADO COMÚN ==========
        self.status = tb.Label(self.root, text="✓ Listo", bootstyle="info")
        self.status.pack(fill=X, padx=10, pady=5)
    
    def bind_shortcuts(self):
        """Vincula atajos de teclado"""
        self.root.bind('<Control-s>', self.handle_shortcut)
        self.root.bind('<Control-S>', self.handle_shortcut)
    
    def handle_shortcut(self, event):
        """Maneja el atajo Ctrl+S según la pestaña activa"""
        current_tab = self.notebook.index(self.notebook.select())
        if current_tab == 0:
            self.convert_from_paste()
        else:
            self.convert_from_file()
    
    def load_file(self):
        """Carga un archivo .txt y lo muestra en la vista previa"""
        filetypes = [("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
        filename = filedialog.askopenfilename(
            title="Seleccionar archivo de texto",
            filetypes=filetypes
        )
        
        if filename:
            self.file_path.set(filename)
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Mostrar en vista previa
                self.text_area.config(state="normal")
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, content)
                self.text_area.config(state="disabled")
                
                self.status.config(
                    text=f"✓ Cargado: {os.path.basename(filename)} ({len(content)} caracteres)",
                    bootstyle="success"
                )
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo leer el archivo:\n{str(e)}")
                self.status.config(text="✗ Error al cargar", bootstyle="danger")
    
    def create_markdown_file(self, content, output_path):
        """
        Crea un archivo markdown con el contenido envuelto en bloques de código.
        
        Args:
            content: Contenido a guardar (sin modificaciones)
            output_path: Ruta del archivo de salida
        
        Raises:
            Exception: Si hay error al guardar
        """
        try:
            # Envolver en bloques de código markdown
            wrapped = f"```\n{content}\n```"
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(wrapped)
        except Exception as e:
            raise e
    
    def convert_from_paste(self):
        """Convierte el texto pegado a archivo .md"""
        # Obtener contenido del área de texto
        content = self.paste_text.get(1.0, tk.END)
        
        # Validar que no esté vacío
        if not content.strip():
            messagebox.showwarning(
                "Advertencia",
                "No hay texto pegado para convertir.\nPega algo en el área de texto."
            )
            return
        
        # Preguntar dónde guardar
        output_path = filedialog.asksaveasfilename(
            title="Guardar como archivo Markdown",
            defaultextension=".md",
            initialfile="contenido.md",
            filetypes=[("Markdown", "*.md"), ("Todos los archivos", "*.*")]
        )
        
        if not output_path:
            self.status.config(text="⊘ Conversión cancelada", bootstyle="warning")
            return
        
        # Verificar si el archivo ya existe
        if os.path.exists(output_path):
            response = messagebox.askyesno(
                "Archivo existe",
                f"¿Sobrescribir '{os.path.basename(output_path)}'?"
            )
            if not response:
                self.status.config(text="⊘ Conversión cancelada", bootstyle="warning")
                return
        
        try:
            self.create_markdown_file(content, output_path)
            
            self.status.config(
                text=f"✓ Guardado: {os.path.basename(output_path)} en {os.path.dirname(output_path)}",
                bootstyle="success"
            )
            messagebox.showinfo(
                "Éxito",
                f"Texto convertido y guardado como:\n\n{output_path}\n\n"
                f"Tamaño: {len(content)} caracteres"
            )
            
            # Limpiar el área de texto después de guardar exitosamente
            self.paste_text.delete(1.0, tk.END)
        
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el archivo:\n{str(e)}")
            self.status.config(text="✗ Error al guardar", bootstyle="danger")
    
    def convert_from_file(self):
        """Convierte un archivo .txt a .md"""
        # Validar que se haya cargado un archivo
        if not self.file_path.get():
            messagebox.showwarning(
                "Advertencia",
                "Primero selecciona un archivo .txt haciendo clic en 'Examinar...'"
            )
            return
        
        input_path = self.file_path.get()
        
        # Sugerir nombre de salida
        base_name = os.path.splitext(os.path.basename(input_path))[0]
        suggested_output = os.path.join(
            os.path.dirname(input_path),
            f"{base_name}.md"
        )
        
        # Dejar que el usuario elija dónde guardar
        output_path = filedialog.asksaveasfilename(
            title="Guardar como archivo Markdown",
            defaultextension=".md",
            initialfile=os.path.basename(suggested_output),
            initialdir=os.path.dirname(suggested_output),
            filetypes=[("Markdown", "*.md"), ("Todos los archivos", "*.*")]
        )
        
        if not output_path:
            self.status.config(text="⊘ Conversión cancelada", bootstyle="warning")
            return
        
        # Verificar si el archivo ya existe
        if os.path.exists(output_path):
            response = messagebox.askyesno(
                "Archivo existe",
                f"¿Sobrescribir '{os.path.basename(output_path)}'?"
            )
            if not response:
                self.status.config(text="⊘ Conversión cancelada", bootstyle="warning")
                return
        
        try:
            # Leer archivo original sin modificaciones
            with open(input_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Crear archivo markdown
            self.create_markdown_file(content, output_path)
            
            self.status.config(
                text=f"✓ Convertido: {os.path.basename(output_path)} en {os.path.dirname(output_path)}",
                bootstyle="success"
            )
            messagebox.showinfo(
                "Éxito",
                f"Archivo convertido y guardado como:\n\n{output_path}\n\n"
                f"Tamaño: {len(content)} caracteres"
            )
        
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo convertir el archivo:\n{str(e)}")
            self.status.config(text="✗ Error en conversión", bootstyle="danger")


def main():
    """Función principal que inicia la aplicación"""
    root = tb.Window(themename="cosmo")
    app = TextToMarkdownApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
