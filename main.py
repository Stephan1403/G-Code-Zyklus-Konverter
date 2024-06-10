import os
from dotenv import load_dotenv

from classes.GCodeReader import GCodeReader
from classes.CycleSchemeManager import CycleSchemeManager
from classes.CycleTransformer import CycleTransformer
from classes.CycleInfoExtractor import CycleInfoExtractor

from ai.AiClient import AiClient, ClientType, getAiClient

# from classes.UI import UI

# from cycle_types.Cycle import Cycle
# from cycle_types.GCode import GCode
# from cycle_types.CycleCall import CycleCall

if __name__ == "__main__":
    load_dotenv()
    # reader = GCodeReader()
    # schemeManager = CycleSchemeManager()
    # transformer = CycleTransformer()

    aiClient = getAiClient(ClientType.GEMINI, api_key=os.getenv("API_KEY"))
    schemeManager = CycleSchemeManager(aiClient, "./data/cycles.pdf")

    cycle430 = schemeManager.get_scheme(430)
    print(cycle430)
    
    # cycle430 = cycleInfoExtractor.extract_cycle_info(430)
    # print(cycle430.steps)
    # print("\n\n AND: \n", cycle430.params)

    # ui = UI()
    # g_code_path = ui.show_gcode_input()
    # if g_code_path is None:
    #     exit(0)

    """
    cycle430 = cycleInfoExtractor.extract_cycle_info(430)
    print(cycle430.steps)
    print("\n\n AND: \n", cycle430.params)

    ui = UI()
    g_code_path = ui.show_gcode_input()
    if g_code_path is None:
        exit(0)
    """

    """
	last_cycle_num = None


	while code:=reader.get_next_code():
		if code.isinstance(Cycle):
			if not schemeManager.does_scheme_exist(code.number):
				cycleInfo = cycleInfoExtractor.extract_cycle_info(code.number)
				schemeManager.add_scheme(cycleInfo) 
			last_cycle_num = code.number

		elif code.isinstance(CycleCall):
			scheme = schemeManager.get_cycle_scheme(last_cycle_num)
			gcode: GCode = transformer.transform_call_to_gcode(code, scheme)
			# TODO: Store in file
		else:
			# TODO: Store in file
			print(f"Code: {code}")
	"""
