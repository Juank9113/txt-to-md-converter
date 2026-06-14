# 🐛 Solución de problemas

Aquí tienes las dudas más frecuentes y cómo resolverlas **sin perder tiempo**.

---

## ❌ Error al ejecutar `python3 txt_to_md_gui.py`

### "No such file or directory"
- **Causa**: No estás en la carpeta correcta o el archivo no existe.
- **Solución**:
  ```bash
  cd ~/ruta/donde/descargaste/txt-to-md-converter
  ls -la   # Deberías ver txt_to_md_gui.py
  python3 txt_to_md_gui.py