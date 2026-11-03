# Presentación visual de Sistemas Operativos

## Un único punto de entrada

Haz doble clic en **ABRIR_APLICACION.cmd**. Se abre el navegador y una ventana
que mantiene el servidor local funcionando. Deja esa ventana abierta durante la
demostración. Para terminar, vuelve a ella y pulsa Ctrl+C.

Desde PowerShell en esta carpeta:

```powershell
.\ABRIR_APLICACION.cmd
```

Necesita Python 3.10 o posterior; no necesita paquetes externos, cuenta ni Internet.
El lanzador también detecta el Python incluido con Codex en este computador.
La aplicación solo escucha en 127.0.0.1. Si el puerto está ocupado, cierra la
ejecución anterior o usa `python app_visual.py --port 8766`.

## Demostración ante el profesor

1. Selecciona E2, efecto convoy. Mantén quantum 3 y pulsa **Ejecutar comparación**.
2. Señala que P1 necesita 12 unidades y P2 llega en el instante 1.
3. Compara P2: espera 11 con FCFS y 2 con Round Robin.
4. Pulsa **Reproducir** o desplaza el control de tiempo. Cada bloque representa
   un intervalo real de la traza; la velocidad de reproducción es ilustrativa.
5. Cambia el quantum, vuelve a ejecutar y observa las nuevas métricas.
6. Selecciona E4 para ver bloqueos por E/S o E5 para ver CPU ociosa. Abre las
   transiciones de estado si el profesor pide explicar listo y bloqueado.
7. En **Pruebas y evidencia**, pulsa **Ejecutar pruebas ahora**. Muestra el
   resultado real de la suite, no una marca de aprobación precargada.
8. Puedes editar la lista de procesos y descargar las entradas, métricas,
   trazas y estados completos en JSON. Los casos inválidos muestran un error.

## Estructura del código

| Archivo | Responsabilidad |
|---|---|
| `models.py` | Datos de proceso, estados y validación |
| `algorithms.py` | Única implementación de FCFS y Round Robin |
| `scenarios.py` | Los cinco casos de entrada |
| `app_visual.py` | Servidor local, conexión con el simulador y guardado de evidencia |
| `interfaz.html` | Presentación, tablas y reproducción de las trazas calculadas |
| `test_simulator.py` | 19 pruebas del simulador, con 800 comparaciones internas |
| `test_app_visual.py` | 8 pruebas de integración HTTP y validación de la aplicación |

La interfaz no contiene una segunda implementación de los algoritmos.
Usa las funciones originales corregidas y las mismas métricas. El botón de
pruebas ejecuta ambos archivos de pruebas: **27 comprobaciones** en esta versión.
Los accesos de consola anteriores siguen disponibles y ejecutan la suite original
de 19 pruebas; el informe anterior documenta esa etapa. Esta guía documenta la
ampliación visual y sus ocho comprobaciones adicionales.

Cada comparación y ejecución de pruebas crea una carpeta fechada en
`resultados_en_vivo`, con `resultado.json`. Las pruebas incluyen su salida y
código de terminación. Esos resultados nuevos no se incorporan automáticamente
al repositorio; las evidencias revisadas de esta ampliación están en
`evidencias_verificacion_final/aplicacion_visual`.

## Alcance y entrega

Se comparan cinco escenarios de planificación de CPU, con espera, respuesta,
retorno, cambios de contexto, estados y utilización. Los valores corresponden a
una simulación de una CPU, con costo de cambio de contexto cero y E/S independiente.
No son mediciones del computador. No se afirma que Round Robin gane siempre.

La nueva interfaz fue preparada y probada con asistencia de IA. No acredita por
sí misma un aporte de Esteban ni de Andrés. La trazabilidad individual y la
constancia de revisión de semana 8 siguen requiriendo evidencias reales del equipo.
