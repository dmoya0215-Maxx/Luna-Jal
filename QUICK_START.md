# 🚀 Guía Rápida de Inicio

## ⚡ 5 Pasos para Comenzar

### 1. **Archivos Creados** ✅

Ya todos los archivos están en tu proyecto:

```
templates/
├── login.html              # Página de login
└── dashboard.html          # Dashboard

static/
├── css/
│   ├── login.css          # Estilos login
│   ├── dashboard.css      # Estilos dashboard
│   └── global.css         # Estilos globales y utilidades
└── js/
    ├── login.js           # Lógica login
    └── dashboard.js       # Lógica dashboard + gráficos
```

### 2. **Configurar URLs** 🔗

En tu archivo `urls.py` principal:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tu_app.urls')),  # Asegúrate de incluir tus URLs
]
```

En tu archivo `tu_app/urls.py`:

```python
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),
]
```

### 3. **Crear las Vistas** 🎯

Copia el contenido del archivo `ejemplo_views.py` a tu `views.py`:

```python
# Básico para que funcione
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

def login_view(request):
    if request.method == 'POST':
        # Tu lógica de login
        pass
    return render(request, 'login.html')

@login_required(login_url='login')
def dashboard_view(request):
    return render(request, 'dashboard.html')
```

### 4. **Incluir CSS y JS** 📦

En Django, asegúrate de que tus templates usen:

```html
{% load static %}

<!-- En el <head> -->
<link rel="stylesheet" href="{% static 'css/login.css' %}">

<!-- Antes de cerrar </body> -->
<script src="{% static 'js/login.js' %}"></script>
```

**Nota**: El dashboard incluye Chart.js automáticamente desde CDN.

### 5. **Ejecutar y Probar** ✨

```bash
# Recolectar archivos estáticos (si estás en producción)
python manage.py collectstatic

# Ejecutar servidor de desarrollo
python manage.py runserver

# Ir a http://localhost:8000/login/
```

---

## 🎨 Personalización Rápida

### Cambiar Colores Primarios

Edita `static/css/dashboard.css` línea 14:

```css
:root {
    --primary-color: #64c8ff;      /* Tu color aquí */
    --secondary-color: #ff006e;
    --accent-color: #b640e0;
}
```

### Cambiar Títulos

En `templates/dashboard.html`:

```html
<!-- Línea ~49 -->
<h2>CRM Dashboard</h2>  <!-- Cambia esto -->

<!-- O línea ~173 -->
<h1>Dashboard Overview</h1>  <!-- Y esto -->
```

### Agregar Más Gráficos

En `templates/dashboard.html`, copia y pega una tarjeta de gráfico:

```html
<div class="chart-card">
    <h3>Mi Nuevo Gráfico</h3>
    <canvas id="miGrafico"></canvas>
</div>
```

En `static/js/dashboard.js`, agrega en `initializeCharts()`:

```javascript
if (document.getElementById('miGrafico')) {
    crearMiGrafico();  // Tu función de gráfico
}
```

---

## 📱 Probar Responsividad

### En Chrome/Firefox:
1. Abre DevTools (F12)
2. Haz clic en icono de dispositivo (responsive mode)
3. Cambia entre tamaños: Mobile (375px), Tablet (768px), Desktop (1200px+)

### O redimensiona la ventana del navegador

---

## 🔍 Verificar que Todo Funciona

### Checklist de Pruebas:

- [ ] ✅ Página de login se ve bien
- [ ] ✅ Campos de entrada responden al focus
- [ ] ✅ Botón "Log in" es clickeable
- [ ] ✅ "Remember me" guarda el email
- [ ] ✅ Dashboard carga después de login
- [ ] ✅ Sidebar es navegable
- [ ] ✅ Gráficos aparecen con datos
- [ ] ✅ Responsive en móvil (F12 → toggle device toolbar)
- [ ] ✅ Colores se ven bien con el tema oscuro
- [ ] ✅ Transiciones y animaciones funcionan suave

---

## 🐛 Si Algo No Funciona

### Los estilos no se aplican

```bash
# Limpia la caché y recarga
python manage.py collectstatic --clear --noinput

# En desarrollo, asegúrate de:
# 1. Que DEBUG = True en settings.py
# 2. Que STATIC_URL = '/static/' en settings.py
# 3. Que los archivos estén en static/css/ y static/js/
```

### Los gráficos están en blanco

1. Abre la consola (F12 → Console)
2. Busca errores de JavaScript
3. Verifica que Chart.js está cargando: `https://cdn.jsdelivr.net/npm/chart.js`
4. Asegúrate que los canvas tienen los IDs correctos

### El responsive no funciona

Verifica que en el HTML hay:
```html
<meta name="viewport" content="width=device-width, initial-scale=1.0">
```

---

## 💡 Tips y Trucos

### Cambiar Tema a Claro (Light Mode)

Crea un archivo `static/css/light.css` con:

```css
:root {
    --dark-bg: #ffffff;
    --card-bg: rgba(240, 240, 255, 0.8);
    --text-primary: #1a1a2e;
    --text-secondary: #5a5a7a;
}
```

Luego en el template:
```html
<link rel="stylesheet" href="{% static 'css/dashboard.css' %}">
<link rel="stylesheet" href="{% static 'css/light.css' %}">
```

### Agregar Más Usuarios de Prueba

```python
# En Django shell
python manage.py shell

from django.contrib.auth.models import User
User.objects.create_user(
    username='testuser',
    email='test@example.com',
    password='testpass123'
)
```

### Depuración de JavaScript

En `static/js/dashboard.js` o `login.js`, agrega:

```javascript
console.log('Dashboard cargado');
console.log('Usuario autenticado:', document.body.dataset);
```

---

## 📚 Archivos de Referencia

| Archivo | Propósito |
|---------|-----------|
| `login.html` | Página de login |
| `dashboard.html` | Dashboard principal |
| `login.css` | Estilos login |
| `dashboard.css` | Estilos dashboard |
| `global.css` | Utilidades globales |
| `login.js` | Validación y lógica login |
| `dashboard.js` | Interactividad y gráficos |
| `ejemplo_views.py` | Referencia de vistas |
| `README_DESIGN.md` | Documentación completa |

---

## 🎯 Próximos Pasos

1. **Personaliza los colores** según tu marca
2. **Agrega tus datos** a los gráficos
3. **Configura tu autenticación** (email/password)
4. **Añade más páginas** siguiendo el mismo patrón
5. **Despliega a producción** (Heroku, PythonAnywhere, etc.)

---

## 🚀 Estás Listo!

Tu sistema web responsivo está listo para usar. Ahora:

1. Prueba el login
2. Navega el dashboard
3. Personaliza según necesites
4. ¡Disfruta!

---

**¿Necesitas ayuda?** Revisa `README_DESIGN.md` para documentación completa.
