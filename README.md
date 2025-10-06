---

<div align="center">

# ⚖️ Molinar’slayer

Sitio web del despacho legal construido con Django, internacionalización ES/EN, arquitectura modular por apps y plantillas reutilizables. Elegante, rápido y listo para crecer.  

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-Framework-092E20?logo=django&logoColor=white)](https://www.djangoproject.com/)
![i18n](https://img.shields.io/badge/i18n-gettext-0088CC)
![Status](https://img.shields.io/badge/Status-Active-success)
[![Repo](https://img.shields.io/badge/GitHub-mikeaude1%2FMolinar--slayer-000000?logo=github)](https://github.com/mikeaude1/Molinar-slayer)

</div>

---

## ✨ Características
- Arquitectura por aplicaciones: portal, practiceareas, profiles, costumer, administrator.
- Internacionalización lista: textos marcados con `trans` y archivos `.po` por app.
- Plantillas base y componentes comunes: `base.html`, `header.html`, `footer.html`.
- Estáticos organizados: CSS, imágenes y JS en `static/`.
- Configuración lista para compilar traducciones y levantar servidor de desarrollo.

---

## 🧭 Tabla de contenidos
- [Instalación](#instalación)
- [Ejecución](#ejecución)
- [Internacionalización (i18n)](#internacionalización-i18n)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Rutas principales](#rutas-principales)
- [Despliegue](#despliegue)
- [Buenas prácticas de Git](#buenas-prácticas-de-git)
- [Contribuir](#contribuir)
- [Licencia](#licencia)

---

## 🚀 Instalación
Requisitos:
- Python 3.10+
- pip y virtualenv
- Django
- gettext (msgfmt en PATH para `compilemessages`)

Pasos (Windows):
```powershell
# 1) Crear y activar entorno virtual
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 2) Instalar dependencias
# Si tienes requirements.txt:
pip install -r requirements.txt
# Si no:
pip install Django

# 3) Migraciones
python manage.py migrate
```

---

## ▶️ Ejecución
```powershell
python manage.py runserver
```
- Desarrollo: http://127.0.0.1:8000/

---

## 🌐 Internacionalización (i18n)
- Generar/actualizar mensajes al añadir nuevos `trans`:
```powershell
python manage.py makemessages -l es
```
- Editar traducciones por app:
  - `apps/portal/locale/es/LC_MESSAGES/django.po`
- Compilar:
```powershell
python manage.py compilemessages -l es
```
- Verificar en navegador:
  - Español: http://127.0.0.1:8000/es/aboutus/
  - Inglés:  http://127.0.0.1:8000/en/aboutus/

---

## 🧱 Estructura del proyecto
```text
apps/                # Aplicaciones Django (portal, practiceareas, profiles, costumer, administrator)
layers/              # Configuración del proyecto (settings, urls, wsgi, asgi)
locale/              # Traducciones globales
static/              # CSS, imágenes y scripts
templates/includes/  # Plantillas base y componentes (base, header, footer)
manage.py            # Utilidades de administración
```

---

## 🗺️ Rutas principales
- `/` Página principal
- `/es/aboutus/` About Us en español
- `/en/aboutus/` About Us en inglés
- Otras según apps: `practiceareas`, `profiles`, etc.

---

## 📦 Despliegue (resumen)
- Configura `ALLOWED_HOSTS` y variables de entorno en `layers/settings.py`.
- Compila mensajes antes de desplegar (o asegura gettext en el servidor).
- Recopila y sirve archivos estáticos según tu setup (ej. `collectstatic` si aplicase).

---

## 🔧 Buenas prácticas de Git
- Remoto:
  - origin: `https://github.com/mikeaude1/Molinar-slayer.git`
- Rama por defecto actual: `master`
- `.gitignore` excluye:
  - entornos virtuales, archivos temporales, bases SQLite y archivos `.mo`.
  - Si quieres versionar `.mo`, elimina `*.mo` de `.gitignore`.

---

## 🤝 Contribuir
- PRs e issues son bienvenidos.
- Mantén estilos consistentes y actualiza traducciones cuando añadas nuevos textos.
- Antes de abrir PR:
  - Verifica que el proyecto ejecuta localmente
  - Compila mensajes si añadiste o cambiaste `trans`

---

## 📜 Licencia
- Por definir.