from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Dict
import json


class AiClient(ABC):
    @abstractmethod
    def dict_query(self, prompt: str, **kwargs) -> Dict:
        raise NotImplementedError()

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
