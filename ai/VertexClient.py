from __future__ import annotations
from typing import Dict
from ai.AiClient import AiClient

import vertexai
from vertexai.generative_models import GenerativeModel

import os
from dotenv import load_dotenv

load_dotenv()

"""
Implementation of the VertexClient class is not yet complete."""


class VertexClient(AiClient):
    def __init__(
        self,
        project_id=os.getenv("VERTEX_PROJECT_ID"),
        location=os.getenv("VERTEX_REGION"),
        model="none",
    ):
        self.project_id = project_id
        self.location = location

        vertexai.init(project=project_id, location=location)
        self.model = GenerativeModel(os.getenv("VERTEX_MODEL_VERSION"))

    def dict_query(self, prompt: str) -> Dict:
        res = self.model.generate_content(prompt)
        return res
