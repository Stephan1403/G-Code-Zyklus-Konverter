# Handles file input
# Finds cycles
# from .types.Cycle import Cycle
# from .types.GCode import GCode

from cycle_types.Cycle import Cycle
from cycle_types.GCode import GCode


class GCodeReader:
    def __init__(self, gcode_path: str) -> None:
        self.gcode_path = gcode_path

    def get_next_code(self) -> Cycle | GCode | None:
        pass
