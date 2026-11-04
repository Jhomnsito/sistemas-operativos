"""Pruebas manualmente calculadas, de invariantes y contra un modelo por ticks."""
import contextlib
import io
import random
import unittest
from algorithms import simulate_fcfs, simulate_round_robin, print_comparison_report
from models import Process, ProcessState
from scenarios import scenarios


def tick_oracle(specs, quantum):
    """Modelo independiente por unidad de tiempo, con E/S y cola FIFO.

    specs: (pid, llegada, CPU total, eventos E/S). No usa clases del simulador.
    Devuelve inicio, fin, espera y bloqueo por PID.
    """
    data = {pid: {'arrival': arrival, 'left': cpu, 'used': 0, 'io': list(events),
                  'start': None, 'end': None, 'wait': 0, 'blocked': 0}
            for pid, arrival, cpu, events in specs}
    pending = [(arrival, index, pid) for index, (pid, arrival, _, _) in enumerate(specs)]
    serial = len(specs)
    ready, active, used_quantum, now = [], None, 0, 0
    while any(p['end'] is None for p in data.values()):
        due = sorted(e for e in pending if e[0] == now)
        for entry in due:
            pending.remove(entry)
            ready.append(entry[2])
        # Se resuelve el tick anterior después de admitir los eventos del límite.
        if active is not None:
            p = data[active]
            if p['left'] == 0:
                p['end'] = now
                active = None
            elif p['io'] and p['used'] == p['io'][0][0]:
                _, duration = p['io'].pop(0)
                p['blocked'] += duration
                pending.append((now + duration, serial, active))
                serial += 1
                active = None
            elif quantum is not None and used_quantum == quantum:
                ready.append(active)
                active = None
        if active is None and ready:
            active = ready.pop(0)
            used_quantum = 0
            if data[active]['start'] is None:
                data[active]['start'] = now
        if all(p['end'] is not None for p in data.values()):
            break
        for pid in ready:
            data[pid]['wait'] += 1
        if active is not None:
            data[active]['left'] -= 1
            data[active]['used'] += 1
            used_quantum += 1
        now += 1
        if now > 10000:
            raise AssertionError('El oráculo excedió su límite de prueba.')
    return {pid: (p['start'], p['end'], p['wait'], p['blocked']) for pid, p in data.items()}


class SimulatorTests(unittest.TestCase):
    def test_fcfs_manual(self):
        """Compara tiempos de FCFS con un caso resuelto a mano."""
        r = simulate_fcfs([Process(1, 0, 5), Process(2, 1, 3), Process(3, 2, 8), Process(4, 3, 6)])
        self.assertEqual([(p.pid, p.completion_time, p.waiting_time, p.response_time) for p in r],
                         [(1, 5, 0, 0), (2, 8, 4, 4), (3, 16, 6, 6), (4, 22, 13, 13)])
        self.assertEqual(r.metrics()['context_switches'], 3)

    def test_rr_manual(self):
        """Compara tiempos de RR con un caso resuelto a mano."""
        r = simulate_round_robin([Process(1, 0, 5), Process(2, 1, 3)], 2)
        p = {p.pid: p for p in r}
        self.assertEqual((p[1].completion_time, p[1].waiting_time, p[1].response_time), (8, 3, 0))
        self.assertEqual((p[2].completion_time, p[2].waiting_time, p[2].response_time), (7, 3, 1))
        self.assertEqual(r.metrics()['context_switches'], 4)

    def test_arrival_on_quantum_boundary(self):
        """Verifica admisión de una llegada en el límite exacto del turno."""
        r = simulate_round_robin([Process(1, 0, 4), Process(2, 2, 1)], 2)
        self.assertEqual([s['pid'] for s in r.timeline], [1, 2, 1])

    def test_stable_arrival_ties(self):
        """Comprueba que llegadas empatadas conserven orden de entrada."""
        r = simulate_fcfs([Process(2, 0, 1), Process(1, 0, 1)])
        self.assertEqual([p.pid for p in r], [2, 1])

    def test_idle(self):
        """Verifica tramos ociosos, espera nula y utilización desde el instante cero."""
        r = simulate_fcfs([Process(1, 3, 2), Process(2, 10, 3)])
        self.assertEqual(r.end_time, 13)
        self.assertEqual(r.metrics()['context_switches'], 0)
        self.assertAlmostEqual(r.metrics()['utilization_percent'], 500 / 13)
        self.assertEqual([(s['start'], s['end']) for s in r.timeline if s['pid'] is None], [(0, 3), (5, 10)])

    def test_one_process_rr(self):
        """Comprueba varios despachos de un único proceso sin falsos cambios de contexto."""
        r = simulate_round_robin([Process(1, 0, 7)], 2)
        self.assertEqual(r.metrics()['dispatches'], 4)
        self.assertEqual(r.metrics()['context_switches'], 0)
        self.assertEqual(r[0].waiting_time, 0)

    def test_io_manual(self):
        """Verifica un bloqueo y sus estados contra un cálculo manual."""
        r = simulate_fcfs([Process(1, 0, 4, io_events=[(2, 3)]), Process(2, 1, 2)])
        p = {p.pid: p for p in r}
        self.assertEqual((p[1].completion_time, p[1].waiting_time, p[1].blocked_time), (7, 0, 3))
        self.assertEqual((p[2].completion_time, p[2].waiting_time), (4, 1))
        self.assertEqual([e['state'] for e in r.events if e['pid'] == 1],
                         ['NUEVO', 'LISTO', 'EJECUCION', 'BLOQUEADO', 'LISTO', 'EJECUCION', 'FINALIZADO'])

    def test_multiple_io(self):
        """Comprueba que un proceso complete varias esperas de E/S."""
        for runner in (simulate_fcfs, lambda p: simulate_round_robin(p, 1)):
            r = runner([Process(1, 0, 6, io_events=[(1, 2), (4, 3)])])
            self.assertEqual((r[0].completion_time, r[0].blocked_time, r[0].waiting_time), (11, 5, 0))

    def test_io_on_quantum_boundary(self):
        """Verifica el bloqueo coincidente con el final del quantum."""
        r = simulate_round_robin([Process(1, 0, 4, io_events=[(2, 2)]), Process(2, 0, 5)], 2)
        self.assertIn({'time': 2, 'pid': 1, 'state': 'BLOQUEADO', 'reason': 'Inicio de E/S'}, r.events)
        self.assertEqual([s['pid'] for s in r.timeline], [1, 2, 1, 2, 2])

    def test_simultaneous_unblock_and_arrival(self):
        """Comprueba el orden de llegada y desbloqueo en un mismo instante."""
        r = simulate_fcfs([Process(1, 0, 2, io_events=[(1, 2)]), Process(2, 3, 1)])
        self.assertEqual([(s['start'], s['pid']) for s in r.timeline], [(0, 1), (1, None), (3, 2), (4, 1)])

    def test_empty(self):
        """Verifica resultados y reporte de una carga vacía sin división entre cero."""
        for r in (simulate_fcfs([]), simulate_round_robin([], 2)):
            self.assertEqual(r, [])
            self.assertTrue(all(v == 0 for v in r.metrics().values()))
            with contextlib.redirect_stdout(io.StringIO()):
                print_comparison_report('vacío', r)

    def test_bad_quantum(self):
        """Rechaza quantum nulo, negativo o de tipo inválido."""
        for q in (0, -1, 1.5, True, None, '3'):
            with self.subTest(q=q), self.assertRaises(ValueError):
                simulate_round_robin([Process(1, 0, 3)], q)

    def test_bad_process(self):
        """Rechaza especificaciones de proceso inválidas."""
        for args in ((0, 0, 3), (1, -1, 3), (1, 0, 0), (1, 0, -1),
                     (1, 0, 2.5), (1, True, 3), ('1', 0, 3)):
            with self.subTest(args=args), self.assertRaises(ValueError):
                Process(*args)

    def test_bad_io(self):
        """Rechaza puntos E/S mal formados, no crecientes o fuera del trabajo CPU."""
        for events in ([(0, 2)], [(3, 1)], [(1, 0)], [(2, 1), (1, 1)], [(1,)], [(1.5, 2)]):
            with self.subTest(events=events), self.assertRaises(ValueError):
                Process(1, 0, 3, io_events=events)

    def test_duplicate_pid_and_type(self):
        """Rechaza PID repetidos y elementos que no son Process."""
        for entries in ([Process(1, 0, 1), Process(1, 2, 1)], [object()]):
            with self.assertRaises(ValueError):
                simulate_fcfs(entries)

    def test_reuse_does_not_mutate_input(self):
        """Repite cargas para comprobar independencia y ausencia de mutaciones de entrada."""
        source = [Process(1, 0, 7), Process(2, 1, 2)]
        before = [vars(p).copy() for p in source]
        first = simulate_round_robin(source, 2)
        simulate_fcfs(source)
        second = simulate_round_robin(source, 2)
        self.assertEqual([vars(p) for p in source], before)
        self.assertEqual(first.timeline, second.timeline)
        self.assertEqual([vars(p) for p in first], [vars(p) for p in second])

    def test_large_quantum_matches_fcfs(self):
        """Comprueba equivalencia de RR con quantum suficiente y FCFS."""
        for _, _, _, source in scenarios():
            a, b = simulate_fcfs(source), simulate_round_robin(source, 1000)
            self.assertEqual(a.timeline, b.timeline)
            self.assertEqual(a.metrics(), b.metrics())

    def test_all_scenarios_invariants(self):
        """Verifica conservación de CPU, métricas y finalización de todas las cargas definidas."""
        for key, _, q, source in scenarios():
            for r in (simulate_fcfs(source), simulate_round_robin(source, q)):
                with self.subTest(scenario=key, algorithm=r.algorithm):
                    self.assertEqual(len(r), len(source))
                    self.assertEqual(r.metrics()['busy_time'], sum(p.burst_time for p in source))
                    self.assertEqual([e['time'] for e in r.events], sorted(e['time'] for e in r.events))
                    for p in r:
                        self.assertEqual(p.state, ProcessState.TERMINATED)
                        self.assertEqual(p.remaining_time, 0)
                        self.assertEqual(p.waiting_time, p.turnaround_time - p.burst_time - p.blocked_time)
                        self.assertGreaterEqual(p.waiting_time, 0)
                        self.assertGreaterEqual(p.response_time, 0)
                    for a, b in zip(r.timeline, r.timeline[1:]):
                        self.assertEqual(a['end'], b['start'])
                    for s in r.timeline:
                        self.assertGreater(s['end'], s['start'])
                    states = {}
                    for e in r.events:
                        states[(e['pid'], e['state'])] = True
                    self.assertTrue(all((p.pid, 'FINALIZADO') in states for p in source))

    def test_200_generated_cases_against_tick_oracle(self):
        """Compara 200 cargas y cuatro configuraciones con un modelo independiente por ticks."""
        rng = random.Random(2620)
        for case in range(200):
            specs = []
            for pid in range(1, rng.randint(1, 6) + 1):
                cpu = rng.randint(1, 12)
                points = sorted(rng.sample(range(1, cpu), rng.randint(0, min(2, cpu - 1))))
                specs.append((pid, rng.randint(0, 10), cpu, [(p, rng.randint(1, 5)) for p in points]))
            rng.shuffle(specs)
            for q in (None, 1, 2, 5):
                with self.subTest(case=case, quantum=q):
                    source = [Process(pid, arrival, cpu, io_events=events) for pid, arrival, cpu, events in specs]
                    r = simulate_fcfs(source) if q is None else simulate_round_robin(source, q)
                    actual = {p.pid: (p.start_time, p.completion_time, p.waiting_time, p.blocked_time) for p in r}
                    self.assertEqual(actual, tick_oracle(specs, q))


if __name__ == '__main__':
    unittest.main()
