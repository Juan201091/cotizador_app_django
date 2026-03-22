# Cotizador de Recetas

## Descripción

Este proyecto es una aplicación web desarrollada con Django que permite calcular el costo de distintas recetas en base a sus ingredientes, mostrando el resultado tanto en pesos argentinos (ARS) como en dólares (USD).

La idea fue resolver el problema de manera clara y ordenada, priorizando que el código sea fácil de entender y mantener, sin agregar complejidad innecesaria pero dejando una base preparada para crecer.

---

## Tecnologías utilizadas

* Backend: Django (Python)
* Frontend: HTML + Bootstrap 5 + HTMX
* Estilos: CSS custom + Bootstrap
* Fuentes de datos: XLS, PDF y Markdown
* Cache: Django Cache Framework
* Contenedores: Docker + Docker Compose

---

## Decisiones de diseño

### Separación por capas

El proyecto se organizó en distintas capas:

* Domain: lógica pura (cálculo de costos)
* Application: casos de uso que orquestan la lógica
* Infrastructure: lectura de archivos
* Views/Templates: manejo HTTP y render

No es una implementación estricta de arquitectura hexagonal, pero sí sigue bastante la idea de separar responsabilidades.

---

### Uso de Use Cases

Se implementaron casos de uso como:

* `ObtenerRecetasUseCase`
* `CalcularCostoRecetasUseCase`

En este caso algunos son simples, pero ayudan a mantener la vista limpia y desacoplada de la lógica.

---

### Cache

Para evitar procesar las fuentes de datos en cada request, los datos base se guardan en cache. Esto mejora el rendimiento y simplifica el flujo general.

---

### Inyección de dependencias

Se utilizó un enfoque simple mediante funciones tipo provider para instanciar servicios y casos de uso, evitando acoplar la vista con la infraestructura.

---

## Fortalezas

* Código ordenado y fácil de seguir
* Separación clara de responsabilidades
* Interfaz simple pero funcional
* Uso de cache para mejorar performance
* Base preparada para escalar sin grandes cambios

---

## Debilidades

* No hay persistencia en base de datos
* Pensado principalmente para uso local o de bajo volumen
* No hay tests automatizados
* Cache básico (no distribuido)
* No hay manejo de usuarios ni autenticación

---

## Asunciones

* Los archivos de entrada tienen un formato consistente
* Los ingredientes coinciden entre recetas y precios
* La cotización del dólar está disponible para la fecha consultada
* El volumen de datos es acotado

---

## Limitaciones

* No está preparado para alta concurrencia
* No hay persistencia histórica de datos
* Dependencia de archivos externos como fuente principal

---

## Cómo ejecutar el proyecto

### 1. Clonar el repositorio

git clone <repo_url>

### 2. Usando Docker (recomendado)

Si tenés Docker instalado, podés levantar todo el entorno con:

docker-compose up --build

Una vez iniciado, la aplicación queda disponible en:

http://localhost:8000/

En este entorno además se centraliza el logging de la aplicación, lo que permite tener trazabilidad de lo que ocurre (carga de datos, uso de cache, errores, etc.), algo útil tanto para debug como para operación.

---

## Posibles mejoras / Escalabilidad

Si este proyecto tuviera que escalar o pasar a un entorno productivo, los siguientes pasos serían razonables:

* Incorporar una base de datos (por ejemplo PostgreSQL)
* Utilizar Redis como sistema de cache
* Separar algunos servicios (por ejemplo la cotización)
* Procesar tareas pesadas en background
* Desplegar con Nginx + Gunicorn en contenedores

También sería importante agregar tests y mejorar el monitoreo general del sistema.

---

## Cierre

La idea no fue hacer algo perfecto, sino una solución clara, mantenible y con una estructura que permita crecer sin tener que rehacer todo desde cero.

Se buscó un equilibrio entre buenas prácticas y simplicidad, evitando sobreingeniería pero manteniendo una base sólida.
