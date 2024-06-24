import math # needed for eval
import copy
from cycle_types.Cycle import Cycle
from cycle_types.CycleScheme import CycleScheme


class CycleTransformer:
    parameter: dict[str, str] = {}
    gcode: list[str] = []
    def scheme_to_gcode(self, cycle: Cycle, scheme: CycleScheme) -> list[str]:
        print(cycle.__dict__)
        cycle_scheme = scheme.code
        self._extract_parameters(cycle)
        self._recursive_extraction(cycle_scheme, self.parameter)
        return self.gcode

    def _extract_parameters(self, cycle: Cycle):
        for key, value in cycle.params.items():
            self.parameter[key] = self._try_convert_to_float(value)
        if cycle.x is not None:
            self.parameter["X"] = cycle.x
        if cycle.y is not None:
            self.parameter["Y"] = cycle.y
        if cycle.z is not None:
            self.parameter["Z"] = cycle.z
        if cycle.speed is not None:
            self.parameter["F"] = cycle.speed

    def _recursive_extraction(self, loop: dict, params: dict):
        for step in loop:
            if "loop" in step:
                # Loop
                self._loop(step)
            elif "if" in step:
                self._if(step, params)
            elif "code" in step:
                self._code(step, params)

    def _code(self, code_dict: dict, params: dict):
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
        eval_code = self._eval_code(complete, params)
        self.gcode.append(eval_code)

    def _if(self, if_dict: dict, params: dict):
        condition = if_dict.get("if", None)
        if not condition:
            raise ValueError("If is required")
        if not isinstance(condition, str):
            raise ValueError("If must be a string")
        pre_eval_expression = self._eval_code(condition, params)
        eval_expression = self._simple_eval(pre_eval_expression, params)
        if eval_expression:
            body = if_dict.get("body", None)
            if not body:
                raise ValueError("Body is required")
            self._recursive_extraction(body, params)

    def _loop(self, loop_dict: dict):
        loop_condition = loop_dict.get("loop", None)
        if not loop_condition:
            raise ValueError("Loop is required")
        if not isinstance(loop_condition, str):
            raise ValueError("Loop must be a string")
        max_loops: int = 1000
        i: int = 1
        params = copy.deepcopy(self.parameter)
        params["i"] = i
        while True:
            first_eval_round = self._eval_code(loop_condition, params)
            if not self._simple_eval(first_eval_round, params):
                break
            body = loop_dict.get("body", None)
            if not body:
                raise ValueError("Body is required")
            self._recursive_extraction(body, params)
            i += 1
            if i > max_loops:
                raise ValueError("Probably an infinite loop. Stopping.")
            params["i"] = i

    def _eval_code(self, code: str, params: dict) -> str:
        eval_expressions = self._extract_bracketed_words(code)
        if eval_expressions:
            for expression in eval_expressions:
                returned_value = self._simple_eval(expression, params)
                code = code.replace("{" + expression + "}", str(returned_value))
        return code

    def _simple_eval(self, expression: str, params: dict) -> str:
        expression_result = None
        try:
            expression_result = eval(expression, globals(), params) # pylint: disable=eval-used
        except Exception as e:
            raise ValueError(f"Invalid expression. Expression: {expression}. Error: {e}") # pylint: disable=raise-missing-from
        return expression_result

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
