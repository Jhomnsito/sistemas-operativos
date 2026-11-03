# Sistemas Operativos listo para ejecutar

Equipo: **Esteban Peña y Andrés Gámez**.
Tema: gestión de procesos y planificación de CPU, opción 1.

## Presentación visual recomendada

Abre **ABRIR_APLICACION.cmd**. El navegador reúne escenarios, tablas,
reproducción de CPU, estados y un botón para ejecutar las 27 pruebas actuales
(19 del simulador y 8 de integración). Mantén abierta la ventana del servidor.
Lee `LEEME_APLICACION.md`: es la guía breve para presentar esta versión.

Los accesos de consola siguientes son alternativas y conservan su comportamiento.

## Abrir y ejecutar en Windows

1. Extrae completamente `sistemas_operativos_actualizado.zip`. No ejecutes los
   archivos desde el interior del ZIP sin extraer.
2. Abre la carpeta `proyecto_so_actualizado`.
3. Haz doble clic en uno de los tres accesos:

| Archivo | Qué ejecuta ahora |
|---|---|
| `EJECUTAR_SIMULACION.cmd` | Los cinco escenarios con FCFS y RR y la sensibilidad al quantum |
| `EJECUTAR_EJEMPLO.cmd` | El caso del proceso largo E2, sus entradas, resultados y pruebas |
| `EJECUTAR_PRUEBAS.cmd` | Las 19 pruebas con nombre y resultado de cada una |

La ventana permanece abierta para revisar los resultados. Al terminar, el
lanzador indica si hubo errores y dónde se guardaron las evidencias. Presiona
una tecla para cerrar cuando hayas acabado de leer.

Se necesita **Python 3.10 o posterior**. Los accesos buscan el lanzador de
Python instalado y, en este equipo, también pueden usar el Python incluido con
Codex. En otro computador debes tener Python disponible. No se requieren pip,
cuentas de Internet ni extensiones de Visual Studio Code para la simulación.

## Cómo presentarlo en vivo

Empieza por `EJECUTAR_EJEMPLO.cmd`. Explica las entradas antes de leer las salidas:
P1 llega en 0 y consume 12 de CPU; P2 llega en 1 y consume 2; P3 llega en 2 y
consume 4. Round Robin usa quantum 3.

Señala P2: en FCFS espera 11 unidades y en RR espera 2. Explica que estos son
tiempos simulados y que aquí no se cobra tiempo por cambio de contexto.
Después abre `EJECUTAR_PRUEBAS.cmd` y comprueba que el resultado real termina en
`OK`. Son 19 métodos, uno con 800 comparaciones internas contra otro modelo.

Para demostrar el conjunto completo, abre `EJECUTAR_SIMULACION.cmd`. Las salidas
incluyen el escenario con bloqueo E4 y el escenario con CPU ociosa E5.

Cada ejecución nueva crea su propia carpeta dentro de `resultados_en_vivo/`.
Así puedes mostrar un resultado calculado en ese momento y conservar el anterior.
Las evidencias anteriores están en `evidencias/` y `resultados_demo/`.

## Si quieres usar la terminal de Visual Studio Code

Abre esta carpeta con Archivo > Abrir carpeta y, en una terminal abierta en ella,
ejecuta con tu intérprete Python:

```powershell
python ejecutar.py ejemplo
python ejecutar.py pruebas
python ejecutar.py simulacion
```

También se conservan los comandos originales:

```powershell
python main.py --output evidencias_nuevas
python -m unittest -v
```

Si el comando `python` no existe pero tienes el lanzador de Windows, prueba
`py -3` en su lugar. Los accesos CMD evitan tener que elegir manualmente el
intérprete en el equipo de la demostración.

## Abrir el informe y preparar la sustentación

Haz doble clic en `informe_tecnico.pdf` y ábrelo con el visor PDF o navegador.
No abras el PDF con el editor de texto de Visual Studio Code. Para leer su
contenido dentro de VS Code, abre `informe_tecnico.md` y utiliza la vista previa
de Markdown. El PDF es el informe que pide el profesor para la entrega.

`GUION_DOS_INTEGRANTES.md` propone el reparto de los veinte minutos y contiene
frases y comandos para ensayar. `APORTES.md` registra los dos nombres y deja
pendientes las contribuciones reales. Completa estas con evidencias, el enlace
real del repositorio/carpeta compartida y la constancia de semana 8 si existe.

`REPOSITORIO.md` indica el estado del repositorio. No se ha inventado un enlace
de GitHub ni un historial de aportes del equipo.
