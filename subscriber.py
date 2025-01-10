
class Subscriber:
    def __init__(self, publisher):
        self.publisher = publisher

    def register(self, event_type: str, callback):
        self.publisher.subscribe(event_type, callback)

    def unregister(self, event_type : str, callback):
        self.publisher.unsubscribe(event_type, callback)