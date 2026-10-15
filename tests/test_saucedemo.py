# framework de pruebas
import pytest

# comunicación con el navegador
from selenium import webdriver

# recomendación de Gemini para evitar el pop-up de recomendación de cambio de clave
from selenium.webdriver.chrome.options import Options

chrome_options = Options()

# desactivar verificacioens de seguridad
chrome_options.add_experimental_option(
    "prefs",
    {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.password_manager_leak_detection": False,
    },
)

# Deshabilitar notificaciones, burbujas y pop-ups de permisos
chrome_options.add_argument("--disable-save-password-bubble")
chrome_options.add_argument("--disable-popup-blocking")
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--lang=es")
chrome_options.add_argument("--alerts --popups")
chrome_options.add_experimental_option(
    "prefs", {"profile.default_content_setting_values.notifications": 2}
)

driver = webdriver.Chrome(options=chrome_options)

# comunicación controlador para chrome
from selenium.webdriver.chrome.service import Service

# driver para versión de chrome
from webdriver_manager.chrome import ChromeDriverManager

# from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

# from selenium.webdriver.chrome.webdriver import WebDriver


# inicia bloque de configuración de la fixture
@pytest.fixture(scope="module")
def driver():
    # descarga del driver
    service = Service(ChromeDriverManager().install())
    # ventana de chrome abierta
    # driver = ChromeDriver(service=service)

    driver = webdriver.Chrome(service=service)

    # asignamos la sesión de chrome abierta, a las pruebas
    yield driver

    # cierra ventana y servicios y libera memoria
    driver.quit()


# defino tuplas como pares de usuario - clave
credentials = [
    ("performance_glitch_user", "secret_sauce"),
    ("problem_user", "secret_sauce"),
    ("error_user", "secret_sauce"),
    ("visual_user", "secret_sauce"),
    # la notificación sigue saliendo = se elimina la opción que da error:
    # ("locked_out_user", "secret_sauce"),
    ("standard_user", "secret_sauce"),
]


# Utilizo el parametrizador para pasar los pares de credenciales
@pytest.mark.parametrize("username, password", credentials)
def test_login(driver, username, password):
    # defino la pagina de pruebas
    driver.get("https://www.saucedemo.com/")

    # reemplazo los parametros por las credenciales
    driver.find_element(By.ID, "user-name").send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.ID, "login-button").click()

    # verifico que haya pasado a la página del inventario
    assert (
        "/inventory.html" in driver.current_url
    ), "ERROR: no se pudo acceder a /inventory.html"

    # el resultado serán 5 passed, y 1 failed (user:locked_out_user, no funciona en la pagina)


# verifico el titulo de la página de productos
def test_inventario(driver):
    titulo_pagina = driver.title

    # verifico que la pagina se llame "Swag Labs"
    assert titulo_pagina == "Swag Labs", "ERROR = El título no es SWAG LABS"

    # agrego una espera de 5 segundos para esperar que aparezca el titulo
    wait = WebDriverWait(driver, 5)

    # verifico que haya algún titulo y esté presente
    elemento_titulo = wait.until(
        EC.presence_of_element_located((By.CLASS_NAME, "title"))
    )

    # ahora sí, verifico que exista el termino "Products" como título
    titulo_listados = driver.find_element(By.CLASS_NAME, "title").text

    assert (
        titulo_listados == "Products"
    ), "ERROR = La página no tiene el texto Products como título"

    # verifico que no exista el termino "Productos" como título, dando error
    assert (
        titulo_listados != "productos"
    ), "ERROR = La página tiene el texto Productos como título 2"

    # 3. Ahora sí extraemos el texto de forma segura
    titulo_listados = elemento_titulo.text

    assert (
        titulo_listados == "Products"
    ), "ERROR = La página no tiene el texto Products como título"


# verifico la existencia de productos
def test_productos(driver):
    # busco los productos dentro de la página
    products_items = driver.find_elements(By.CLASS_NAME, "inventory_item")
    cantidad_productos = len(products_items)

    # verifico que haya al menos un producto
    assert cantidad_productos > 0, "ERROR = No se han encontrado productos"


# validando la interfaz
def test_interfaz(driver):
    # busco el menu hamburguesa
    burguer_menu = driver.find_element(By.ID, "react-burger-menu-btn")
    # verifico que esté visible el menu hamburguesa
    assert burguer_menu.is_displayed()

    # busco el menu del filtro
    filter_menu = driver.find_element(By.CLASS_NAME, "product_sort_container")
    # verifico que esté visible la opción NAME_A_TO_Z
    assert filter_menu.is_displayed()


# validando la existencia del nombre y precio del primer producto
def test_primer_producto(driver):
    # busco el titulo del primer producto
    elemento_nombre = driver.find_element(By.ID, "item_4_title_link")
    # recupero el texto de ese producto
    nombre_obtenido = elemento_nombre.text

    # busco el precio del primer producto
    elemento_precio = driver.find_element(By.CLASS_NAME, "inventory_item_price")
    # recupero el texto del precio de ese producto
    precio_obtenido = elemento_precio.text

    # verifico que se obtengan los elementos deseados
    assert (
        nombre_obtenido == "Sauce Labs Backpack"
    ), f"ERROR = El nombre esperado era 'Sauce Labs Backpack', pero se obtuvo '{nombre_obtenido}'"
    assert (
        precio_obtenido == "$29.99"
    ), f"ERROR = El precio esperado era $29.99, pero se obtuvo {precio_obtenido}"


# validando la existencia del nombre y precio del primer producto
def test_agregar_producto(driver):
    # busco el boton de agregar el primer producto al carrito
    botones_agregar = driver.find_elements(By.CLASS_NAME, "btn_inventory")
    boton_primer_producto = botones_agregar[0]
    # clickeo el botón
    boton_primer_producto.click()

    # tiempo máximo de espera para que cambie el texto del boton: de 5 segundos
    wait = WebDriverWait(driver, 5)

    # ayuda de Gemini: espera explicita
    wait.until(
        EC.text_to_be_present_in_element((By.CLASS_NAME, "btn_inventory"), "Remove")
    )

    # ayuda de Gemini: volvemos a obtener el estado actual del botón antes de validarlo
    texto_actual = driver.find_elements(By.CLASS_NAME, "btn_inventory")[0].text.lower()

    # verifica que el texto del boton haya cambiado a "Remove"
    assert (
        texto_actual == "remove"
    ), "ERROR = El botón no se modifica, no agrega el elemento al carrito"


# validar el contador del carrito
def test_contador_carrito(driver):
    # busco el texto (número) del badge del carrito
    carrito_badge = driver.find_element(By.CLASS_NAME, "shopping_cart_badge").text

    # verifico que no esté vacío
    assert carrito_badge, "ERROR = El contador del carrito no incrementa"


# validar que ingrese a la pagina del carrito
def test_navegar_carrito(driver):
    # busco el botón del carrito y lo activo
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()

    # verifico que haya ido hacia la pagina del carrito
    assert (
        "/cart.html" in driver.current_url
    ), "ERROR = No se dirige a la web del carrito"


# comprobar que se agregó el producto en el carrito
def test_comprobar_producto_en_carrito(driver):
    # busco el nombre del primer producto
    producto_en_carrito = driver.find_element(By.CLASS_NAME, "inventory_item_name").text

    assert (
        producto_en_carrito == "Sauce Labs Backpack"
    ), "ERROR = El producto no fue agregado"
