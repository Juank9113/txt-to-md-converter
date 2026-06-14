#!/usr/bin/env python3
# txt_to_md_gui.py - Conversor a Markdown con ttkbootstrap y modo iOS (banner sin resaltos)

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import ttkbootstrap as tb
from ttkbootstrap.widgets.scrolled import ScrolledText
import os
import threading

class TxtToMarkdownApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Conversor TXT a Markdown")
        self.root.geometry("800x700")
        self.root.minsize(700, 600)

        self.file_path = tk.StringVar()
        self.current_theme = tk.StringVar(value="darkly")  # Oscuro por defecto

        self.create_widgets()
        self.root.bind('<Control-v>', lambda e: self.paste_text())
        self.apply_theme()

    def create_widgets(self):
        # ========== BANNER LIMPIO (sin rellenos, sin bootstyle, sin fondos extra) ==========
        # Usamos un Frame normal sin bootstyle para que herede el fondo del tema
        header = tk.Frame(self.root, height=100)
        header.pack(fill=tk.X, pady=0)
        header.pack_propagate(False)

        # Contenedor interno para márgenes
        inner = tk.Frame(header)
        inner.pack(expand=True, fill=tk.BOTH, padx=20, pady=10)

        # Título: sin bootstyle, fuente sans-serif, color automático según tema
        title = tk.Label(
            inner,
            text="Conversor TXT a Markdown",
            font=("Helvetica Neue", 22, "bold"),
            anchor="w"
        )
        title.pack(anchor="w", pady=(0, 5))

        # Subtítulo: sin bootstyle, con ajuste de línea
        subtitle = tk.Label(
            inner,
            text="Convierte texto o archivos .txt a bloque Markdown sin modificar el contenido, sin importar el tamaño del texto",
            font=("Helvetica Neue", 10),
            wraplength=700,
            justify="left",
            anchor="w"
        )
        subtitle.pack(anchor="w")

        # ========== RESTO DE LA INTERFAZ ==========
        self.notebook = tb.Notebook(self.root, bootstyle="primary")
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=15, pady=(10, 15))

        self.tab_paste = tb.Frame(self.notebook)
        self.notebook.add(self.tab_paste, text="📝 Pegar texto", sticky="nsew")
        self.create_paste_tab()

        self.tab_file = tb.Frame(self.notebook)
        self.notebook.add(self.tab_file, text="📂 Cargar archivo", sticky="nsew")
        self.create_file_tab()

        self.progress = ttk.Progressbar(self.root, mode='indeterminate', length=300)

        bottom_frame = tb.Frame(self.root)
        bottom_frame.pack(fill=tk.X, padx=15, pady=(0, 10))

        self.theme_switch = tb.Checkbutton(
            bottom_frame,
            text="🌙 Modo oscuro",
            variable=self.current_theme,
            onvalue="darkly",
            offvalue="cosmo",
            command=self.toggle_theme,
            bootstyle="primary-round-toggle"
        )
        self.theme_switch.pack(side=tk.LEFT, padx=5)

        self.status_label = tb.Label(bottom_frame, text="✅ Listo", font=("Helvetica", 9), bootstyle="info")
        self.status_label.pack(side=tk.RIGHT, padx=10)

        self.create_tooltips()

        # Forzar que el fondo del header se actualice al cambiar de tema
        self.update_header_bg()

    def update_header_bg(self):
        """Actualiza el fondo del header según el tema actual (sin usar bootstyle)."""
        # Obtenemos el color de fondo del tema actual
        bg_color = self.root.style.lookup('TFrame', 'background')
        header = self.root.children.get('!frame')  # El header es el primer Frame creado
        if header:
            header.configure(bg=bg_color)
            # También actualizamos los frames internos
            for child in header.winfo_children():
                child.configure(bg=bg_color)
                for subchild in child.winfo_children():
                    if isinstance(subchild, (tk.Label, tk.Frame)):
                        subchild.configure(bg=bg_color)

    def toggle_theme(self):
        new_theme = self.current_theme.get()
        self.root.style.theme_use(new_theme)
        # Actualizar texto del interruptor y etiqueta de estado
        if new_theme == "darkly":
            self.theme_switch.config(text="🌙 Modo oscuro")
            self.status_label.config(text="Tema oscuro activado", bootstyle="info")
        else:
            self.theme_switch.config(text="☀️ Modo claro")
            self.status_label.config(text="Tema claro activado", bootstyle="info")
        # Actualizar el fondo del header para que coincida con el nuevo tema
        self.update_header_bg()

    def apply_theme(self):
        self.root.style.theme_use(self.current_theme.get())
        self.update_header_bg()

    def create_paste_tab(self):
        tb.Label(self.tab_paste, text="Pega tu texto aquí:", font=("Helvetica", 10, "bold")).pack(anchor=tk.W, padx=10, pady=(10,5))
        self.paste_text = ScrolledText(self.tab_paste, height=18, wrap=tk.WORD, font=("Courier New", 10))
        self.paste_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        btn_frame = tb.Frame(self.tab_paste)
        btn_frame.pack(pady=10)
        self.convert_btn = tb.Button(btn_frame, text="✨ Convertir a Markdown", command=self.convert_from_paste, bootstyle="success", width=20)
        self.convert_btn.pack(side=tk.LEFT, padx=5)
        tb.Button(btn_frame, text="🗑️ Limpiar", command=lambda: self.paste_text.delete(1.0, tk.END), bootstyle="secondary", width=15).pack(side=tk.LEFT, padx=5)
        tb.Label(self.tab_paste, text="💡 Tip: Usa Ctrl+V para pegar texto", font=("Helvetica", 8), bootstyle="secondary").pack(pady=5)

    def create_file_tab(self):
        top_frame = tb.Frame(self.tab_file)
        top_frame.pack(fill=tk.X, padx=10, pady=10)
        tb.Label(top_frame, text="Archivo .txt:", font=("Helvetica", 10, "bold")).pack(side=tk.LEFT, padx=5)
        self.file_entry = tb.Entry(top_frame, textvariable=self.file_path, width=50)
        self.file_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        tb.Button(top_frame, text="Examinar...", command=self.load_file, bootstyle="primary").pack(side=tk.LEFT, padx=5)

        tb.Label(self.tab_file, text="Vista previa del contenido:", font=("Helvetica", 10, "bold")).pack(anchor=tk.W, padx=10, pady=(10,0))
        self.text_area = ScrolledText(self.tab_file, height=15, wrap=tk.WORD, font=("Courier New", 10))
        self.text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        btn_frame = tb.Frame(self.tab_file)
        btn_frame.pack(pady=10)
        self.convert_file_btn = tb.Button(btn_frame, text="📦 Convertir archivo a .md", command=self.convert_from_file, bootstyle="success", width=25)
        self.convert_file_btn.pack()

    def create_tooltips(self):
        def show_tooltip(event, text):
            tooltip = tk.Toplevel(self.root)
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
            tb.Label(tooltip, text=text, bootstyle="info", relief="solid", borderwidth=1).pack()
            self.root.after(1500, tooltip.destroy)
        self.convert_btn.bind("<Enter>", lambda e: show_tooltip(e, "Convierte el texto a .md con bloque markdown"))
        self.convert_file_btn.bind("<Enter>", lambda e: show_tooltip(e, "Convierte el archivo cargado a .md"))

    def start_progress(self):
        self.progress.pack(fill=tk.X, padx=15, pady=(0,10))
        self.progress.start(10)

    def stop_progress(self):
        self.progress.stop()
        self.progress.pack_forget()

    def load_file(self):
        filename = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt"), ("Todos", "*.*")])
        if filename:
            self.file_path.set(filename)
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, content)
                self.status_label.config(text=f"✅ Cargado: {os.path.basename(filename)}", bootstyle="success")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo leer:\n{str(e)}")
                self.status_label.config(text="❌ Error", bootstyle="danger")

    def convert_from_file(self):
        if not self.file_path.get():
            messagebox.showwarning("Advertencia", "Primero carga un archivo .txt")
            return
        input_path = self.file_path.get()
        output_path = input_path.replace('.txt', '.md')
        if output_path == input_path:
            output_path = input_path + '.md'

        def convert():
            try:
                self.start_progress()
                self.status_label.config(text="⏳ Convirtiendo...", bootstyle="info")
                with open(input_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                wrapped = f"```markdown\n{content}\n```\n"
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(wrapped)
                self.stop_progress()
                self.status_label.config(text=f"✅ Convertido: {os.path.basename(output_path)}", bootstyle="success")
                messagebox.showinfo("Éxito", f"Archivo guardado como:\n{output_path}")
            except Exception as e:
                self.stop_progress()
                self.status_label.config(text="❌ Error", bootstyle="danger")
                messagebox.showerror("Error", f"No se pudo convertir:\n{str(e)}")
        threading.Thread(target=convert, daemon=True).start()

    def convert_from_paste(self):
        content = self.paste_text.get(1.0, tk.END).strip()
        if not content:
            messagebox.showwarning("Advertencia", "No hay texto pegado")
            return
        output_path = filedialog.asksaveasfilename(defaultextension=".md", filetypes=[("Markdown", "*.md")])
        if not output_path:
            return

        def convert():
            try:
                self.start_progress()
                self.status_label.config(text="⏳ Convirtiendo...", bootstyle="info")
                wrapped = f"```markdown\n{content}\n```\n"
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(wrapped)
                self.stop_progress()
                self.status_label.config(text=f"✅ Guardado: {os.path.basename(output_path)}", bootstyle="success")
                messagebox.showinfo("Éxito", f"Texto guardado como:\n{output_path}")
            except Exception as e:
                self.stop_progress()
                self.status_label.config(text="❌ Error", bootstyle="danger")
                messagebox.showerror("Error", f"No se pudo guardar:\n{str(e)}")
        threading.Thread(target=convert, daemon=True).start()

    def paste_text(self):
        try:
            clipboard = self.root.clipboard_get()
            self.paste_text.insert(tk.INSERT, clipboard)
            self.status_label.config(text="📋 Texto pegado", bootstyle="info")
        except:
            pass

if __name__ == "__main__":
    root = tb.Window(themename="darkly", title="Conversor TXT a Markdown")
    app = TxtToMarkdownApp(root)
    root.mainloop()