from __future__ import annotations
from ai.AiClient import AiClient
from typing import Dict

import google.generativeai as genai

import os
from dotenv import load_dotenv
load_dotenv()


class GeminiClient(AiClient):
    def __init__(self, api_key=os.getenv("API_KEY"), model=os.getenv("GEMINI_MODEL_VERSION")):
        self.api_key = api_key
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model)

    def dict_query(self, prompt: str) -> Dict:
        output = self.model.generate_content(prompt)
        text_output = output.candidates[0].content.parts[0].text
        dict_res = super().get_dict_from_str_response(text_output)
        return dict_res
