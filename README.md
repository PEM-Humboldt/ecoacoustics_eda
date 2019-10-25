# Flujo de análisis de paisajes sonoros - Parte 1


La gran cantidad de datos colectados durante un monitoreo acústico requiere de un flujo de trabajo estandarizado para guardar la información de forma estructurada, facilitar el intercambio de trabajo entre investigadores y agilizar el análisis de los datos. Se propone un flujo de trabajo semi-automático con el fin de aprovechar la velocidad de cómputo de los computadores y la capacidad de abstracción humana. En este documento se detallan las primeras fases del flujo de trabajo: (1) estructuración de metadatos a partir de los archivos de audio, (2) sub-muestreo de los datos para análisis exploratorio, (3) visualización de los datos, y (4) cuantificación de diferencias entre paisajes sonoros.

## 1. Estructuración de metadatos

Al realizar una grabación de audio, los sensores acústicos incluyen en cada archivo información que es fundamental para los análisis posteriores. Con el fin de automatizar la recuperación de estos datos se programó en lenguaje R un script que recorre todos los archivos en un directorio, extrae los metadatos y los estructura en un archivo separado por comas, o csv. **Se recomienda que los archivos estén anidados en un directorio con el nombre de la localidad y un subdirectorio con el nombre del punto de muestreo**. Un script (read_audio_metadata.R) recupera un total de 12 características y otro script (plot_audio_metadata.R) facilita graficar esta información (Figura 1).

-	Nombre del archivo
-	Frecuencia de muestreo
-	Número de bits por muestra
-	Número de muestras
-	Número de canales en la grabación
-	Tamaño del archivo
-	Tipo de grabadora
-	Nombre del sensor
-	Fecha
-	Hora
-	Duración de la grabación
-	Nombre del directorio principal dónde se encuentran los archivos (localidad)
-	Nombre del sub-directorio dónde se encuentran (punto de muestreo)


## 2. Sub-muestreo de los datos

En cada monitoreo acústico se recuperan grandes cantidades de datos, del orden de los Terabytes. Por las capacidades limitadas de cómputo y la velocidad de acceso de los datos, realizar pruebas y análisis sobre todo el conjunto de datos no resulta eficiente. Un sub-muestreo de estos datos permite tener una visión global de los datos de forma ágil. El script recorre un conjunto de archivos de audio, tomando cinco segundos (5 s) de cada archivo y si es necesario realiza un re-muestreo del audio para obtener archivos homogéneos. La salida es un archivo en formato pkl que puede ser leída por Python fácilmente.

Nombre del script: sample_acoustic_monitoring.py

## 3. Visualización de datos

A partir del sub-muestreo de los datos resulta sumamente fácil y rápido realizar múltiples análisis, como calcular características acústicas y visualizar datos. Al trabajar con volúmenes de Terabytes, la visualización de datos resulta efectiva tanto para presentar información de grandes cantidades de datos, como para direccionar los análisis más complejos. La mente humana está altamente entrenada para reconocer patrones visuales, y al presentarle información en formato crudo, pero de manera organizada, es capaz de identificar fácilmente las principales tendencias de los datos. 

Para la visualización de los datos de los monitoreos acústicos se tuvo en cuenta una representación en 2D del sonido y los pulsos naturales de 24 horas del paisaje sonoro. Así, se propone calcular el espectrograma de cada archivo de audio y organizar estos espectrogramas en ciclos de 24 horas (Figuras 2, 3 y 4).

Nombre del script: audio_to_spectro_image.py


## 4. Análisis cuantitativo de paisajes sonoros

Los patrones identificados gracias a las herramientas de visualización deben ser medidos para poder comparar la información entre los puntos de muestreo y realizar un análisis cuantitativo. Con este fin, se diseñó un índice sencillo y de fácil interpretación. El índice calcula el porcentaje de actividad acústica relacionando a partir de un umbral seleccionado por el usuario, la cantidad de píxeles en un espectrograma que están por encima del umbral, dividido por los píxeles que están por debajo. Con este sencillo índice es posible comparar la actividad acústica entre diferentes sitios (Figuras 5 y 6).

Nombre del script: compute_soundscape_metrics.py
