class GCode:
    steps: list[str] = []
    def add_step(self, step: str):
        self.steps.append(step)
    def get_gcode(self) -> str:
        value: str = ""
        for step in self.steps:
            if step is not None:
                value += (step + "\n")
        return value
