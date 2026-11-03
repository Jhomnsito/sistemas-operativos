# Sistemas Operativos

Simulador de planificación de CPU. Compara FCFS y Round Robin en una CPU simulada. Conserva los tres escenarios
del proyecto original y añade E/S y tiempos ociosos para validar los estados.

## Requisitos y ejecución

Python 3.10 o posterior. Verificado con Python 3.12.14 en Windows.
Solo se usa la biblioteca estándar: no necesitas instalar paquetes con pip.

1. Extrae todo el ZIP.
2. Abre una terminal en la carpeta del proyecto, donde está `main.py`.
3. Ejecuta:

```console
python main.py
python -m unittest -v
```

Si en Windows utilizas el lanzador de Python, puedes usar `py -3` en lugar de
`python`. Los tiempos que aparecen son unidades simuladas, no segundos medidos.

Para guardar una nueva ejecución sin reemplazar las evidencias incluidas:

```console
python main.py --output evidencias_nuevas
```

Para guardar también el texto de consola con una terminal:

```console
python main.py --output evidencias_nuevas > ejecucion_nueva.txt
python -m unittest -v > pruebas_nuevas.txt 2>&1
```

El programa devuelve código 0 si completa la ejecución y 1 ante errores de
escritura o validación. Los argumentos incorrectos de consola los informa argparse.
Los CSV usan punto decimal y coma como separador; si Excel no los separa
correctamente, impórtalos como datos delimitados por comas.

## Archivos

- `models.py`: datos de procesos, validación de entradas y estados.
- `algorithms.py`: FCFS, RR, cola de listos, eventos E/S, trazas y métricas.
- `scenarios.py`: cinco escenarios y sus datos de entrada.
- `main.py`: ejecuta ambas políticas, exporta resultados y compara cuatro quantum.
- `test_simulator.py`: 19 pruebas; una de ellas compara 200 casos con cuatro
  configuraciones contra un modelo independiente por ticks, para 800 comparaciones.
- `informe_tecnico.pdf`: explicación, resultados, análisis y riesgos.
- `informe_tecnico.md`: contenido editable del informe, con las mismas cifras.
- `REVISION.md`: diagnóstico del ZIP original y correcciones aplicadas.
- `APORTES.md`: registro honesto de lo verificable y datos del equipo por completar.
- `GUIA_SUSTENTACION.md`: preguntas y ejecución breve para preparar la sustentación.
- `GUION_DOS_INTEGRANTES.md`: propuesta de exposición para Esteban Peña y Andrés Gámez.
- `evidencias/`: resultados reales de la revisión, pruebas y entradas reproducibles.
- `evidencias/revision_original/`: salida y fallos registrados sobre el ZIP recibido.

## Modelo y criterios

Cada proceso se construye con `Process(pid, llegada, cpu_total, io_events=...)`.
Ejemplo: `Process(1, 0, 6, io_events=[(2, 4)])` requiere seis unidades de CPU y
se bloquea cuatro unidades después de consumir las primeras dos de CPU.
Los puntos de E/S se expresan en CPU acumulada, no en tiempo global.
Puedes cambiar los casos en `scenarios.py` y volver a ejecutar las pruebas.

FCFS ejecuta hasta finalizar o bloquearse. RR ejecuta como máximo un quantum.
Las llegadas y desbloqueos ocurridos durante el tramo de CPU entran antes que
el proceso reinsertado por fin de quantum. Los empates se resuelven por orden
de registro: llegadas en orden de entrada, antes de desbloqueos al mismo instante;
los desbloqueos empatados siguen su orden de registro.

Los estados son NUEVO, LISTO, EJECUCION, BLOQUEADO y FINALIZADO. Al iniciar la
simulación se crean los registros NUEVO; cada llegada activa la admisión a LISTO.
Las funciones devuelven copias nuevas: comparar algoritmos no altera la entrada.
La clase `SimulationResult` conserva la interfaz de lista del código original y
añade `timeline`, `events`, `end_time` y `metrics()`.

Un cambio de contexto se cuenta entre dos tramos contiguos de CPU de procesos
distintos. No se cuenta el primer despacho, el paso desde/hacia CPU ociosa ni
renovar el quantum del mismo proceso. Los despachos se cuentan aparte. La
utilización usa todo el intervalo desde t=0 hasta la última finalización, incluido
el ocio inicial. No se añade costo temporal por cambio de contexto.

## Evidencias

- `entradas.json`: datos exactos de los cinco escenarios.
- `resumen.csv`: 10 combinaciones de escenario y algoritmo.
- `procesos.csv`: llegada, CPU, E/S, inicio, fin, espera, retorno y respuesta.
- `cpu.csv`: tramos de CPU y ocio; PID vacío significa CPU ociosa.
- `estados.csv`: estado, instante y motivo de cada transición.
- `sensibilidad_quantum.csv`: E2 con quantum 1, 3, 6 y 12.
- `ejecucion.txt`: salida completa de la ejecución realizada.
- `pruebas.txt`: salida real de unittest con 19 pruebas aprobadas.
- `compatibilidad_original.json`: métricas por proceso de los tres casos originales,
  iguales en ambas versiones durante la revisión.
- `validacion_adicional.txt`: recálculo de CSV y prueba del manejo de errores de salida.
- `entorno.json`: versión de Python, plataforma y SHA-256 del código ejecutado.

En la salida de unittest, 19 significa métodos de prueba, no 19 casos de carga:
las 800 comparaciones se ejecutan como subcasos de un método. Se usa semilla 2620.
Las simulaciones son deterministas; repetirlas no constituye muestreo de un SO real.

## Limitaciones y entrega académica

La E/S tiene duración fija y puede solaparse; no hay cola ni contención de
dispositivo. No hay paralelismo real, prioridades efectivas, memoria, fallos de
hardware ni costos de caché. El campo `priority` se conserva por compatibilidad,
pero FCFS y RR no lo usan. No se deducen rendimientos reales de Windows o Linux.
El programa materializa las trazas en memoria; está pensado para cargas pequeñas.

El informe ya identifica a Esteban Peña y Andrés Gámez. Antes de entregar,
completa `APORTES.md` con aportes y evidencias reales, coloca la versión en el
repositorio/carpeta compartida del grupo y acredita la revisión de semana 8.
No se inventó ninguno de esos antecedentes. Lee el código, reproduce los
resultados y declara la asistencia de IA según lo exige el curso.

## Carpeta final y demostración en vivo

El equipo confirmado es Esteban Peña y Andrés Gámez. Empieza por `INICIO_RAPIDO.md`.
En Windows puedes hacer doble clic en `EJECUTAR_SIMULACION.cmd`,
`EJECUTAR_EJEMPLO.cmd` o `EJECUTAR_PRUEBAS.cmd`. Cada lanzador conserva
la consola abierta y guarda una ejecución nueva en `resultados_en_vivo/`.
Los lanzadores buscan Python 3.10 o posterior; en el equipo donde se preparó
la entrega también pueden usar el Python ya incluido con Codex.

`demostracion_en_vivo.py` recalcula E2 y ejecuta las pruebas. `demostracion_pruebas.py`
muestra cada prueba por nombre. `ejecutar.py` centraliza los lanzadores y registra
sus salidas. No se necesitan extensiones de VS Code para ejecutar estos archivos.
El PDF se puede abrir con el visor de documentos o navegador del equipo.

`resultados_demo/` conserva las ejecuciones reales de la demostración anterior.
`VERIFICACION_ENTREGA.md` registra los controles realizados sobre esta carpeta final.
`REPOSITORIO.md` explica el historial local y la publicación verificada en el
repositorio privado https://github.com/Jhomnsito/sistemas-operativos.
El historial local asistido no acredita retrospectivamente los aportes del equipo.
