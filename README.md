# 🕸️ Scraping Distribuido con Actores en Python (Pykka)

Este proyecto implementa un sistema de scraping distribuido utilizando el modelo de **actores con Pykka**, un **servidor TCP en Python**, y consultas a **MercadoLibre** para obtener información sobre productos.

Es ideal como ejemplo de arquitectura reactiva, procesamiento paralelo y comunicación entre actores.

## 🧠 ¿Cómo funciona?

- Un **servidor TCP/IP** espera conexiones de clientes.
- El cliente puede enviar una solicitud con varias consultas de productos.
- Por cada consulta, se crea un actor que realiza **web scraping** a MercadoLibre.
- Cada resultado es devuelto al cliente de forma ordenada y gestionada por actores secundarios (handlers).

## 🛠️ Tecnologías utilizadas

- 🐍 **Python 3.10+**
- 🎭 **Pykka** (modelo de actores)
- 🌐 **requests** y **BeautifulSoup** para scraping
- 🧵 **socket** y **threading** para la comunicación cliente-servidor

## 📦 Instalación

1. Cloná el repositorio:

```bash
git clone https://github.com/tu-usuario/scraping-actores-pykka.git
cd scraping-actores-pykka
Instalá las dependencias:

bash
Copiar
Editar
pip install -r requirements.txt
Contenido de requirements.txt:

nginx
Copiar
Editar
pykka
requests
beautifulsoup4
🚀 Cómo ejecutar
Iniciá el servidor:

bash
Copiar
Editar
python servidor.py
El servidor estará escuchando en la dirección:

ini
Copiar
Editar
host = 192.168.1.15
port = 8786
Asegurate de que el firewall permita conexiones a ese puerto o ajustalo a localhost para pruebas locales.

Enviá una solicitud desde un cliente TCP con el formato:

nginx
Copiar
Editar
scrape zapatillas,nike,auriculares
Los actores se encargarán de buscar esos términos en MercadoLibre y enviar los resultados al cliente.

📤 Estructura general
css
Copiar
Editar
ServidorActor         → Maneja la conexión del cliente.
└── ClientRequestActor → Crea un Scraper por cada consulta.
    └── ScraperMercadoLibre → Realiza el scraping en paralelo.
    └── ResultHandler → Envia los resultados al cliente.
✅ Ejemplo de salida
yaml
Copiar
Editar
Request 1:
Zapatillas Deportivas: $15.000
Zapatillas Urbanas: $18.000

Request 2:
Nike Air Max: $30.000
Nike Revolution: $25.000
...
📚 Aprendizajes clave
Uso del patrón actor para programación concurrente.

Integración de scraping con concurrencia real.

Comunicación por sockets entre cliente-servidor.

💡 Ideas futuras
Crear una interfaz gráfica para enviar consultas.

Exportar los resultados a un archivo CSV o base de datos.

Añadir manejo de múltiples clientes simultáneos.

📬 Contribuciones
Este proyecto es un experimento académico y está abierto a mejoras.
¡Sos bienvenido/a a colaborar, probar y proponer ideas!

