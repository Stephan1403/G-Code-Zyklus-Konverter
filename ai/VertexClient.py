from __future__ import annotations
from typing import Dict
from ai.AiClient import AiClient

import vertexai
from vertexai.generative_models import GenerativeModel

import os
from dotenv import load_dotenv
load_dotenv()


class VertexClient(AiClient):
    def __init__(self, project_id=os.getenv("PROJECT_ID"), location=os.getenv("REGION"), model="none"):
        self.project_id = project_id
        self.location = location
        
        vertexai.init(project=project_id, location=location)
        #self.model = TextGenerationModel.from_pretrained("google/text-bison@001")
        self.model = GenerativeModel("gemini-pro")
        #self.model = GenerativeModel("gemini-1.5-flash-001")
        

        

    def dict_query(self, prompt: str) -> Dict:
        res = self.model.generate_content(prompt)
        return res