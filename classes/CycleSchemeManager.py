import json
from typing import Dict
from ai.AiClient import AiClient

from classes.CycleInfoExtractor import CycleInfoExtractor
from classes.PromptGenerator import PromptGenerator

from cycle_types.CycleInfo import CycleInfo
from cycle_types.CycleScheme import CycleScheme


class CycleSchemeManager:
    def __init__(self, aiClient: AiClient, pdf_path: str) -> None:
        self.aiClient = aiClient
        self.cycleInfoExtractor = CycleInfoExtractor(pdf_path, aiClient)

    def get_scheme(self, cycle_number: int) -> CycleScheme:
        """Returns a scheme from the storage.
        If none exists it generates a new one
        using the the given ai and given documentation

        Args:
            :param ``cycleNum``: The number of the requested cycle
        """
        if scheme := self._get_scheme_from_storage(cycle_number):
            return scheme
        scheme = self._generate_scheme_from_ai(cycle_number)
        self._store_scheme(scheme, cycle_number)
        return scheme

    def _get_scheme_from_storage(self, cycle_number: int) -> CycleScheme | None:
        saved_data:dict = None
        with open("./data/cycle_schemes.json", "r", encoding="utf-8") as f:
            saved_data = json.load(f)
        cycle_scheme: CycleScheme | None = saved_data.get(str(cycle_number), None)
        if cycle_scheme is not None:
            print("Use cycle scheme from storage.")
            return CycleScheme(cycle_scheme)
        return None

    def _generate_scheme_from_ai(self, cycle_number: int) -> CycleScheme:
        print(f"Generating scheme for cycle {cycle_number} ...")
        cycleInfo: CycleInfo = self.cycleInfoExtractor.extract_cycle_info(
            cycle_number)

        prompt = PromptGenerator.generate_with_instructions_and_data(
            "generate_scheme", cycleInfo
        )

        print("Retrieving cycle generated scheme ... ")
        scheme_code = self.aiClient.dict_query(prompt=prompt)
        scheme = CycleScheme(scheme_code)
        print("Received generated scheme.")
        return scheme

    def _store_scheme(self, scheme: CycleScheme, cycle_number: int) -> None:
        saved_data:dict = None
        with open("./data/cycle_schemes.json", "r", encoding="utf-8") as f:
            saved_data = json.load(f)
        saved_data[str(cycle_number)] = scheme.code
        with open("./data/cycle_schemes.json", "w", encoding="utf-8") as f:
            f.write(json.dumps(saved_data, indent=2))
