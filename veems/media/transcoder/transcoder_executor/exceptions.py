class TranscodeException(Exception):
    def __init__(self, message, stderr=None):
        self.stderr = stderr
        self.message = message
