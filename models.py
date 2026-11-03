"""Datos de entrada y estados del simulador. Los tiempos son unidades enteras."""
from enum import Enum


class ProcessState(Enum):
    NEW = 'NUEVO'
    READY = 'LISTO'
    RUNNING = 'EJECUCION'
    BLOCKED = 'BLOQUEADO'
    TERMINATED = 'FINALIZADO'


def require_int(name, value, minimum):
    if type(value) is not int or value < minimum:
        raise ValueError(f'{name} debe ser un entero >= {minimum}.')


class Process:
    def __init__(self, pid, arrival_time, burst_time, priority=0, io_events=None):
        require_int('pid', pid, 1)
        require_int('arrival_time', arrival_time, 0)
        require_int('burst_time', burst_time, 1)
        if type(priority) is not int:
            raise ValueError('priority debe ser un entero.')
        # Cada par indica (CPU acumulada antes de bloquear, duración de E/S).
        events = []
        previous = 0
        for event in (() if io_events is None else io_events):
            if not isinstance(event, (list, tuple)) or len(event) != 2:
                raise ValueError('Cada evento E/S debe ser un par (CPU acumulada, duración).')
            after, duration = event
            require_int('CPU antes de E/S', after, 1)
            require_int('duración de E/S', duration, 1)
            if not previous < after < burst_time:
                raise ValueError('Los puntos de E/S deben crecer y ser menores que la CPU total.')
            events.append((after, duration))
            previous = after
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.priority = priority  # Conservado por compatibilidad; FCFS y RR no lo usan.
        self.io_events = tuple(events)
        self.remaining_time = burst_time
        self.state = ProcessState.NEW
        self.start_time = -1
        self.completion_time = 0
        self.waiting_time = 0
        self.turnaround_time = 0
        self.response_time = -1
        self.blocked_time = 0
        self._io_index = 0
        self._ready_since = arrival_time

    def fresh_copy(self):
        return Process(self.pid, self.arrival_time, self.burst_time,
                       self.priority, self.io_events)

    def __repr__(self):
        return (f'P{self.pid}(Llegada={self.arrival_time}, CPU={self.burst_time}, '
                f'Restante={self.remaining_time}, Estado={self.state.value})')
