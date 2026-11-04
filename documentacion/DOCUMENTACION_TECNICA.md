# Documentación técnica de funciones

El motor comparte la implementación de FCFS y RR. Las copias de entrada evitan contaminación entre corridas. El simulador avanza por eventos y salta los intervalos ociosos; la cola de listos usa deque y las llegadas/fines de E/S usan heapq. El costo crece con procesos, eventos y turnos registrados, no con cada unidad ociosa. Las trazas se conservan en memoria.

La interfaz admite de 1 a 30 procesos, PID/llegada/CPU enteros de hasta 1000, quantum de 1 a 1000, hasta 20 eventos E/S por proceso y un máximo total de 2000 unidades CPU. La duración E/S es positiva y sus puntos de bloqueo deben crecer antes del fin de CPU. Los límites visuales no alteran las políticas del motor.

La API local solo sirve la página, JavaScript, CSS y escenarios; las operaciones POST comparan cargas o ejecutan pruebas. Los cuerpos JSON se limitan a 24000 bytes; las pruebas tienen timeout de 45 segundos. Las tablas de estados se construyen al desplegar su panel.

## algorithms.py

### SimulationResult.__init__(self, algorithm, processes, timeline, events, end_time)

Agrupa procesos terminados, tramos CPU, estados y último instante.

### SimulationResult.metrics(self)

Calcula medias, máximos, utilización, productividad, cambios y despachos.

La utilización cuenta desde t=0 y los cambios excluyen tramos ociosos.
Una carga vacía devuelve métricas cero; los tiempos son simulados.

### _simulate(process_list, quantum)

Simula una CPU con eventos, FIFO y copias de la entrada.

quantum=None selecciona FCFS; un entero positivo limita los turnos de RR.
Devuelve SimulationResult sin modificar los Process originales.
Valida tipo y unicidad de PID. La creación es simulada y E/S no compite
por un dispositivo compartido. No recorre unidades ociosas una por una.

### simulate_fcfs(process_list)

Devuelve FCFS no expropiativo: conserva CPU hasta terminar o bloquearse.

Recibe Process; no modifica la carga y rechaza PID duplicados.

### simulate_round_robin(process_list, quantum)

Devuelve RR para una carga Process y quantum entero positivo.

Reinserta al final de listos al agotar turno; lanza ValueError si Q es inválido.

### print_comparison_report(algorithm_name, completed_processes)

Imprime métricas y traza de procesos terminados; acepta una carga vacía.

## app_visual.py

### scenario_data()

Devuelve los cinco escenarios como registros serializables a JSON.

### save_evidence(kind, data)

Guarda una ejecución fechada y devuelve sus datos con la ruta de evidencia.

Args: kind identifica la operación; data contiene entradas y resultados.
Raises: OSError si la carpeta o el JSON no pueden escribirse.

### compare(payload)

Valida una carga, compara FCFS/RR y guarda métricas, procesos y trazas.

payload contiene processes (pid, arrival, cpu, io) y quantum entero.
Devuelve un diccionario JSON. Lanza ValueError ante una carga inválida.
Los límites acotan el volumen de trazas representado por el navegador.

### run_tests()

Ejecuta unittest con límite de 45 s y conserva salida y código de retorno.

Devuelve evidencia de éxito, fallo o timeout; no interpreta salida antigua.

### Handler.reply(self, code, payload, content_type='application/json; charset=utf-8')

Envía bytes o un objeto JSON con estado HTTP y longitud de contenido.

### Handler.local_request(self)

Comprueba que Host y Origin correspondan al puerto local del servidor.

### Handler.do_GET(self)

Sirve la interfaz y sus recursos explícitos o los escenarios iniciales.

### Handler.do_POST(self)

Recibe JSON acotado para comparar o probar; devuelve errores legibles.

### main()

Abre un servidor local, opcionalmente el navegador, y espera hasta Ctrl+C.

## main.py

### write_csv(path, rows)

Escribe registros no vacíos como CSV UTF-8 con cabecera y orden de campos.

### main(argv=None)

Ejecuta cinco escenarios y sensibilidad de Q; exporta CSV/JSON a --output.

Devuelve 0 al completar y 1 ante errores de entrada o escritura.
argv permite invocación desde pruebas o desde la línea de comandos.

## models.py

### require_int(name, value, minimum)

Rechaza con ValueError un valor no entero, booleano o menor que minimum.

### Process.__init__(self, pid, arrival_time, burst_time, priority=0, io_events=None)

Valida y crea un registro NUEVO sin tiempo de CPU consumido.

pid es único en cada carga; arrival_time >= 0 y burst_time >= 1.
io_events contiene pares (CPU acumulada, duración), crecientes y
anteriores al fin de CPU. priority se conserva pero no decide turnos.
Lanza ValueError cuando la especificación viola estas restricciones.

### Process.fresh_copy(self)

Devuelve otro Process con igual carga y todas sus métricas reiniciadas.

### Process.__repr__(self)

Devuelve una descripción breve del PID, carga, CPU restante y estado.

## scenarios.py

### scenarios()

Construye cargas nuevas (id, descripción, quantum RR, lista Process).

E1-E3 conservan las cargas originales; E4 cubre E/S y E5 tiempos ociosos.

## test_app_visual.py

### QuietHandler.log_message(self, format, *args)

Silencia el diagnóstico HTTP para conservar legible la salida de unittest.

### AppTests.setUpClass(cls)

Inicia un servidor HTTP real en un puerto local libre para las pruebas.

### AppTests.tearDownClass(cls)

Detiene el servidor, libera su puerto y espera al hilo de pruebas.

### AppTests.request(self, path, payload=None, **headers)

Envía una petición real y devuelve estado y cuerpo, también para respuestas de error.

### AppTests.example(self)

Obtiene del servidor la carga E2 para construir una comparación reproducible.

### AppTests.test_page_and_presets(self)

Comprueba acceso a la página y presencia de los cinco escenarios.

### AppTests.test_manual_example_over_http(self)

Verifica por HTTP las esperas manuales de P2 y conservación de 18 unidades CPU.

### AppTests.test_zero_quantum_is_rejected(self)

Comprueba el rechazo HTTP de quantum cero.

### AppTests.test_duplicate_pid_is_rejected(self)

Comprueba que dos procesos con igual PID no se admiten.

### AppTests.test_fractional_input_is_rejected(self)

Rechaza CPU fraccionaria cuando el modelo requiere tiempos enteros.

### AppTests.test_unknown_path_does_not_serve_files(self)

Verifica que rutas arbitrarias no expongan archivos del proyecto.

### AppTests.test_foreign_origin_is_rejected(self)

Rechaza una solicitud procedente de un origen distinto del servidor local.

### AppTests.test_io_input_is_preserved(self)

Comprueba bloqueo de cuatro unidades y transiciones BLOQUEADO para E4.

### AppTests.test_invalid_encoding_returns_readable_error(self)

Comprueba que bytes no UTF-8 reciben un error JSON en vez de cortar la conexión.

### AppTests.test_excessive_cpu_is_rejected_before_simulation(self)

Rechaza una carga visual que supera el límite total de CPU.

### AppTests.test_script_and_stylesheet_are_served(self)

Verifica que JavaScript y CSS separados sean accesibles como recursos explícitos.

### AppTests.test_missing_resource_returns_readable_error(self)

Comprueba respuesta JSON 500 si falta un archivo necesario para la interfaz.

## test_simulator.py

### tick_oracle(specs, quantum)

Modelo independiente por unidad de tiempo, con E/S y cola FIFO.

specs: (pid, llegada, CPU total, eventos E/S). No usa clases del simulador.
Devuelve inicio, fin, espera y bloqueo por PID.

### SimulatorTests.test_fcfs_manual(self)

Compara tiempos de FCFS con un caso resuelto a mano.

### SimulatorTests.test_rr_manual(self)

Compara tiempos de RR con un caso resuelto a mano.

### SimulatorTests.test_arrival_on_quantum_boundary(self)

Verifica admisión de una llegada en el límite exacto del turno.

### SimulatorTests.test_stable_arrival_ties(self)

Comprueba que llegadas empatadas conserven orden de entrada.

### SimulatorTests.test_idle(self)

Verifica tramos ociosos, espera nula y utilización desde el instante cero.

### SimulatorTests.test_one_process_rr(self)

Comprueba varios despachos de un único proceso sin falsos cambios de contexto.

### SimulatorTests.test_io_manual(self)

Verifica un bloqueo y sus estados contra un cálculo manual.

### SimulatorTests.test_multiple_io(self)

Comprueba que un proceso complete varias esperas de E/S.

### SimulatorTests.test_io_on_quantum_boundary(self)

Verifica el bloqueo coincidente con el final del quantum.

### SimulatorTests.test_simultaneous_unblock_and_arrival(self)

Comprueba el orden de llegada y desbloqueo en un mismo instante.

### SimulatorTests.test_empty(self)

Verifica resultados y reporte de una carga vacía sin división entre cero.

### SimulatorTests.test_bad_quantum(self)

Rechaza quantum nulo, negativo o de tipo inválido.

### SimulatorTests.test_bad_process(self)

Rechaza especificaciones de proceso inválidas.

### SimulatorTests.test_bad_io(self)

Rechaza puntos E/S mal formados, no crecientes o fuera del trabajo CPU.

### SimulatorTests.test_duplicate_pid_and_type(self)

Rechaza PID repetidos y elementos que no son Process.

### SimulatorTests.test_reuse_does_not_mutate_input(self)

Repite cargas para comprobar independencia y ausencia de mutaciones de entrada.

### SimulatorTests.test_large_quantum_matches_fcfs(self)

Comprueba equivalencia de RR con quantum suficiente y FCFS.

### SimulatorTests.test_all_scenarios_invariants(self)

Verifica conservación de CPU, métricas y finalización de todas las cargas definidas.

### SimulatorTests.test_200_generated_cases_against_tick_oracle(self)

Compara 200 cargas y cuatro configuraciones con un modelo independiente por ticks.

## interfaz.js y estilos.css

interfaz.js solicita los datos al servidor y presenta sus resultados; no implementa un segundo planificador. Sus funciones documentadas construyen controles y tablas, gestionan vistas, reproducen trazas existentes, cargan estados bajo demanda y descargan JSON. estilos.css contiene la presentación adaptable; interfaz.html define la estructura y controles.
