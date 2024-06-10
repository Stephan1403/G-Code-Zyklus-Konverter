from typing import List, Dict


class CycleInfo:
    def __init__(self, number: int, steps: List, params: Dict, description=""):
        self.number = number
        self.description = description
        self.steps = steps
        self.params = params

    def __str__(self) -> str:
        des = ""
        if len(des) > 0:
            des = f"Zyklus Beschreibung: {self.description}\n"

        return (
            des
            + f"""Zyklus Ablauf:
        {"\n-".join(self.steps)}

        mit folgenden Zyklus Parametern:
        {"\n-".join(self.params)}

        """
        )

    def __repr__(self) -> str:
        return str(self)
