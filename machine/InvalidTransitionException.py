class InvalidTransitionException(Exception):
    def __init__(self, message="Invalid origin state"):
        self.message = message
        super().__init__(self.message)