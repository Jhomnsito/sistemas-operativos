"""FCFS y Round Robin con eventos de llegada y finalización de E/S.

CPU única, sin costo temporal de despacho ni cambio de contexto. Cada E/S
tiene duración fija y puede solaparse con otras: no se simula cola de dispositivo.
"""
from collections import deque
import heapq
from itertools import count
from models import Process, ProcessState, require_int


class SimulationResult(list):
    """Lista de procesos terminados más trazas verificables de la ejecución."""
    def __init__(self, algorithm, processes, timeline, events, end_time):
        super().__init__(processes)
        self.algorithm = algorithm
        self.timeline = timeline
        self.events = events
        self.end_time = end_time

    def metrics(self):
        n = len(self)
        busy = sum(s['end'] - s['start'] for s in self.timeline if s['pid'] is not None)
        changes = sum(a['pid'] is not None and b['pid'] is not None and a['pid'] != b['pid']
                      for a, b in zip(self.timeline, self.timeline[1:]))
        return {
            'processes': n,
            'avg_waiting': sum(p.waiting_time for p in self) / n if n else 0,
            'avg_turnaround': sum(p.turnaround_time for p in self) / n if n else 0,
            'avg_response': sum(p.response_time for p in self) / n if n else 0,
            'max_waiting': max((p.waiting_time for p in self), default=0),
            'max_response': max((p.response_time for p in self), default=0),
            'context_switches': changes,
            'dispatches': sum(s['pid'] is not None for s in self.timeline),
            'end_time': self.end_time,
            'busy_time': busy,
            'utilization_percent': 100 * busy / self.end_time if self.end_time else 0,
            'throughput': n / self.end_time if self.end_time else 0,
        }


def _simulate(process_list, quantum):
    source = list(process_list)
    if any(not isinstance(p, Process) for p in source):
        raise ValueError('La entrada debe contener objetos Process.')
    if len({p.pid for p in source}) != len(source):
        raise ValueError('Los PID deben ser únicos dentro de un escenario.')
    processes = [p.fresh_copy() for p in source]
    pending, ready, done, timeline, events = [], deque(), [], [], []
    sequence = count()
    now = 0

    def transition(p, state, time, reason):
        p.state = state
        events.append({'time': time, 'pid': p.pid, 'state': state.value, 'reason': reason})

    for p in processes:
        transition(p, ProcessState.NEW, 0, 'Creación del proceso simulado')
        heapq.heappush(pending, (p.arrival_time, next(sequence), p, 'Llegada'))

    def release_until(time):
        # Desempate por orden de registro. A igual instante, las llegadas iniciales
        # preceden a los desbloqueos; ambos preceden a la reinserción por quantum.
        while pending and pending[0][0] <= time:
            available, _, p, reason = heapq.heappop(pending)
            transition(p, ProcessState.READY, available, reason)
            p._ready_since = available
            ready.append(p)

    while pending or ready:
        release_until(now)
        if not ready:
            following = pending[0][0]
            timeline.append({'start': now, 'end': following, 'pid': None})
            now = following
            release_until(now)
        p = ready.popleft()
        p.waiting_time += now - p._ready_since
        if p.start_time == -1:
            p.start_time = now
            p.response_time = now - p.arrival_time
        transition(p, ProcessState.RUNNING, now, 'Despacho de CPU')
        consumed = p.burst_time - p.remaining_time
        has_io = p._io_index < len(p.io_events)
        until_io = p.io_events[p._io_index][0] - consumed if has_io else p.remaining_time
        duration = min(p.remaining_time, until_io,
                       quantum if quantum is not None else p.remaining_time)
        timeline.append({'start': now, 'end': now + duration, 'pid': p.pid})
        now += duration
        p.remaining_time -= duration
        release_until(now)
        if p.remaining_time == 0:
            p.completion_time = now
            p.turnaround_time = now - p.arrival_time
            assert p.waiting_time == p.turnaround_time - p.burst_time - p.blocked_time
            transition(p, ProcessState.TERMINATED, now, 'CPU total completada')
            done.append(p)
        elif has_io and p.burst_time - p.remaining_time == p.io_events[p._io_index][0]:
            io_duration = p.io_events[p._io_index][1]
            p.blocked_time += io_duration
            p._io_index += 1
            transition(p, ProcessState.BLOCKED, now, 'Inicio de E/S')
            heapq.heappush(pending, (now + io_duration, next(sequence), p, 'Fin de E/S'))
        else:
            transition(p, ProcessState.READY, now, 'Fin de quantum')
            p._ready_since = now
            ready.append(p)
    return SimulationResult('FCFS' if quantum is None else f'RR Q={quantum}',
                            done, timeline, events, now)


def simulate_fcfs(process_list):
    """FCFS no expropiativo: conserva CPU hasta finalizar o bloquearse."""
    return _simulate(process_list, None)


def simulate_round_robin(process_list, quantum):
    require_int('quantum', quantum, 1)
    return _simulate(process_list, quantum)


def print_comparison_report(algorithm_name, completed_processes):
    print(f'\nREPORTE: {algorithm_name}')
    print(f'{"PID":<6} {"Llegada":>8} {"CPU":>6} {"E/S":>6} {"Fin":>6} '
          f'{"Espera":>8} {"Retorno":>8} {"Respuesta":>10}')
    for p in sorted(completed_processes, key=lambda p: p.pid):
        print(f'P{p.pid:<5} {p.arrival_time:>8} {p.burst_time:>6} {p.blocked_time:>6} '
              f'{p.completion_time:>6} {p.waiting_time:>8} {p.turnaround_time:>8} {p.response_time:>10}')
    n = len(completed_processes)
    if not n:
        print('Sin procesos. Promedios definidos como 0 por convención del simulador.')
    for field, label in [('waiting_time', 'Espera'), ('turnaround_time', 'Retorno'),
                         ('response_time', 'Respuesta')]:
        average = sum(getattr(p, field) for p in completed_processes) / n if n else 0
        print(f'{label} promedio: {average:.4f}')
    if isinstance(completed_processes, SimulationResult):
        m = completed_processes.metrics()
        print(f'Cambios de contexto: {m["context_switches"]}; despachos: {m["dispatches"]}; '
              f'CPU ocupada: {m["busy_time"]}/{m["end_time"]}; '
              f'utilización: {m["utilization_percent"]:.2f}%')
        print('Traza CPU: ' + ' | '.join(
            f'{s["start"]}-{s["end"]}:' + ('OCIOSA' if s['pid'] is None else f'P{s["pid"]}')
            for s in completed_processes.timeline))
