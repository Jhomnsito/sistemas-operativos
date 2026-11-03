# Guion de sustentación para Esteban Peña y Andrés Gámez

Esta es una propuesta para repartir la exposición. No afirma quién escribió cada
archivo ni sustituye el registro de aportes reales. Ambos deben comprender el
proyecto completo y poder ejecutar la demostración.

## Distribución de los veinte minutos

| Tiempo | Integrante | Contenido |
|---|---|---|
| 0 a 3 minutos | Esteban Peña | Tema, problema, objetivo y explicación de FCFS y Round Robin |
| 3 a 5 minutos | Andrés Gámez | Diseño, archivos, estados y datos de los escenarios |
| 5 a 9 minutos | Andrés Gámez | Ejecutar el programa y demostrar el escenario del proceso largo |
| 9 a 12 minutos | Esteban Peña | Interpretar espera, respuesta y retorno; contrastar E1 con E2 |
| 12 a 14 minutos | Andrés Gámez | Ejecutar las pruebas y explicar dos comprobaciones concretas |
| 14 a 16 minutos | Esteban Peña | Limitaciones, riesgos, mejoras y conclusión |
| 16 a 20 minutos | Ambos | Preguntas del profesor y aclaración de aportes reales |

## Apertura de Esteban

“Somos Esteban Peña y Andrés Gámez. Nuestro proyecto trata sobre gestión de
procesos y planificación de CPU, la opción uno. Comparamos FCFS, que atiende
por orden de entrada a la cola, con Round Robin, que reparte turnos de CPU.
Queremos observar cómo cambia la espera, la primera respuesta y el tiempo hasta
finalizar cuando se usan las mismas cargas.”

Explicar después: FCFS mantiene la CPU hasta finalizar o bloquearse; RR limita el
turno mediante un quantum. No afirmar que RR siempre es mejor.

## Diseño y demostración de Andrés

“Representamos los procesos con objetos y sus estados. Una cola decide quién
recibe la CPU y otra organiza las llegadas y el fin de las esperas de E/S.
Tenemos cinco escenarios. Los tres originales comparan cargas sin E/S;
añadimos uno de bloqueo y otro de CPU ociosa.”

Abrir una terminal en la carpeta del proyecto y ejecutar:

```powershell
python main.py --output evidencias_sustentacion
```

Mostrar el escenario E2. Sus entradas son P1: llegada 0, CPU 12; P2: llegada 1,
CPU 2; P3: llegada 2, CPU 4. RR usa quantum 3.

“En FCFS, el segundo proceso llega en uno y empieza en doce: espera once
unidades. En RR empieza en tres y espera dos. El programa acaba de calcular los
resultados y guardarlos. No estamos mostrando únicamente una captura anterior.”

Mostrar también E4 en `estados.csv`: P1 se bloquea en 2 y vuelve a LISTO en 6.
Volver a listo no significa recibir CPU inmediatamente. Si hay tiempo, mostrar
los periodos ociosos de E5 en `cpu.csv`.

## Interpretación de Esteban

“Espera es el tiempo en la cola de listos. Respuesta es el tiempo desde la llegada
hasta el primer uso de CPU. Retorno es el tiempo desde que llega hasta que termina.
El tiempo bloqueado por E/S no se cuenta como espera en listo.”

“En E2, RR reduce la respuesta media de 7.67 a 1.67 y la espera media de 7.67 a
4.67. Pero en E1, aunque mejora la respuesta, aumenta la espera y el retorno.
La elección depende de la carga y de la métrica que se quiera mejorar.”

No atribuir el aumento del retorno a un costo temporal de cambios: en este
modelo ese costo es cero. El orden de los turnos explica los resultados.

## Pruebas de Andrés

Ejecutar las pruebas existentes, sin editar ni preparar resultados manualmente:

```powershell
python -m unittest -v
```

“Cada línea terminada en ok indica una comprobación aprobada. El conjunto
incluye 19 métodos de prueba. Uno compara 200 cargas bajo cuatro configuraciones
con un segundo modelo: en total son 800 comparaciones.”

Elegir una comprobación breve para explicar, por ejemplo la validación de quantum:

```powershell
python -m unittest -v test_simulator.SimulatorTests.test_bad_quantum
```

“Esta prueba comprueba que el programa rechaza valores inválidos. Que termine
bien significa que produjo el error esperado, no que aceptó un quantum cero.”

Si preguntan por E/S, se puede ejecutar el caso calculado a mano:

```powershell
python -m unittest -v test_simulator.SimulatorTests.test_io_manual
```

Revisar el resultado real antes de afirmar que todas aprobaron. Si aparece un
fallo, reconocerlo, leerlo y explicar qué quedó pendiente.

## Cierre de Esteban

“Concluimos que RR favorece la respuesta inicial en cuatro de nuestras cinco
cargas, mientras que el efecto en espera y retorno varía. El modelo usa una CPU,
tiempos enteros y E/S fija. No incluye el costo temporal de cambio de contexto
ni una cola de dispositivo; por eso no mide el rendimiento real del computador.
Como mejoras proponemos incorporar esos costos y la contención de E/S.”

“Se utilizó IA como apoyo para revisar, corregir, probar y documentar el proyecto.
La asistencia está declarada. Los integrantes debemos comprender y verificar
el código y sustentar los resultados.”

## Preparación que ambos deben completar

- Confirmar que el comando de Python funciona en el equipo de presentación.
- Ensayar la demostración y abrir previamente código, evidencias e informe.
- Registrar en `APORTES.md` qué hizo realmente cada uno y con qué evidencia.
- Añadir el enlace real de la carpeta compartida o repositorio.
- Aportar la constancia de semana 8 si existe.
- Poder responder las preguntas del conjunto; este reparto no limita la evaluación individual.

Los nombres están confirmados. Las contribuciones y antecedentes pendientes no
se completaron por suposición.
