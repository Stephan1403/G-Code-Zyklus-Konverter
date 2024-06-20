from typing import List
import json


class PromptGenerator2:
    @classmethod
    def generate_with_instructions_and_data(cls, instruction_name: str, data):
        instructions = cls._get_ai_instructions_from_name(instruction_name)
        data = str(data)
        return f"{instructions}: \n {data}"

    @classmethod
    def _get_ai_instructions_from_name(cls, name: str):
        with open("config/ai_instructions.json") as f:
            json_file = json.load(f)
            try:
                prompt_str = ""
                prompt_list = json_file["prompts"][name]
                for prompt in prompt_list:
                    prompt_str += prompt + "\n"
                return prompt_str
            except KeyError:
                raise KeyError(f"No prompt with name {name}")


class PromptPart:
    """One Part of the Prompt"""

    def __init__(self, name: str, content_list: List, show_tag: bool = True) -> None:
        self.name = name
        self.show_tag = show_tag
        self.content_list = content_list
        self.value: str = ""

    def get(self) -> str:
        self._generate()
        return self.value

    def _generate(self) -> None:
        self._add_content_from_list()
        if self.show_tag:
            self._append_tag()

    def _add_content_from_list(self) -> None:
        content_text: str = ""
        for el in self.content_list:
            if self.show_tag:
                content_text += "  "
            content_text += el + "\n"
        # Set value and remove one \n at the end
        self.value += content_text.removesuffix("\n")

    def _append_tag(self):
        open_tag = f"<{self.name.upper()}>\n"
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
        if isinstance(prompt_parts, PromptPart):
            return prompt + prompt_parts.get() + "\n\n"

        for p in prompt_parts:
            prompt = prompt + p.get() + "\n\n"
        return prompt

    @classmethod
    def get_default_system_instruction(cls) -> PromptPart:
        return PromptPart(
            "System instructions", ["Be something fun", "lol"], show_tag=False
        )

    @classmethod
    def get_default_return_format(cls) -> PromptPart:
        return PromptPart("Return Format", ["Do json", "moin"])


if __name__ == "__main__":
    i = PromptPart("Instruction", ["This should not ", "have any tag", "lul"])
    p = PromptPart("Example", ["First line", "Second line", "Third line"])

    prom = PromptGenerator.generate(i, p)
    prom2 = PromptGenerator.generate_default_for_translation(i, i, i, i)
    print(prom2)
