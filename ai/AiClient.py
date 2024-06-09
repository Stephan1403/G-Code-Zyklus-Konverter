from typing import Dict
import json
import google.generativeai as genai


MODEL_VERSION = "gemini-1.5-flash-latest"


class AiClient:
    def __init__(self, api_key):
        self.api_key = api_key
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(MODEL_VERSION)

    def query(self, data: str, prompt_name: str) -> Dict:
        prompt = self._get_ai_prompt_as_str(prompt_name)
        combined_prompt = f"{prompt}: \n{data}"
        output = self.model.generate_content(combined_prompt)
        dict_output = self._get_dict_from_generated_content_response(output)
        return dict_output

    def _get_ai_prompt_as_str(self, prompt_name: str) -> str:
        with open("ai_instructions.json") as f:
            json_file = json.load(f)
            try:
                prompt_str = ""
                prompt_list = json_file["prompts"][prompt_name]
                for prompt in prompt_list:
                    prompt_str += prompt + "\n"
                return prompt_str
            except KeyError:
                raise KeyError(f"No prompt with name {prompt_name}")

    def _get_dict_from_generated_content_response(self, gen_content_res) -> Dict:
        def remove_json_signature(text: str) -> str:
            output = text.strip()
            output = output.removeprefix("```json")
            output = output.removesuffix("```")
            return output

        def transform_text_to_dict(json_text: str) -> Dict:
            try:
                return json.loads(json_text)
            except Exception:
                # raise OuputIsInvalidJsonException(json_text)
                raise Exception("Raise cutsom")  # TODO: raise custom here

        try:
            text_output = gen_content_res.candidates[0].content.parts[0].text
            output = remove_json_signature(text_output)
            output = output.replace("\\n", " ")
            return transform_text_to_dict(output)
        except KeyError:
            # TODO: read content of promptFeedback, and raise custom here
            # raise CouldNotGenerateAiContentException()
            raise Exception("Hello")
