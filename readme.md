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

* Los archivos de entrada tienen un formato consistente y no cambian
* Los ingredientes coinciden entre recetas y precios
* La cotización del dólar está disponible para la fecha consultada
* El volumen de datos es acotado

---

## Limitaciones

* No hay persistencia histórica de datos
* Dependencia de archivos internos como fuente principal

---

## Cómo ejecutar el proyecto

### 1. Clonar el repositorio

```bash
git clone <https://github.com/Juan201091/cotizador_app_django.git>
cd <cotizador_app_django>
```

---

### 2. Requisitos

Asegurarse de tener instalado:

* Docker
* Docker Compose

---

### 3. Ejecutar con Docker (recomendado)

```bash
docker-compose up --build -d
```

Esto levanta automáticamente todos los servicios necesarios.

Una vez iniciado, la aplicación queda disponible en:

```
http://localhost:8000/
```

En este entorno también se centraliza el logging de la aplicación, lo que permite tener trazabilidad de eventos importantes como carga de datos, uso de cache y posibles errores.


## Posibles mejoras / Escalabilidad

Si la aplicación tuviera que escalar a un entorno productivo, sería recomendable incorporar una base de datos para persistir la información y no depender únicamente de archivos en memoria. También se podría utilizar un sistema de cache distribuido como Redis para mejorar el rendimiento en escenarios con múltiples usuarios.

Por otro lado, el servicio de cotización del dólar podría optimizarse mediante cacheo por fecha, ya que se trata de un valor determinístico. Esto permitiría reducir llamadas a servicios externos y mejorar los tiempos de respuesta, además de considerar el uso de múltiples fuentes para mayor resiliencia.

Finalmente, se podrían delegar tareas más pesadas a procesos en background y realizar el despliegue utilizando herramientas como Nginx y Gunicorn dentro de contenedores, lo que permitiría mejorar la estabilidad y facilitar la escalabilidad de la aplicación.

## Cierre

La idea no fue hacer algo perfecto, sino una solución clara, mantenible y con una estructura que permita crecer sin tener que rehacer todo desde cero.

Se buscó un equilibrio entre buenas prácticas y simplicidad, evitando sobreingeniería pero manteniendo una base sólida.
