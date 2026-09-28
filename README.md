# Morgenstern / Generar no es entregar.

**Una línea de producción editorial con IA.** Ideas, estructura, capítulos, revisión, EPUB y audiolibro. El problema interesante no es pedirle texto a un modelo: es conservar el contexto de una obra, coordinar el trabajo y terminar con entregables revisables.

**Python · Textual · Automatización editorial**

## La obra manda

La estructura acompaña al contenido. La generación forma parte de un recorrido que incluye decisiones del autor y salida editorial. Morgenstern está orientado a producir a escala sin convertir cada libro en una carpeta de respuestas sueltas.

~~~text
Idea y esquema → Obra organizada → Generación coordinada
                                     ↓
                           Revisión y decisiones del autor
                                     ↓
                           EPUB / audio / entregables
~~~

[Recorrido del producto](docs/EXPERIENCIA.md) · [Responsabilidades y decisiones](docs/ARQUITECTURA.md)

## Abre una entrega. Después lee el código.

[**Entrega pública inspeccionable →**](https://calinrus-dev.github.io/morgenstern-showcase/) · [EPUB sintético](examples/sample.epub) · [Informe con hashes](examples/report.json)

Aquí hay dos piezas, con el origen bien separado:

- **Una adaptación del validador multimedia real:** [media_gate.py](samples/media_gate.py). Inspecciona streams y duración mediante ffprobe. Se ha desacoplado de la configuración privada y endurecido frente a NaN, informes malformados y procesos que se cuelgan.
- **Un generador nuevo para esta publicación:** [delivery_demo.py](samples/delivery_demo.py). Produce un EPUB mínimo determinista y un tono de un segundo. Sirve para repetir la comprobación sin proveedores, manuscritos ni cuentas. El tono no es un audiolibro y el generador no es el exportador privado.

[![Pruebas de la muestra](https://github.com/calinrus-dev/morgenstern-showcase/actions/workflows/verify.yml/badge.svg)](https://github.com/calinrus-dev/morgenstern-showcase/actions/workflows/verify.yml)

~~~sh
python3 -m unittest discover -s test -v
python3 samples/delivery_demo.py
python3 samples/media_gate.py build/public-demo/tone.wav --minimum 0.9
~~~

Python 3.11+ y FFmpeg/ffprobe. En Windows: `py -3`. Sin dependencias Python adicionales. CI reproduce el EPUB y el WAV y los compara byte a byte con los publicados.

## Fallar antes de llamar «entrega» a un archivo

Un fichero con extensión correcta puede estar vacío. Una duración NaN se puede colar en una comparación inocente. Un vídeo sin audio puede ser válido como formato y no cumplir el contrato de un audiolibro audiovisual. Esas diferencias están en [pruebas ejecutables](test/test_delivery.py), no escondidas bajo un «todo OK».

La inspección de ffprobe comprueba contenedor, streams y duración; no escucha la narración ni decodifica cada frame. El EPUB tiene comprobaciones estructurales acotadas; no se anuncia certificación EPUBCheck. La muestra tampoco acredita una generación completa con IA, costes por libro ni calidad literaria.

**Automatizar producción exige conservar el control editorial. El botón de generar todavía no sabe editar.**

[Estado del producto](docs/ESTADO.md) · [Origen y límites](docs/PROVENANCE.md) · [Verificación](docs/VERIFICATION.md) · [Portfolio](https://github.com/calinrus-dev/portfolio)


[Instagram @c4linrus](https://www.instagram.com/c4linrus/) · [LinkedIn / calinrus](https://www.linkedin.com/in/calinrus-dev/)
