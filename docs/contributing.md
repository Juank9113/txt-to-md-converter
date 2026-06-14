
---

### 📄 `docs/contributing.md` (guía para contribuir)

```markdown
# 🤝 Contribuir al proyecto

¡Gracias por tu interés! Cualquier ayuda es bienvenida, desde reportar un bug hasta mejorar el código o la documentación.

---

## 🌟 ¿Cómo puedes ayudar?

- **Reportar errores** – Abre un issue contando qué pasó.
- **Sugerir mejoras** – Si se te ocurre una funcionalidad nueva, compártela.
- **Mejorar el código** – Haz un fork, modifica y envía un Pull Request.
- **Traducir la documentación** – Si hablas otro idioma, puedes traducir los archivos `.md`.

---

## 🐛 Reportar un bug

1. Ve a la pestaña [Issues](https://github.com/Juank9113/txt-to-md-converter/issues).
2. Haz clic en **New Issue**.
3. Elige la plantilla "Bug report".
4. Explica detalladamente:
   - Qué hiciste.
   - Qué esperabas que pasara.
   - Qué pasó realmente.
   - Si es posible, adjunta una captura de pantalla.

---

## ✨ Sugerir una mejora

1. Abre un [nuevo issue](https://github.com/Juank9113/txt-to-md-converter/issues/new).
2. Usa la plantilla "Feature request".
3. Describe la mejora y por qué sería útil.

---

## 💻 Enviar código (Pull Request)

1. **Haz un fork** del repositorio (botón "Fork" en GitHub).
2. **Clona tu fork**:
```bash
    git clone https://github.com/tu-usuario/txt-to-md-converter.git
    cd txt-to-md-converter
```
3. Crea una rama para tu cambio:
```bash
    git checkout -b mi-mejora
```

4. Realiza tus cambios y haz commit:
```bash
    git add .
    git commit -m "Descripción clara de lo que cambiaste"
```
5. Sube la rama a tu fork:
```bash
   git push origin mi-mejora
```
6. Abre un Pull Request desde tu fork al repositorio original.
---
📝 Estilo de código

    Python 3.8+.

    Sigue la guía PEP 8 (puedes usar black para formatear).

    Comenta las funciones importantes.
---

📚 Mejorar la documentación

La documentación está en la carpeta docs/ y se genera con MkDocs. Para editarla localmente:

    Instala MkDocs: pip install mkdocs mkdocs-material

    Ejecuta mkdocs serve

    Abre http://127.0.0.1:8000 para ver los cambios en vivo.

    Modifica los archivos .md.

    Cuando termines, haz commit y push.

    El sitio se actualizará automáticamente con mkdocs gh-deploy.
---

⭐ ¡Apoya el proyecto con una estrella!

Si te gusta lo que hacemos, por favor, deja una estrella 🌟 en GitHub. Es gratis y nos ayuda muchísimo.

Haz clic aquí para dar ⭐
👨‍💻 Autor

Juan Carlos Blanco Ruiz

    GitHub: @Juank9113

    Email: juancarlosblancoruiz@gmail.com

¡Gracias por contribuir!
text

---

## ✅ Ahora ya tienes todos los archivos completos.

### Resumen de lo que debes hacer:

1. **Crear la estructura de directorios** (si no la tienes):
   ```bash
   mkdir -p docs && touch docs/{index,installation,usage,troubleshooting,contributing}.md mkdocs.yml

2. Copiar el contenido de cada archivo desde este mensaje hacia los archivos correspondientes (usa nano docs/index.md, etc.).

3. Instalar MkDocs si no lo has hecho:
    ```bash
    pip install mkdocs mkdocs-material
    ```
4. Probar localmente:
    ```bash
    mkdocs serve
    ```

5. Publicar en GitHub Pages:
    ```bash
    mkdocs gh-deploy --force
    ```
6. Abrir tu sitio: https://Juank9113.github.io/txt-to-md-converter/


