class Scene:
    def __init__(self):
        self.next_state = None

    def update(self, screen, keys, events, dt=None):
        raise NotImplementedError

    def switch_to(self, state):
        self.next_state = state