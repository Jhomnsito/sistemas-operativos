# Guía de sustentación

Propuesta de recorrido para los 20 minutos máximos. Distribuyan la participación
entre integrantes reales; esta propuesta no acredita que la exposición ya ocurrió.

1. Minutos 0 a 3: problema y objetivo. Varios procesos solicitan una CPU;
   comparar el orden FCFS con los turnos RR y explicar qué se intenta optimizar.
2. Minutos 3 a 7: diseño. Mostrar Process, cola de listos, eventos de E/S y
   transiciones. Explicar que las funciones trabajan sobre copias de la entrada.
3. Minutos 7 a 11: ejecutar `python main.py --output demo` y abrir `demo/resumen.csv`.
   Mostrar E2 y la mejora de respuesta de RR; contrastar E1, donde empeora el retorno.
4. Minutos 11 a 14: abrir `demo/estados.csv`, filtrar E4/P1 y seguir el bloqueo y
   regreso a listo. En E5 mostrar los intervalos de CPU ociosa.
5. Minutos 14 a 17: ejecutar `python -m unittest -v`; explicar el caso manual y
   el oráculo por ticks, sin confundir 19 métodos con 800 comparaciones internas.
6. Minutos 17 a 20: riesgos, límites, aportes reales y preguntas.

## Preguntas que cada integrante debería poder responder

**¿Qué es FCFS?** Atender por orden de entrada a la cola; aquí ejecuta sin
expropiación hasta terminar o bloquearse. Tras E/S, vuelve al final de la cola.

**¿Qué agrega Round Robin?** Limita cada turno de CPU a un quantum positivo.
Si queda CPU y no ocurre bloqueo, el proceso vuelve al final de la cola.

**¿Cuáles son los tiempos?** Retorno = fin - llegada. Respuesta = primer uso
de CPU - llegada. Espera = retorno - CPU consumida - tiempo bloqueado.
La espera solo cuenta el tiempo en LISTO.

**¿RR siempre es mejor?** No. En E1 baja la respuesta media de 5.75 a 3.00,
pero sube el retorno de 11.25 a 14.00. En E2 mejora ambas métricas.

**¿Por qué RR hace más despachos que cambios?** Un proceso puede agotar el
quantum y ser seleccionado otra vez sin que la CPU pase a otro proceso.
Con un solo proceso de CPU 7 y quantum 2 hay cuatro despachos y cero cambios
según nuestra definición; el costo temporal no está modelado.

**¿Cómo sé que el estado bloqueado se utiliza?** E4/P1 se bloquea al consumir
dos unidades de CPU durante cuatro unidades de tiempo; el historial registra
BLOQUEADO y después LISTO por fin de E/S.

**¿Se crean procesos del sistema?** Se crean objetos simulados. No se crean
procesos Windows ni se cambia el planificador del sistema operativo anfitrión.

**¿La utilización del 100 % significa rendimiento perfecto?** No. Significa
que en esos escenarios la CPU simulada no quedó ociosa entre t=0 y el final;
se ignoran costos reales y no mide la capacidad del equipo.

**¿Qué pasa con un quantum pequeño?** En E2 mejora la respuesta observada y
aumenta los cambios contados; si cada cambio tuviera costo real, podría reducir
el tiempo de CPU útil. El simulador no mide ese costo.

**¿Hay inanición?** Ningún proceso quedó sin terminar en las cargas finitas
probadas. Esto no es una prueba experimental de toda carga posible. RR reparte
turnos; FCFS puede retrasar tareas cortas detrás de una larga (efecto convoy).

**¿Qué se simplificó?** Una CPU, tiempos enteros, E/S fija sin cola de dispositivo,
sin costo temporal de cambios, sin prioridades efectivas ni recursos reales.

**¿Qué hizo la IA?** Describir la asistencia de `APORTES.md` y las modificaciones
que el equipo realmente revisó. Poder explicar un resultado y seguir una traza
es parte de la validación, no basta con ejecutar el programa.
