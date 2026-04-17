class Tracer:
    def __init__(self):
        self.events: list[dict] = []

    def add(self, type_: str, **payload):
        self.events.append({"type": type_, "payload": payload})
