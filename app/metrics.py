from prometheus_client import Counter, Gauge

crdt_operations_total = Counter('crdt_operations_total', 'Total CRDT operations', ['operation_type'])
crdt_conflicts_resolved = Counter('crdt_conflicts_resolved', 'Number of conflicts resolved')
active_sessions = Gauge('active_sessions', 'Number of active WebSocket sessions')