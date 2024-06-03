from ..types.CycleInfo import CycleInfo
from ..types.CycleScheme import CycleScheme

class CycleSchemeManager:

    def __init__(self) -> None:
        self.aiClient = None
    
    def does_scheme_exist(self, number: int) -> bool:
        pass
        # Checks if scheme in storage
    
    def add_scheme(self, cycleInfo: CycleInfo) -> None:
        pass
        # Adds scheme to storage
    
    def get_cycle_scheme(self, number: int) -> CycleScheme:
        # Get scheme from storage throw error if not found
        pass
    
    