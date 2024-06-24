from __future__ import annotations
import json
from ai.AiClient import AiClient
from typing import Dict

from openai import OpenAI

import os
from dotenv import load_dotenv
load_dotenv()


class OpenaiClient(AiClient):
    def __init__(self, api_key=os.getenv("OPENAI_API_KEY")):
        self.api_key = api_key
        self.client = OpenAI(api_key=api_key)

    def dict_query(self, prompt: str) -> Dict:
        output = self.client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
            model=os.getenv("OPENAI_MODEL_VERSION")
        )
        response = output.choices[0].message.content
        dict_res = super().get_dict_from_str_response(response)
        print(dict_res)
        return dict_res
