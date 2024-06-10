from __future__ import annotations
from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict
import json
import google.generativeai as genai

MODEL_VERSION = "gemini-1.5-flash-latest"


class ClientType(Enum):
    GEMINI = "GEMINI"


def getAiClient(client_type: ClientType = ClientType.GEMINI, **kwargs) -> AiClient:
    strategies = {
        ClientType.GEMINI: GeminiClient,
    }
    return strategies[client_type](**kwargs)


class AiClient(ABC):
    @abstractmethod
    def dict_query(self, **kwargs) -> Dict:
        pass

    def get_dict_from_str_response(self, content: str) -> Dict:
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
            output = remove_json_signature(content)
            output = output.replace("\\n", " ")
            return transform_text_to_dict(output)
        except KeyError:
            # TODO: read content of promptFeedback, and raise custom here
            # raise CouldNotGenerateAiContentException()
            raise Exception("Hello")


class GeminiClient(AiClient):
    def __init__(self, api_key, model=MODEL_VERSION):
        print("key = ", api_key)
        self.api_key = api_key
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model)

    def dict_query(self, data: str) -> Dict:
        output = self.model.generate_content(data)
        text_output = output.candidates[0].content.parts[0].text
        dict_res = super().get_dict_from_str_response(text_output)
        return dict_res
