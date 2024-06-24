from typing import Dict
from ai.AiClient import AiClient

from classes.CycleInfoExtractor import CycleInfoExtractor
from classes.PromptGenerator import PromptGenerator, PromptPart

from cycle_types.CycleInfo import CycleInfo
from cycle_types.CycleScheme import CycleScheme


class CycleSchemeManager:
    def __init__(self, aiClient: AiClient, pdf_path: str) -> None:
        self.aiClient = aiClient
        self.cycleInfoExtractor = CycleInfoExtractor(pdf_path, aiClient)

    def get_scheme(self, cycleNum: int) -> CycleScheme:
        """Returns a scheme from the storage.
        If none exists it generates a new one
        using the the given ai and given documentation

        Args:
            :param ``cycleNum``: The number of the requested cycle
        """
        if scheme := self._get_scheme_from_storage(cycleNum):
            return scheme
        scheme = self._generate_scheme_from_ai(cycleNum)
        # self._store_scheme(scheme)
        return scheme

    def _get_scheme_from_storage(self, cycleNum: int) -> CycleScheme | None:
        if False:  # TODO: Get scheme from storage
            return CycleScheme(cycleNum)
        return None

    def _generate_scheme_from_ai(self, cycleNum: int) -> CycleScheme:
        cycleInfo: CycleInfo = self.cycleInfoExtractor.extract_cycle_info(
            cycleNum)

        c_prompt_info = PromptPart(
            name="Zyklus Informationen", data=[str(cycleInfo)])

        prompt = PromptGenerator.generate(scheme_instruction, c_prompt_info)

        print("Retrieving cycle generated scheme ... ")
        dict_out = self.aiClient.dict_query(prompt=prompt)
        print("Received generated scheme.")
        return dict_out  # type: ignore

        # TODO: store dict in CycleScheme

    def _store_scheme(self, cycleScheme: CycleScheme) -> None:
        pass
        # Adds scheme to storage


scheme_instruction = PromptPart(
    name="Instruktionen",
    data=["prompts", "generate_scheme"],
    show_tag=False,
    from_file=True,
)
