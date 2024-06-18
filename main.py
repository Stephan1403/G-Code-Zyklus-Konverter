import os
from dotenv import load_dotenv

from classes.GCodeReader import GCodeReader
from classes.CycleSchemeManager import CycleSchemeManager
from classes.CycleTransformer import CycleTransformer

from ai.aiClientMethods import ClientType, getAiClient
from cycle_types.Cycle import Cycle
from cycle_types.GCode import GCode

ai_client = getAiClient(ClientType.VERTEX)
manager = CycleSchemeManager(ai_client, "./data/cycles.pdf")
transformer = CycleTransformer()


def main():
    finished_gcode = GCode()
    gcode_path = "./test_gcode.txt"
    execution_loop(gcode_path, finished_gcode)
    save_gcode(finished_gcode)


def transform(cycle: Cycle) -> str | list[str]:
    scheme = manager.get_scheme(cycle.number)
    return transformer.scheme_to_gcode(cycle, scheme)


def add_to_finished_gcode(lines: str | list[str], finished_gcode: GCode):
    if isinstance(lines, list):
        for line in lines:
            finished_gcode.add_step(line)
        return
    finished_gcode.add_step(lines)


def save_gcode(finished_gcode: GCode):
    with open("./output.gcode", "w", encoding="utf-8") as f:
        f.write(finished_gcode.get_gcode())


def execution_loop(gcode_path: str, finished_gcode: GCode):
    reader = GCodeReader(gcode_path)
    while cycle := reader.get_next_code():
        if isinstance(cycle, Cycle):
            add_to_finished_gcode(transform(cycle), finished_gcode)
        else:
            add_to_finished_gcode(cycle, finished_gcode)
    print("Transformation Finished")


if __name__ == "__main__":

    content = (
        "Return json only. I want the key to be test. And the value Hello World"
    )

    res = ai_client.dict_query(content)
    print(res)
