class EventDispatcher:
    def __init__(self):
        self.listeners = {}

    def add_listener(self, event_name, callback):
        """Add a listener for a specific event."""
        if event_name not in self.listeners:
            self.listeners[event_name] = []
        self.listeners[event_name].append(callback)

    def remove_listener(self, event_name, callback):
        """Remove a specific listener for a specific event."""
        if event_name in self.listeners:
            self.listeners[event_name].remove(callback)

    def dispatch_event(self, event_name, data=None):
        """Dispatch an event to all listeners for that event."""
        if event_name in self.listeners:
            for callback in self.listeners[event_name]:
                callback(data)

# You can instantiate this class in your main.py and pass it around to Model, View, Controller
# For example, in your main.py:
# event_dispatcher = EventDispatcher()
