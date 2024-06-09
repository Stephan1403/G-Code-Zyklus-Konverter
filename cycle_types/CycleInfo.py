from typing import List, Dict


class CycleInfo:
    def __init__(self, number: int, steps: List, params: Dict) -> None:
        self.number = number
        self.steps = steps
        self.params = params
