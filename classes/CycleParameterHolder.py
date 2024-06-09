from typing import List
from cycle_types.Cycle import Cycle

class CycleParameterHolder:
    """
    A class that holds a list of parameterized cycles
    """
    parameterized_cycles: List[Cycle]
    def add_parameterized_cycle(self, cycle: Cycle):
        """
        Adds a cycle to the list of parameterized cycles
        """
        self.parameterized_cycles.append(cycle)
    def get_parerized_cycle(self, name: str) -> Cycle | None:
        """
        Returns a cycle with the given name if it exists, otherwise returns None
        uses name as a key, because maybe we could have multiple cycles with the same number,
        but with other names
        """
        for cycle in self.parameterized_cycles:
            if cycle.name == name:
                return cycle
        return None
    def delete_parameterized_cycle(self, name: str) -> bool:
        """
        Deletes a cycle with the given name if it exists, otherwise returns False
        """
        for cycle in self.parameterized_cycles:
            if cycle.name == name:
                self.parameterized_cycles.remove(cycle)
                return True
        return False
