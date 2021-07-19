class Subscription:
    def __init__(self):
        self.subscribers = {}

    def subscribe(self, listener, function):
        self.subscribers[listener] = function

    def push_notification(self):
        for listener in self.subscribers.keys():
            self.subscribers[listener]()

class PageSubscription(Subscription):
    def __init__(self):
        super().__init__()
