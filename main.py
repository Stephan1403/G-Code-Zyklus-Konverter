from classes.GCodeReader import GCodeReader
from classes.CycleSchemeManager import CycleSchemeManager
from classes.CycleTransformer import CycleTransformer
from classes.CycleInfoExtractor import CycleInfoExtractor

from .types.Cycle import Cycle
from .types.GCode import GCode
from .types.CycleCall import CycleCall

if __name__ == "__main__":
	
	reader = GCodeReader()
	schemeManager = CycleSchemeManager()
	transformer = CycleTransformer()
	cycleInfoExtractor = CycleInfoExtractor("pdf_path")
	
	last_cycle_num = None
	
	while code:=reader.get_next_code():
		if code.isinstance(Cycle):
			if not schemeManager.does_scheme_exist(code.number):
				cycleInfo = cycleInfoExtractor.extract_cycle_info(code)
				schemeManager.add_scheme(cycleInfo)
			last_cycle_num = code.number
			
		elif code.isinstance(CycleCall):
			scheme = schemeManager.get_cycle_scheme(last_cycle_num)
			gcode: GCode = transformer.transform_call_to_gcode(code, scheme)
			# TODO: Store in file
		else:
			# TODO: Store in file
			print(f"Code: {code}")
	