class Publisher:
    def __init__(self):
        self.subscribers = {}

    def subscribe(self, event_type: str, callback):
        """
        Subscribing tells publisher what to call, on what event
        """
        if event_type not in self.subscribers:
            self.subscribers[event_type] = [] # variable amount of callbacks
        self.subscribers[event_type].append(callback)

    def unsubscribe(self, event_type: str, callback):
        if event_type in self.subscribers:
            self.subscribers[event_type].remove(callback)
        else:
            raise AttributeError(f"No event type {event_type} to unsubscribe to")
    
    def publish(self, event_type: str, data=None):
        """
        Data is a kwarg to pass to callback.
        Each callback has to include data as its argument
        """
        if event_type in self.subscribers:
            for callback in self.subscribers[event_type]:
                callback(data) # call the method/function
        else:
            raise AttributeError(f"No subscriber to listen to {event_type}")

