import copy
from typing import Literal
from Errors.GCodeError import GCodeException
from cycle_types.Cycle import Cycle

class GCodeReader:
    converted_lines: list[str | Cycle] = []
    last_cycle_def: Cycle
    reader_index: int = -1

    def __init__(self, gcode_path: str) -> None:
        self.gcode_path = gcode_path
        lines = self.__read_file()
        lines_for_detection = lines
        for index, l in enumerate(lines_for_detection): # removes all linenumbers at start
            while l.startswith(tuple(str(i) for i in range(10))):
                l = l[1:]
            l = l.strip()
            lines_for_detection[index] = l
        skip: int = 0
        for i, line in enumerate(lines_for_detection):
            if skip > 0: # skip lines with parameters from cycle definition
                skip -= 1
                continue
            if line.startswith("CYCL DEF"):
                skip = self.__cycle_def_handler(line, lines[i+1:])
            elif line.startswith("CYCL CALL POS"):
                self.__cycle_call_pos_handler(line)
            elif line.startswith("CYCL CALL PAT"):
                raise NotImplementedError("CYCL CALL PAT not implemented yet")
            elif line.startswith("CYCL CALL"):
                self.__cycle_call_handler(line)
            else: self.__normal_gcode_handler(line)

    def get_next_code(self) -> Cycle | str | None:
        self.reader_index += 1
        if self.reader_index >= len(self.converted_lines):
            return None
        return self.converted_lines[self.reader_index]

    def __cycle_def_handler(self, line: str, lines_after: list[str]) -> int:
        number = int(line.split(" ")[2])
        name = line.split(" ")[3]
        i: int = 0
        params: dict[str, str] = {}
        while lines_after[i].startswith("Q"):
            line = lines_after[i]
            parameter_name = line.split(" ")[0].split("=")[0]
            parameter_value = line.split("=")[1].split(" ")[0]
            params[parameter_name] = parameter_value
            i+=1
        cycle = Cycle()
        cycle.number = number
        cycle.name = name
        cycle.params = params
        self.last_cycle_def = cycle
        return i # returns the amount of lines that were read, so that the main loop can skip them

    def __cycle_call_handler(self, line: str):
        cycle = copy.copy(self.last_cycle_def)
        if cycle is None:
            raise GCodeException("No cycle defined before CYCL CALL")
        if self.__get_cycle_pos(line, "F") is not None:
            cycle.speed = "F" + self.__get_cycle_pos(line, "F")
        self.converted_lines.append(cycle)

    def __cycle_call_pos_handler(self, line: str):
        cycle = copy.copy(self.last_cycle_def)
        if cycle is None:
            raise GCodeException("No cycle defined before CYCL CALL")
        cycle.x = float(self.__get_cycle_pos(line, "X"))
        cycle.y = float(self.__get_cycle_pos(line, "Y"))
        cycle.z = float(self.__get_cycle_pos(line, "Z"))
        if self.__get_cycle_pos(line, "F") is not None:
            cycle.speed = "F" + self.__get_cycle_pos(line, "F")
        self.converted_lines.append(cycle)

    def __normal_gcode_handler(self, line: str):
        self.converted_lines.append(line)

    def __read_file(self) -> list[str]:
        lines: list[str] = []
        with open(self.gcode_path, "r", encoding="utf-8") as file:
            lines = file.readlines()
        for i, line in enumerate(lines):
            lines[i] = line.strip()
        return lines

    def __get_cycle_pos(self, line: str, coord: Literal["X", "Y", "Z", "F"]) -> str | None:
        result: str | None = None
        try:
            result = line.split(" " + coord)[1].split(" ")[0]
        except Exception:
            pass
        return result
