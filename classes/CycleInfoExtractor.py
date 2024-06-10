from typing import List, Dict
from cycle_types.CycleInfo import CycleInfo
from ai.AiClient import AiClient

import json
import pymupdf


class CycleInfoExtractor:
    def __init__(self, pdf_path: str, aiClient: AiClient) -> None:
        # TODO: create aiClient here or pass instance ???
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
        prompt = self._generate_prompt("get_cycle_steps", data=blocks)
        dict_out: Dict = self.aiClient.dict_query(prompt=prompt)
        return dict_out["steps"]

    def _get_cycle_description_from_api(self, blocks: List[str]) -> List[str]:
        pass

    def _get_cycle_params_from_api(self, blocks: List[str]) -> Dict[str, str]:
        """Returns the cycle params from the API"""
        prompt = self._generate_prompt("get_cycle_params", data=blocks)
        dict_out = self.aiClient.dict_query(prompt=prompt)
        return dict_out

    def _generate_prompt(self, instruction_name: str, data) -> str:
        def get_ai_instructions(instruction_name: str) -> str:
            with open("config/ai_instructions.json") as f:
                json_file = json.load(f)
                try:
                    prompt_str = ""
                    prompt_list = json_file["prompts"][instruction_name]
                    for prompt in prompt_list:
                        prompt_str += prompt + "\n"
                    return prompt_str
                except KeyError:
                    raise KeyError(f"No prompt with name {instruction_name}")

        instruction = get_ai_instructions(instruction_name)
        data = str(data)
        return f"{instruction}: \n {data}"
