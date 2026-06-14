# 🔧 Instalación

Sigue esta guía sin saltarte ningún paso. **Funciona en Windows, Linux y macOS**.

## 📋 Requisitos previos

- **Python 3.8 o superior** – [Descargar Python](https://python.org)
- **pip** (viene incluido con Python)

> 🧪 **Para verificar si ya los tienes**, abre una terminal y escribe:
> ```bash
> python3 --version
> pip3 --version
> ```

## 📥 Pasos de instalación

### 1. Clonar el repositorio (o descargar el código)

```bash
git clone https://github.com/Juank9113/txt-to-md-converter.git
cd txt-to-md-converter
```

### 2. Instalar la única dependencia

```bash
pip install ttkbootstrap
```
### En algunos sistemas usa pip3:

```bash
pip3 install ttkbootstrap
```

### 3. Ejecutar la aplicación
```bash
python3 txt_to_md_gui.py
```
¡La ventana principal debería aparecer!

## 🐛 Si algo sale mal
|Problemas |Solución|
|---------|---------------|
|ModuleNotFoundError: No module named 'ttkbootstrap'	    |Ejecuta pip3 install ttkbootstrap otra vez. Si persiste, prueba python3 -m pip install ttkbootstrap.|
|can't open file 'txt_to_md_gui.py'	|Asegúrate de estar dentro de la carpeta correcta con cd txt-to-md-converter.|
|TclError: no display name and no $DISPLAY environment variable (Linux sin interfaz)	|Necesitas ejecutar la GUI en un entorno con pantalla (no SSH sin X forwarding).|

⭐ ¿Te funcionó? ¡Apóyanos con una estrella!

Haz clic aquí para dar ⭐ en GitHub
👤 Autor

Juan Carlos Blanco Ruiz – @Juank9113 – juancarlosblancoruiz@gmail.com