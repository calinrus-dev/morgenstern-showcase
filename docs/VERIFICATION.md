# Cómo comprobar esta muestra

[← Proyecto](../README.md) · [Origen](PROVENANCE.md)

## Repetir la comprobación

Python 3.11+ y FFmpeg/ffprobe en PATH; biblioteca estándar. Windows puede usar py -3.

Desde la raíz de este repositorio:

~~~sh
python3 -m unittest discover -s test -v
python3 samples/delivery_demo.py
~~~

Última ejecución local: **7 pruebas aprobadas**, 28 de septiembre de 2026. Este es un resultado fechado, no una promesa sobre cambios futuros.

[Workflow y ejecuciones públicas](https://github.com/calinrus-dev/morgenstern-showcase/actions/workflows/verify.yml). Abre una ejecución para ver el commit exacto y los logs; el badge del README sigue la rama actual.

## Comprobar la interacción

[Demo publicada](https://calinrus-dev.github.io/morgenstern-showcase/). También puedes servir la raíz con python3 -m http.server 8090 y abrir el puerto local en el navegador. No se necesitan cuentas ni credenciales.

## Qué no certifican estas pruebas

ffprobe no decodifica todo el contenido ni evalúa calidad narrativa o de voz. El EPUB se comprueba estructuralmente, sin ejecutar EPUBCheck. La fixture no representa generación con IA ni una producción editorial completa.

Las pruebas nuevas ejercitan las piezas públicas. No se suman a las cifras históricas de tests del producto como si fueran la misma suite.
