from ai.AiClient import AiClient

from classes.CycleInfoExtractor import CycleInfoExtractor

from cycle_types.CycleInfo import CycleInfo
from cycle_types.CycleScheme import CycleScheme


class CycleSchemeManager:
    def __init__(
        self, aiClient: AiClient, cycleInfoExtractor: CycleInfoExtractor
    ) -> None:
        self.aiClient = aiClient
        self.cylceInfoExtractor = ciExtractor

    def does_scheme_exist(self, number: int) -> bool:
        pass
        return False
        # Checks if scheme in storage

    def add_scheme(self, cycleInfo: CycleInfo) -> None:
        pass
        # Adds scheme to storage

    def generate_scheme_from_ai(self, cycleInfo: CycleInfo) -> CycleScheme:
        pass

    def get_cycle_scheme(self, cycleNum: int) -> CycleScheme:
        # Get scheme from storage throw error if not found

        pass
