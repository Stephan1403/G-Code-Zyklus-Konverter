from Errors.PromptErrors import InstructionNotFoundError
from typing import List, Dict
import json


class PromptPart:
    """One Part of the Prompt"""

    # TODO: data should be checked for type pathlike and not string

    def __init__(
        self,
        name: str,
        data: List[str],
        show_tag: bool = True,
        from_file: bool = False,
        path="config/ai_instructions.json",
    ) -> None:
        """Create a new PromptPart

        Args:
            :param ``name``: Name of the part
            :param ``data``: Data in form of a list or the path in the json file to the data
            :param ``show_tag``: Whether to show the tag or not
            :param ``path``: Path to the json file with the instructions
        """
        self.name = name
        self.show_tag = show_tag
        self.data = data
        self.from_file = from_file
        self.path = path
        self.value: str = ""

    def get(self) -> str:
        self._generate()
        return self.value

    def _generate(self) -> None:
        if self.from_file:
            c_list = self._get_content_from_file(self.data)
        else:
            c_list = self.data
        self._add_content_from_list(c_list)
        if self.show_tag:
            self._append_tag()

    def _add_content_from_list(self, content_list: List[str], show_tag=None) -> None:
        if show_tag is None:
            show_tag = self.show_tag

        content_text: str = ""
        for el in content_list:
            if show_tag:
                content_text += "  "
            content_text += el + "\n"
        # Set value and remove one \n at the end
        self.value += content_text.removesuffix("\n")

    def _get_content_from_file(self, path: List[str]) -> List[str]:
        """Retrieve data from the json file.

        Args:
            :param ``path``: is a list of keys to the destination in the json"""
        with open(self.path) as f:
            data = json.load(f)
            for key in path:
                try:
                    data = data[key]
                except KeyError:
                    raise InstructionNotFoundError(key)
            return data if data is not None else []

    def _append_tag(self):
        open_tag = f"<{self.name.upper()}>B\nA"
        close_tag = f"\n</{self.name.upper()}>"
        self.value = open_tag + self.value + close_tag


class PromptGenerator:
    @classmethod
    def generate(cls, *prompt_parts: PromptPart) -> str:
        return cls.add_prompt_parts("", *prompt_parts).removesuffix("\n\n")

    @classmethod
    def generate_default_for_translation(
        cls,
        examples: PromptPart,
        description: PromptPart,
        steps: PromptPart,
        params: PromptPart,
    ) -> str:
        """Generate a default prompt for translation using set default params"""
        prompt = ""
        prompt = cls.add_prompt_parts(
            prompt,
            cls.get_default_system_instruction(),
            cls.get_default_return_format(),
            examples,
            description,
            steps,
            params,
        )

        return prompt.removesuffix("\n\n")

    @classmethod
    def add_prompt_parts(cls, prompt: str, *prompt_parts: PromptPart) -> str:
        for p in prompt_parts:
            prompt = prompt + p.get() + "\n\n"
        return prompt

    # Default prompts
    @classmethod
    def get_default_system_instruction(cls) -> PromptPart:
        return PromptPart(
            "System instructions",
            ["general_instructions"],
            show_tag=False,
            from_file=True,
        )

    @classmethod
    def get_default_return_format(cls) -> PromptPart:
        return PromptPart(
            "System instructions",
            ["prompts", "generate_scheme"],
            show_tag=False,
            from_file=True,
        )
