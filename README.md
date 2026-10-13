# Mercado Local - version Flask

Aplicacion web academica para el catalogo y registro de pedidos de una tienda local. Este proyecto adapta la aplicacion Mercado Local al framework Flask, manteniendo el modelo SQLite y la interfaz del proyecto.

## Arquitectura del modulo

- `mercado_local/__init__.py`: fabrica de aplicacion, configuracion, inicializacion de datos y encabezados HTTP.
- `mercado_local/routes/pages.py`: modulo de presentacion para la pagina principal.
- `mercado_local/routes/catalog.py`: API REST de catalogo y estado.
- `mercado_local/routes/orders.py`: API de pedidos y validacion de origen/payload.
- `mercado_local/store/database.py`: persistencia SQLite, consultas parametrizadas y reglas de pedido.
- `mercado_local/templates/`: plantilla HTML.
- `mercado_local/static/`: CSS y JavaScript.
- `instance/`: base SQLite local, no incluida en el control de versiones.

Se aplica el patron Application Factory de Flask y se separan rutas con Blueprints para facilitar configuracion y mantenimiento por modulo.

## Ambiente

- Python 3.9 o superior.
- Flask 3.1.3.
- SQLite incluido en la biblioteca estandar de Python.

## Instalacion y ejecucion en Windows

Desde la carpeta raiz del proyecto:

```powershell
py -3 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python app.py
```

Abrir `http://127.0.0.1:5000`. La base `instance/tienda.db` se inicializa automaticamente con datos demostrativos.

## Endpoints

- `GET /`: interfaz de la tienda.
- `GET /api/products`: listado del catalogo.
- `POST /api/orders`: registro de pedidos JSON.
- `GET /api/health`: estado del servicio.

El endpoint de pedidos espera `customer`, `email` e `items`, donde cada elemento incluye `product_id` y `quantity`. Precios y totales se calculan usando los datos de la base, no los valores enviados por el navegador.

## Cambios frente al servidor anterior

Se reemplaza el servidor HTTP manual por Flask. Las funciones de base de datos y la interfaz existente se reutilizan; los controladores Flask ahora gestionan rutas, errores HTTP y plantillas. Los Blueprints mantienen catalogo, pedidos y pagina en modulos separados.

## Seguridad y alcance

Los pedidos se limitan a 16 KB, se rechazan origenes distintos del host y se devuelven errores JSON controlados. Se conservan consultas parametrizadas y escape de texto en el navegador. Se agregan cabeceras basicas de seguridad. Es un prototipo local; no integra cuentas, pagos ni despliegue publico. Para produccion se requiere HTTPS, token CSRF, controles de acceso, logging y servidor WSGI de produccion.

## Control de versiones

El codigo se administra con Git en la rama `main`. El ZIP incluye `ENLACE_REPOSITORIO.txt` con el URL proporcionado por el aprendiz: https://github.com/TU_USUARIO/mercado-local-flask.git/. Si `TU_USUARIO` es solo un marcador, debe cambiarse por el usuario real de GitHub. Tambien se incluye un Git bundle portable.

## Verificacion

No se incluyen pruebas automatizadas en esta evidencia. El entorno que genero el proyecto no tiene Flask instalado y no se ejecuto la aplicacion; despues de instalar los requisitos puede iniciarse con `python app.py` y verificarse `/`, `/api/products` y `/api/health` en el navegador.

## Referencias

- Documentacion oficial Flask: https://flask.palletsprojects.com/en/stable/
- Application Factories: https://flask.palletsprojects.com/en/stable/patterns/appfactories/
- Blueprints: https://flask.palletsprojects.com/en/stable/blueprints/

