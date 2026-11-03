# Guía breve para presentar

## Conceptos

- CPU: recurso que ejecuta instrucciones; el modelo atiende un proceso a la vez.
- Proceso: trabajo identificado por un PID único.
- FCFS: atiende por orden de llegada hasta terminar o bloquearse.
- Round Robin: atiende por turnos; el quantum limita cada turno.
- Espera: suma de los intervalos en la cola de listos.
- Respuesta: primer inicio de CPU menos llegada.
- Retorno: fin menos llegada; incluye CPU, espera y bloqueo.
- Listo: puede ejecutar, pero espera turno. Bloqueado: espera una E/S.
- Los números son unidades simuladas; no son segundos medidos.

## Escenarios

| Caso | Qué muestra |
|---|---|
| E1, carga escalonada | Llegan trabajos en instantes diferentes |
| E2, convoy | Un trabajo largo llega antes que dos cortos |
| E3, simultáneos | Todos llegan al inicio; desempata el orden de la lista |
| E4, E/S | P1 se bloquea después de consumir dos unidades y regresa cuatro después |
| E5, ocio | No hay procesos disponibles en 0-3 y 5-10 |

## Demostración en dos minutos

1. Abre la aplicación. Di: «Comparamos dos formas de repartir una CPU».
2. Selecciona E2 y quantum 3. Pulsa Ejecutar comparación.
3. Señala P2: llega en 1; FCFS lo atiende en 12, RR en 3. Espera 11 y 2.
4. Mueve el reloj a 3: FCFS ejecuta P1; RR ejecuta P2.
5. Ejecuta las pruebas y muestra el resultado real. Descarga la evidencia.
6. Cierra: «El resultado depende de la carga; no hay un ganador universal».

Para preguntas adicionales, muestra E4 y sus transiciones o E5 y los tramos libres.
En E4, volver a LISTO en 6 no garantiza empezar en 6.

## Crear otro ejercicio

En Editar los procesos, cada registro tiene `pid`, `arrival`, `cpu` e `io`.
`io: []` significa sin bloqueos; `io: [[2,4]]` significa esperar cuatro unidades
después de consumir dos de CPU. Los puntos E/S deben ser crecientes y menores
que el trabajo total. Conserva las comas entre registros y evita PID repetidos.
Cambiar el quantum divide el mismo trabajo en turnos distintos; no añade CPU.

## Validación

`test... ok` indica una comprobación aprobada; `Ran 27 tests` cuenta las pruebas
y `OK` resume que aprobaron. Los códigos HTTP de rechazo se provocan a propósito
en pruebas de entradas inválidas. Un caso que falla debe investigarse; las pruebas
no garantizan ausencia de todo error posible.

## Reparto propuesto (no acredita aportes históricos)

Esteban: objetivo, conceptos, ejemplo y conclusiones. Andrés: diseño, E/S,
pruebas y límites. Ambos deben conocer todo el proyecto y participar.
La sustentación puede durar hasta 20 minutos según la consigna del profesor.
