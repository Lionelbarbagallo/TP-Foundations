# Trabajo Práctico I - Módulo Foundations - Diplomatura Cloud Data Engineering

## Bienvenido al repositorio de mi trabajo!

Para este trabajo hemos utilizado un dataset público disponible on line en la plataforma Kaggle: "Brazilian E-Commerce Public Dataset by Olist". La docuemntación del dataset puede 
consultarse en https://www.kaggle.com/olistbr/brazilian-ecommerce?select=olist_order_items_dataset.csv. Este dataset contiene datos relativos a las ventas online de varios marketplace brasilños, tales como productos vendidos, montos facturados, medios de pago, plazos de entregas e información sobre clientes y vendedores.

Este conjunto de datos permite responder varias inquietudes de negocio. Más adelante profundizaremos en algunas de ellas, pero veremos que muy fácilmente podemos identificar 
patrones en las ventas, estudiar el ritmo de entregas o entender la distribuciónn territorial de las ventas. En conjunto, esta información puede servir de input para varias
áreas del negocio: finanzas, marketing, operaciones y logística.

## Qué encontraré en este repositorio?

Aquí encontrarás los archivos pertinentes para consrtuir y correr las imágenes de Docker que realizan todos los procesos involucrados con la lectura de los datos desde su ubicación original,
limpieza, transformación y cargado posterior en una base de datos PostgreSQL, terminando con la realización de algunas consultas de negocio relevantes. 

## Requerimientos previos

Antes de comenzar precisarás tener instalados:

```
Git
```
```
Docker Engine
```
```
Docker Compose 
```
Puedes consultar la documentación oficial con instrucciones para su instalado en https://docs.docker.com/compose/install/

Adicionalmente, requerirás un token de autenticación para utilizar la API de Kaggle. A los efectos de simplificar la prueba y evaluación del presente trabajo, hemos incluido un token de prueba
en la carpeta inicial del repositorio. Podrán hallar el mismo bajo el nombre kaggle.json. Se recomienda generar su propio token y reemplazar el actual por el nuevo. Para hacerlo,
referimos a la documentación oficial de Kaggle: https://www.kaggle.com/docs/api

## Comencemos! 

Para utilizar este material recomendamos realizar un git clone del presente repositorio. Para ello, puede correr en consola el siguiente comando:

```
git clone -b master https://github.com/Lionelbarbagallo/TP-Foundations.git
```
Una vez descargado el material, ingrese en la carpeta TP-Foundations.

```
cd TP-Foundations
```

Antes de seguir, verifique que no tenga corriendo en su equipo otros contenedores con los nombres (esto podría generar conflictos):

* db
* etl
* queries

Una vez realizada esta verificación, procederemos a buildear la imagen de los contenedores que instanciaremos. Para ello, corra (siempre dentro del directorio TP-Foundations):

```
docker-compose -f dc.yml build
```
Una vez que la imagen está construida, podemos ejecutarla:
```
docker-compose -f dc.yml up -d
```
Utilizamos la bandera -d para correr el proceso en modo detached mode en el backgroud.

## Qué servicios y procesos activa esta imagen?

La imagen de Docker que acabamos de correr levanta tres contenedores. En el primero, va a estar corriendo el servicio de Postgres. Los otros dos contenedores van a correr los procesos de ETL
y consulta de la base de datos.

## Sobre la base de datos

Se trata de una base de datos PostgreSQL, levantada a apartir de la imagen oficial de Postgres disponible en Docker Hub https://hub.docker.com/_/postgres
La base de datos es inicializada con los siguientes valores por default:

Nombre: postgres \
Usuario: postgres \
Password: postgres 

Asimismo, se expone el puerto 5432 (puerto default de Postgres) hacia el puerto 5432 del host.

## Sobre las consultas

Una vez terminada la carga del dataset en la base de datos, un tercer contenedor lleva adelante un conjunto de consultas pre definidad para satisfacer ciertos requerimientos de negocio.
La salida de estas consultas son un conjunto de reportes .csv que son almacenados en la carpeta base del proyecto.

Las consultas realizadas permiten responder las siguientes necesidades de negocio:

### mejores_clientes:
Permite identificar los mejores clientes del marketplace. Podemos aplicar programas de fidelización y promociones.\
### ventas_zipcodes:
Permite identificar los zip codes con mayores ventas. Es un dato relevante en caso de que la gerencia decida instalas tiendas físicas.\
### mas_vendidos:
Permite identificar los productos más vendidos para orientar los esfuerzos de marketing en ellos y distribuir el presupuesto de publicidad.\ 
### shares:
Permite identificar el share de cada división en las ventas totales, y de cada producto en su división.\ 
### tiempo_entregas:
Es una serie de tiempo que muestra el cumplimiento de los plazos de entrega. Se calcula como fecha de entrega - fecha estimada de entrega. Un valor negativo, significa que los productos se están entregando en plazos menores a los previstos. Los valores se muestran en días. Esta información es relevante para evaluar el área de logística y operaciones.

## Aspectos a mejorar

Han quedado varios puntos susceptibles de mejoras de los que no queremos dejar de dar cuenta.

* Los argumentos para inicializar la base de datos han sido hardcodeados. Esto es una mala práctica que debe ser reemplazada por un uso adecuado de parámetros definibles por el usuario.
* No se han especificado versiones de las librerías y programas utilizados. En el futuro esto puede dar lugar a incompatibilidades entre las diversas modificaciones debidas a moficiaciones futuras no previstas. Para evitar este inconveniente, debieran explicitarse en el código las versiones utilizadas de cada programa.
* Queda pendiente la mejora de las estrategias de logging para resolver posibles problemas no previstos (como la modificación de alguna dependencia o de la fuente del dataset).
* Vinculado con el punto anterior, queda pendiente una mejora en las estrategias de handling de errores y excepciones.


 




