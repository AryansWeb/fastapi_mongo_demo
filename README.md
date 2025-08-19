# 🚀 API RESTful con FastAPI, MongoDB y Despliegue en Azure

*Desarrollado por: [@vicogarcia16](https://github.com/vicogarcia16)*

---

### 🌐 Demo en Vivo

Puedes interactuar con la API desplegada en Azure aquí:

**[https://fastapi-mongo-vic-dkbkg8bea9hrhheu.eastus-01.azurewebsites.net/](https://fastapi-mongo-vic-dkbkg8bea9hrhheu.eastus-01.azurewebsites.net/)**

La documentación interactiva (Swagger UI) se encuentra en la ruta raíz.

---

Este proyecto demuestra el desarrollo de una API escalable y lista para producción, construida con un stack tecnológico moderno y siguiendo las mejores prácticas de la industria.

La aplicación gestiona una API para productos y usuarios, implementando operaciones CRUD, un sistema de autenticación robusto, y funcionalidades avanzadas de búsqueda y agregación. El proyecto está completamente contenerizado y desplegado en la nube de Microsoft Azure.

## 🛠️ Arquitectura y Habilidades Demostradas

Este repositorio es una muestra práctica de las siguientes capacidades técnicas:

- **Python Avanzado:** El código está desarrollado en Python 3.11, utilizando **tipado estático** para robustez y **programación asíncrona** en todo el framework para optimizar el performance.

- **Experiencia en FastAPI:**
  - **Ruteo y Dependencias:** Uso del sistema de Inyección de Dependencias de FastAPI para una lógica limpia y reutilizable.
  - **Seguridad:** Implementación de seguridad **OAuth2 con tokens JWT** para proteger endpoints.
  - **Documentación Automática:** Generación de documentación interactiva bajo el estándar **OpenAPI**.

- **Modelado y Validación de Datos con Pydantic:** Se utiliza Pydantic para la **validación estricta** de los datos de entrada y la **serialización** de las respuestas, garantizando la integridad de los datos que fluyen a través de la API.

- **Bases de Datos NoSQL - MongoDB:**
  - **Modelado de Colecciones:** Se utiliza el ODM **Beanie** (basado en Pydantic y Motor) para definir los esquemas de las colecciones de forma declarativa y asíncrona.
  - **Interacción Asíncrona:** Todas las operaciones con la base de datos son no bloqueantes.
  - **Optimización de Consultas:** Creación de **índices** (incluyendo índices de texto) para acelerar las búsquedas y filtros.
  - **Agregaciones:** Uso del **Aggregation Framework** de MongoDB para realizar cálculos complejos en el servidor.

- **Pruebas de Calidad de Código:**
  - **Testing:** El proyecto incluye una suite de **pruebas unitarias y de integración** desarrolladas con **Pytest** (ver directorio `/tests`).
  - **Linters:** Se usa **Ruff** para mantener un código limpio, consistente y libre de errores comunes.

- **Contenerización con Docker:** La aplicación está completamente contenerizada, con un `Dockerfile` optimizado para crear entornos de producción ligeros y seguros.

- **Despliegue en Cloud (Azure):** El proyecto está desplegado en **Azure**, demostrando experiencia en:
  - **Despliegue de Contenedores:** Uso de **Azure App Service for Containers**.
  - **Gestión de Imágenes:** Almacenamiento y versionado de imágenes en **Azure Container Registry**.
  - **Base de Datos Gestionada:** Uso de **Azure Cosmos DB (API para MongoDB)**.
  - **Gestión de Secretos:** Configuración segura de variables de entorno en el servicio de nube.

---

## 📂 Estructura del Proyecto

```
fastapi_mongo_demo/
├── app/                    # Directorio principal de la aplicación FastAPI
│   ├── core/               # Configuración central, excepciones, etc.
│   ├── db/                 # Conexión a la base de datos
│   ├── dependencies/       # Dependencias reutilizables
│   ├── models/             # Modelos de datos (Beanie/Pydantic)
│   ├── routes/             # Lógica de los endpoints de la API
│   ├── schemas/            # Esquemas Pydantic para validación
│   └── utils/              # Funciones de utilidad (ej. auth)
├── tests/                  # Pruebas unitarias y de integración
├── .dockerignore           # Archivos a ignorar por Docker
├── .gitignore              # Archivos a ignorar por Git
├── Dockerfile              # Define el contenedor de la aplicación
├── Pipfile                 # Dependencias del proyecto para Pipenv
└── README.md               # Este archivo
```

## 📡 Endpoints Principales de la API

La documentación completa e interactiva se encuentra en la ruta raíz (`/`) una vez que la aplicación está en ejecución.

| Verbo      | Ruta                                      | Descripción                                                                                                     |
|------------|-------------------------------------------|-----------------------------------------------------------------------------------------------------------------|
| **GET**    | `/health`                                 | Endpoint de verificación de salud de la aplicación y conectividad con MongoDB.                                 |
| **POST**   | `/api/v1/auth/register`                   | Registra un nuevo usuario.                                                                                      |
| **POST**   | `/api/v1/auth/login`                      | Inicia sesión y obtiene un token JWT.                                                                           |
| **GET**    | `/api/v1/products/`                       | Obtiene una lista de productos. Permite filtrar por `min_price`, `max_price` y `query` (búsqueda por texto). |
| **POST**   | `/api/v1/products/`                       | Crea un nuevo producto (requiere autenticación).                                                                |
| **GET**    | `/api/v1/products/aggregation/by_user`    | Agrega la cantidad de productos creados por cada usuario.                                                       |
| **GET**    | `/api/v1/products/{product_id}`           | Obtiene un producto por su ID.                                                                                  |
| **PUT**    | `/api/v1/products/{product_id}`           | Actualiza un producto (requiere autenticación).                                                                 |
| **DELETE** | `/api/v1/products/{product_id}`           | Elimina un producto (requiere autenticación).                                                                   |

---

## ⚙️ Guía de Instalación Local

### 1. Prerrequisitos

- Python 3.11, Pipenv y una instancia de MongoDB.

### 2. Pasos

1. **Clonar el repositorio**
   ```bash
   git clone <URL-del-repositorio>
   cd fastapi_mongo_demo
   ```

2. **Instalar dependencias** (se utiliza `pipenv` para la gestión de dependencias y entornos virtuales):
   ```bash
   pipenv install
   pipenv shell
   ```

3. **Configurar variables de entorno**: Crear un archivo `.env` a partir del siguiente ejemplo y llenarlo con los datos correspondientes.
   ```ini
   # Configuración de la base de datos
   MONGO_URI="mongodb://localhost:27017"
   MONGO_DB="fastapi_demo"

   # Secretos para la autenticación JWT
   SECRET_KEY="tu_clave_super_secreta_aqui"
   ALGORITHM="HS256"
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

4. **Ejecutar la aplicación**:
   ```bash
   uvicorn app.main:app --reload
   ```
   La documentación de la API estará disponible en `http://127.0.0.1:8000/`.

## ⚡ Comandos Útiles

Este proyecto utiliza los scripts de `pipenv` para facilitar las tareas de desarrollo comunes. Una vez activado el entorno (`pipenv shell`), puedes usar los siguientes comandos:

- `pipenv run server`: Inicia el servidor de desarrollo con recarga automática.
- `pipenv run lint`: Ejecuta el linter (Ruff) para revisar la calidad del código.
- `pipenv run format`: Formatea todo el código automáticamente con Ruff.
- `pipenv run test`: Lanza la suite de pruebas con Pytest.
- `pipenv run test-cov`: Ejecuta las pruebas y muestra un reporte de cobertura en la terminal.

---

## ☁️ Arquitectura de Despliegue en Azure

Esta sección describe a alto nivel la arquitectura y el flujo de trabajo para desplegar la aplicación en Microsoft Azure.

### Componentes Principales

1.  **Azure Cosmos DB (API para MongoDB):** Actúa como la base de datos NoSQL gestionada, ofreciendo escalabilidad y alta disponibilidad.
2.  **Azure Container Registry (ACR):** Un registro de Docker privado y seguro para almacenar y gestionar las imágenes de la aplicación.
3.  **Azure App Service (para Contenedares):** Es el servicio PaaS que ejecuta la aplicación a partir de la imagen de Docker almacenada en ACR. Gestiona el escalado, la seguridad y la red.

### Flujo de Despliegue Conceptual

El ciclo de vida del despliegue sigue un flujo de CI/CD (Integración Continua / Despliegue Continuo) conceptual:

1.  **Contenerización:** El código fuente se empaqueta en una imagen de Docker. Este artefacto portable y auto-contenido asegura que el entorno de ejecución sea consistente en cualquier máquina.
2.  **Registro:** La imagen se versiona y almacena en Azure Container Registry, que actúa como la única fuente de verdad para las versiones desplegables de la aplicación.
3.  **Orquestación:** Azure App Service se configura para usar la imagen del registro. Al iniciar o reiniciar, el servicio descarga la versión más reciente de la imagen para asegurar que se ejecuta el código actualizado.
4.  **Inyección de Configuración:** Durante el arranque, App Service inyecta de forma segura las variables de entorno (secretos, URI de la base de datos) en el contenedor. Esto desacopla la configuración del código y evita exponer datos sensibles en la imagen de Docker.
5.  **Servicio Activo:** El contenedor se ejecuta y la aplicación se vuelve accesible al público, conectándose de forma segura a la base de datos y otros servicios de Azure.