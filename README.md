# Práctica 1: Web scraping a Menéame.net

## Descripción

Esta práctica se ha realizado bajo el contexto de la asignatura _Tipología y ciclo de vida de los datos_, perteneciente al Máster en Ciencia de Datos de la Universitat Oberta de Catalunya. En ella, se aplican técnicas de _web scraping_ mediante el lenguaje de programación Python para extraer así datos de la web [Menéame.net](http://meneame.net) y generar un _dataset_.


## Uso

La aplicacion puede ser ejecutada desde una terminal con Python3 mediante el siguiente comando

```
python main.py --stop_date 23/10/2017 --show_graphs
```

Donde **--stop_date** es la fecha hasta la cual las noticias seran recolectadas en el dataset por la aplicación y **--show_graphs** es un parametro opcional que indica si se deben mostrar las graficas resumen del dataset una vez creado.

Como opcion extra, una vez el dataset se ha generado se pueden volver a mostrar las graficas usando solo la opcion **--show_graphs** o **-g**, de la siguiente manera:

```
python main.py -g
```

## Documentación

La documentación relativa a la práctica se encuentra en [nuestra wiki](https://github.com/Cs4r/MeneameScraper/wiki/MeneameScraper).

## Recursos

1. Lawson, R. (2015). _Web Scraping with Python_. Packt Publishing Ltd. Chapter 2. Scraping the Data.
2. Mitchel, R. (2015). _Web Scraping with Python: Collecting Data from the Modern Web_. O'Reilly Media, Inc. Chapter 1. Your First Web Scraper.
