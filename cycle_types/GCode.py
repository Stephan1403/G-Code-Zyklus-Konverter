class GCode:
    steps: list[str]
    def add_step(self, step: str):
        self.steps.append(step)
    def get_gcode(self) -> str:
        return "\n".join(self.steps)