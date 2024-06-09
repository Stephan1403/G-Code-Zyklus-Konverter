from classes.GCodeReader import GCodeReader
from classes.CycleSchemeManager import CycleSchemeManager
from classes.CycleTransformer import CycleTransformer
from classes.CycleInfoExtractor import CycleInfoExtractor
from classes.UI import UI

# from cycle_types.Cycle import Cycle
# from cycle_types.GCode import GCode
# from cycle_types.CycleCall import CycleCall

if __name__ == "__main__":
    # reader = GCodeReader()
    # schemeManager = CycleSchemeManager()
    # transformer = CycleTransformer()
    # cycleInfoExtractor = CycleInfoExtractor("./data/cycles.pdf")

    # cycleInfoExtractor.extract_cycle_info(430)

    ui = UI()
    g_code_path = ui.show_gcode_input()
    if g_code_path is None:
        exit(0)
    
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
