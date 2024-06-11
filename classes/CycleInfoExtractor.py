from typing import List, Dict
from cycle_types.CycleInfo import CycleInfo

from ai.AiClient import AiClient
from classes.PromptGenerator import PromptGenerator

import pymupdf


class CycleInfoExtractor:
    def __init__(self, pdf_path: str, aiClient: AiClient) -> None:
        self.aiClient: AiClient = aiClient
        self.doc = pymupdf.open(pdf_path)

    def extract_cycle_info(self, cycleNum: int) -> CycleInfo:
        pages = self._get_cycle_pages(self.doc, cycleNum)
        cycle_blocks = self._get_cycle_blocks_from_pages(pages)

        cycle_steps = self._get_cycle_steps_from_api(cycle_blocks)
        cycle_params = self._get_cycle_params_from_api(cycle_blocks)

        return CycleInfo(cycleNum, cycle_steps, cycle_params)

    def _get_cycle_pages(self, doc, cycleNum: int) -> List:
        """Returns a list of pages that contain the cycleNum"""

        def is_cycle_page(page, cycleNum) -> bool:
            if page.number < 55:  # ignore hardcoded table of contents
                # TODO: check dynamically if page is cycle page (e.g. not table of contents)
                return False
            return page.search_for(f"Zyklus {cycleNum},")

        # TODO: use only given pages as input
        pages = []
        for page in doc:
            if is_cycle_page(page, cycleNum):
                pages.append(page)
        if len(pages) == 0:
            # raise CycleNotFoundException() TODO: raise custom here
            raise Exception("Raise cycle not found here")
        return pages

    def _get_cycle_blocks_from_pages(self, pages):
        """Returns a list of all blocks for the given pages"""
        cycle_blocks = []
        for page in pages:
            blocks = page.get_text("blocks")
            for block in blocks:
                cycle_blocks.append(block[4])
        return cycle_blocks

    def _get_cycle_steps_from_api(self, blocks: List[str]) -> List[str]:
        """Returns the cycle steps from the API"""
        prompt = PromptGenerator.generate_with_instructions_and_data(
            "get_cycle_steps", data=blocks
        )
        print("Requesting cycle steps from ai ...")
        dict_out: Dict = self.aiClient.dict_query(prompt=prompt)
        print("Retrieved cycle steps")
        return dict_out["steps"]

    def _get_cycle_description_from_api(self, blocks: List[str]) -> List[str]:
        return []

    def _get_cycle_params_from_api(self, blocks: List[str]) -> Dict[str, str]:
        """Returns the cycle params from the API"""
        prompt = PromptGenerator.generate_with_instructions_and_data(
            "get_cycle_params", data=blocks
        )

        print("Requesting cycle params from ai ...")
        dict_out = self.aiClient.dict_query(prompt=prompt)
        print("Retrieved cycle params")
        return dict_out
