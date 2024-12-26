import pygame


class EventManager:
    """Centralized system for managing inputs and events"""

    def __init__(self):
        self.keys = set()
        self.key_down_actions = {}
        self.key_up_actions = {}
        self.quit = False

    def register_key_action(self, key, action, event_type):
        """
        Register an action for a keypress or key release.
        - `key`: Key to listen for (e.g., pygame.K_SPACE).
        - `action`: Callable action to execute when the key event occurs.
        - `event_type`: Either `pygame.KEYDOWN` or `pygame.KEYUP`.
        """
        if event_type == pygame.KEYDOWN:
            self.key_down_actions[key] = action
        elif event_type == pygame.KEYUP:
            self.key_up_actions[key] = action

    def process_event(self):
        """Poll event and execute registered actions"""
        self.keys.clear()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit = True
            elif event.type == pygame.KEYDOWN and event.key in self.key_down_actions:
                self.key_down_actions[event.key]()
            elif event.type == pygame.KEYUP and event.key in self.key_up_actions:
                self.key_up_actions[event.key]()

    def is_quit(self):
        """Check if the quit event is triggered"""
        return self.quit
