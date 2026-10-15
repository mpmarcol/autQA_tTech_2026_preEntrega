# Automatización QA - 2026, 2do cuatrimestre
# Pre Entrega 

## Propósito del proyecto

El propósito de este proyecto es aplicar los conocimientos del curso para automatizar flujos básicos de navegación web en la página "saucedemo.com". 

Busco validar, simulando las acciones de un usuario real, tres caminos principales dentro de la aplicación: el inicio de sesión, la verificación del catálogo de productos y el uso del carrito de compras. A través de esto, aplico estrategias de localización, interacción con elementos y validación de estados en la página.

---

## Tecnologías utilizadas

Para este proyecto utilizo las siguientes herramientas:

- **Python**: como lenguaje principal.
- **Pytest**: para la estructura del testing y aserciones.
- **Selenium WebDriver**: para la comunicación y automatización con el navegador.
- **WebDriver Manager**: para descargar y gestionar el driver de Chrome automáticamente.
- **Git y GitHub**: para el control de versiones y entrega del código.
- **Pytest-HTML**: para generar el reporte visual de las pruebas.

---

## Estructura del proyecto

El proyecto está organizado siguiendo los criterios solicitados, en la siguiente estructura de carpetas:

```text
pre-entrega-automation-testing-[nombre-apellido]/
│
├── reports/
│   └── reporte.html
├── tests/
│   └── test_saucedemo.py
├── utils/
└── README.md
```

---

## Características implementadas y Casos de Prueba

Basado en los criterios mínimos del enunciado, desarrollo las siguientes validaciones:

### 1. Automatización de Login
- Defino la página de pruebas y navego hacia el login.
- Ingreso credenciales válidas (usuario `standard_user` y contraseña `secret_sauce`). Utilizo el parametrizador para pasar distintos pares de credenciales.
- Verifico el login exitoso validando que haya pasado a la ruta `/inventory.html`.
- Agrego una espera explícita para asegurar la carga y valido la presencia de los títulos "Swag Labs" y "Products".

### 2. Navegación y verificación del catálogo
- Verifico que el título de la página de inventario sea correcto.
- Busco los productos dentro de la página y compruebo que haya al menos uno visible.
- Valido la interfaz, verificando que estén presentes el menú hamburguesa y el menú del filtro.
- Busco y recupero el texto para listar el nombre y el precio del primer producto de la lista.

### 3. Interacción con productos (Carrito)
- Busco el botón de agregar el primer producto y lo clickeo.
- Ayuda de Gemini: utilizo una espera explícita para verificar que el botón cambie su texto a "Remove".
- Verifico que el contador del badge del carrito se incremente (que no esté vacío).
- Navego hacia el carrito clickeando el link.
- Compruebo que el producto se haya agregado buscando su nombre dentro de la página del carrito.

### Extras (Configuraciones)
- Inicia un bloque de configuración de la fixture para abrir la sesión de Chrome y luego cerrar ventana y liberar memoria.
- Agrego opciones (chrome_options) para deshabilitar notificaciones, burbujas y evitar el pop-up de recomendación de cambio de clave de Chrome que interfiere con las pruebas.

---

## Instalación de dependencias

Antes de correr las pruebas, fue necesario instalar las librerías que utilizo en el framework.

1. Clonar el repositorio y abrir una terminal en la carpeta raíz.
2. Instalar las dependencias ejecutando:

```bash
pip install selenium pytest pytest-html webdriver-manager
```

---

## Ejecución de las pruebas

Una vez instaladas las herramientas, las pruebas se corrierondesde la terminal. 

Para ejecutar todas las pruebas y ver el detalle paso a paso en la consola, utilicé:
```bash
python.exe -m pytest .\tests\test_saucedemo.py -v 
```

## Generación de reportes

Para generar un reporte en HTML con los resultados de la ejecución (aprobados, fallados y tiempos), utilizo el siguiente comando:

```bash
python.exe -m pytest .\tests\test_saucedemo.py -v --html=reports/reporte.html --self-contained-html
```

El resultado se guardará como `reporte.html` dentro de la carpeta `reports/`.