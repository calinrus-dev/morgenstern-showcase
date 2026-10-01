# Morgenstern / Estado y evidencia

[← Inicio](../README.md)

**Estado:** interfaz de escritorio en desarrollo; beta pública en preparación.

**Fecha de revisión:** 1 de octubre de 2026.

## Nueva interfaz

El estudio React + Tauri 2 reúne estructura de la obra, editor Markdown, lectura, versiones y asistente contextual. La factoría editorial conecta objetivos, tareas aprobadas, generación y revisión de propuestas antes de aplicar una nueva versión. La exportación EPUB está integrada en el estudio.

[Estudio de escritura](../assets/interface/estudio-escritura.jpg) · [Factoría editorial](../assets/interface/factoria-editorial.jpg)

Estas capturas son reales y utilizan una obra de prueba. Las respuestas del chat y la propuesta del diff son simuladas; no se presentan como evaluación de calidad literaria o de un proveedor LLM.

## Comprobaciones del producto privado

En el entorno local Linux se ha compilado y arrancado el cliente de escritorio. Se han comprobado los recorridos de creación, guardado de versiones, chat, revisión de propuestas y exportación EPUB. La suite Python pasó 1.501 pruebas, junto a los controles Ruff y mypy; también pasaron las pruebas Rust y del frontend.

Estas comprobaciones pertenecen al repositorio privado y se declaran aquí como contexto. Las pruebas que cualquier persona puede reproducir en este showcase están en [VERIFICATION.md](VERIFICATION.md).

La configuración de CI incluye Windows, pero la nueva aplicación no se ha probado todavía en una máquina Windows. La compilación Docker tampoco se ha ejecutado en esta revisión local. Los pipelines de audio y vídeo permanecen en el motor y no se anuncian como botones ya integrados en el estudio.

## Próxima beta

Estoy preparando una beta que pondré a disposición próximamente. Todavía no hay fecha de lanzamiento, instaladores públicos ni inscripción abierta. Este repositorio comunicará su disponibilidad y condiciones de prueba cuando estén definidas.

## Alcance

La generación requiere un proveedor configurado o un modelo local disponible. El modo local de la aplicación no implica que todos los proveedores funcionen sin conexión. La calidad de una obra necesita revisión humana.

El núcleo del producto y los datos de usuario permanecen privados. Este showcase conserva su muestra pública ejecutable de EPUB/audio y su validador multimedia.
