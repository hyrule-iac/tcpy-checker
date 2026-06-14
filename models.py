# Creating new servers class model and CheckResult
class Server:
    def __init__(self, name, ip, port, service=None):
        self.name = name
        self.ip = ip
        self.port = port
        self.service = service
        
    def to_dict(self):
        return {
            "name": self.name,
            "ip": self.ip,
            "port": self.port,
            "service": self.service
        }
    def __repr__(self):
        return f"Server(name={self.name}, ip={self.ip}, port={self.port}, service={self.service})"


class CheckResult:
    def __init__(self, server: Server):
        self.server: Server = server
        self.success: bool | None = None
        self.latency_ms: float | None = None
        self.attempts: int = 0
        self.error_type: str | None = None
        self.error_message: str | None = None
        self.timestamp: str | None = None
        self.source_host: str | None = None

    def to_dict(self):
        return {
            "server": self.server.to_dict(),
            "success": self.success,
            "latency_ms": self.latency_ms,
            "attempts": self.attempts,
            "error_type": self.error_type,
            "error_message": self.error_message,
            "timestamp": self.timestamp,
            "source_host": self.source_host,
        }
