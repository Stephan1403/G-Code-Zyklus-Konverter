import math # needed for eval
from cycle_types.Cycle import Cycle
from cycle_types.CycleScheme import CycleScheme


class CycleTransformer:
    parameter: dict[str, str] = {}
    gcode: list[str] = []
    def scheme_to_gcode(self, cycle: Cycle, scheme: CycleScheme) -> list[str]:
        cycle_scheme = scheme.code
        self._extract_parameters(cycle)
        self._recursive_extraction(cycle_scheme)

    def _extract_parameters(self, cycle: Cycle):
        for key, value in cycle.params.items():
            self.parameter[key] = self._try_convert_to_float(value)
        if cycle.x:
            self.parameter["X"] = cycle.x
        if cycle.y:
            self.parameter["Y"] = cycle.y
        if cycle.z:
            self.parameter["Z"] = cycle.z
        if cycle.speed:
            self.parameter["F"] = cycle.speed

    def _recursive_extraction(self, loop: dict):
        for step in loop:
            if "loop" in step:
                # Loop
                # print("Loop")
                self._loop(step)
            elif "if" in step:
                # print("If")
                self._if(step)
            elif "code" in step:
                # print("Code")
                self._code(step)

    def _code(self, code_dict: dict):
        code = code_dict.get("code", None)
        args = code_dict.get("args", None)
        if not code:
            raise ValueError("Code is required")
        if not isinstance(args, list):
            raise ValueError("Args must be a dictionary")
        values: str = ""
        for value in args:
            values += (" " + value)
        complete = code + values
        complete = complete.strip()
        eval_code = self._eval_code(complete)
        self.gcode.append(eval_code)

    def _if(self, if_dict: dict):
        pass

    def _loop(self, loop_dict: dict):
        pass

    def _eval_code(self, code: str):
        eval_expressions = self._extract_bracketed_words(code)
        if eval_expressions:
            for expression in eval_expressions:
                returned_value = eval(expression, globals(), self.parameter) # pylint: disable=eval-used
                print(expression + " = " + str(returned_value))
                code = code.replace("{" + expression + "}", str(returned_value))
        return code

    def _extract_bracketed_words(self, text: str):
        words = []
        start = None
        for i, char in enumerate(text):
            if char == "{":
                start = i + 1  # Skip the opening brace
            elif char == "}":
                if start is not None:
                    words.append(text[start:i])
                    start = None
        return words

    def _try_convert_to_float(self, x: str) -> float | str:
        try:
            return float(x)
        except ValueError:
            return x
