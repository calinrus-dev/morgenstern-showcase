# Origen y alcance de la muestra pública

[← Proyecto](../README.md)

## Qué se publica

media_gate.py adapta las comprobaciones del validador multimedia real. Elimina la configuración interna y añade comprobaciones de forma, duración finita y timeout. delivery_demo.py y sus archivos son referencias sintéticas nuevas. El exportador EPUB del producto permanece privado.

[Inspeccionar la pieza](../samples/media_gate.py). La primera publicación de estas muestras es del 28 de septiembre de 2026. Esa fecha no pretende representar la fecha de creación del producto ni actividad de desarrollo histórica.

## Qué puede comprobar otra persona

Las capturas de `assets/interface/` se tomaron el 1 de octubre de 2026 de la interfaz React/Tauri del producto en desarrollo. Muestran una obra sintética creada para comprobaciones locales, chat con proveedor mock y una propuesta editorial simulada. Son capturas de la aplicación, no diseños conceptuales. Los manuscritos, conversaciones y credenciales de usuarios no forman parte de esta publicación.

El código público, las pruebas y el workflow están en este mismo repositorio. Se pueden clonar, ejecutar y discutir. La procedencia desde archivos privados es una declaración del autor: un lector externo no tiene acceso a ese historial para contrastarla. Las adaptaciones se describen arriba para no confundir una muestra con el producto completo.

## Límites

ffprobe no decodifica todo el contenido ni evalúa calidad narrativa o de voz. El EPUB se comprueba estructuralmente, sin ejecutar EPUBCheck. La fixture no representa generación con IA ni una producción editorial completa.

La publicación de estas piezas no abre el núcleo del producto. Las APIs internas, secretos, claves, datos de usuario, contenido comercial y demás implementaciones privadas quedan fuera.

## Derechos

Copyright © 2026 Calin Rus. Código visible para evaluación técnica. No se incorpora una licencia general de reutilización al producto privado.
