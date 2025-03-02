import re
from typing import List, Dict
from cycle_types.CycleInfo import CycleInfo

from ai.AiClient import AiClient
from classes.PromptGenerator import (
    PromptGenerator,
    PromptPart,
)

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

        return CycleInfo(
            cycleNum, cycle_steps["steps"], cycle_params, cycle_steps["description"]
        )

    def _get_cycle_pages(self, doc, cycleNum: int) -> List:
        """Returns a list of pages that contain the cycleNum"""

        def is_cycle_page(page, cycleNum) -> bool:
            if page.number < 55:  # ignore hardcoded table of contents
                # TODO: check dynamically if page is cycle page (e.g. not table of contents)
                return False
            t = page.get_text()
            pattern = rf"Zyklus {cycleNum}\W+"
            if re.search(pattern, t):
                return True
            return False

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

    def _get_cycle_steps_from_api(self, blocks: List[str]) -> Dict:
        """Returns the cycle steps from the API"""
        # Generate prompt
        block_data = PromptPart(name="Daten", data=blocks)
        prompt = PromptGenerator.generate(
            c_steps_instruction, c_steps_format, block_data
        )

        print("Requesting cycle steps from ai ...")
        dict_out: Dict = self.aiClient.dict_query(prompt=prompt)
        print("Retrieved cycle steps")
        return dict_out

    def _get_cycle_params_from_api(self, blocks: List[str]) -> Dict[str, str]:
        """Returns the cycle params from the API"""
        # Generate prompt
        block_data = PromptPart(name="Daten", data=blocks)
        prompt = PromptGenerator.generate(
            c_params_instructions, c_params_format, block_data
        )

        print("Requesting cycle params from ai ...")
        dict_out = self.aiClient.dict_query(prompt=prompt)
        print("Retrieved cycle params")
        return dict_out


""" Prompt definitions """
# Cycle steps
c_steps_instruction = PromptPart(
    name="Cycle steps instruction",
    data=["prompts", "get_cycle_steps", "instructions"],
    show_tag=False,
    from_file=True,
)
c_steps_format = PromptPart(
    name="Erwartete Rückgabe",
    data=["prompts", "get_cycle_steps", "format"],
    show_tag=True,
    from_file=True,
)

# Cycle params
c_params_instructions = PromptPart(
    name="Erwartete Rückgabe",
    data=["prompts", "get_cycle_params", "instructions"],
    show_tag=False,
    from_file=True,
)
c_params_format = PromptPart(
    name="Erwartete Rückgabe",
    data=["prompts", "get_cycle_params", "format"],
    show_tag=True,
    from_file=True,
)
