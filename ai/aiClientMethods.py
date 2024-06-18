from __future__ import annotations
from ai.AiClient import AiClient
from ai.VertexClient import VertexClient
from ai.GeminiClient import GeminiClient
from enum import Enum




class ClientType(Enum):
    GEMINI = "GEMINI"
    VERTEX = "VERTEX"


def getAiClient(client_type: ClientType = ClientType.GEMINI, **kwargs) -> AiClient:
    strategies = {
        ClientType.GEMINI: GeminiClient,
        ClientType.VERTEX: VertexClient,
    }
    return strategies[client_type](**kwargs)
