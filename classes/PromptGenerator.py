import json


class PromptGenerator:
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
