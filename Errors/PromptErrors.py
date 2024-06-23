"""All Exceptions that get thrown during Prompt creation and usage"""


class InstructionNotFoundError(Exception):
    def __init__(self, missing_key, message=None):
        if message is None:
            message = f"Instruction with key {missing_key} not found"
        super().__init__(message)
