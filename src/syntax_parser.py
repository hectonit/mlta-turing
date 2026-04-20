from typing import Dict, Tuple


class TuringSyntaxError(Exception):
    pass


class TuringLogicError(Exception):
    pass


class Code:
    instructions: Dict[Tuple[str, str], Tuple[str, str, str]]

    def __init__(self):
        self.instructions = dict()

    @classmethod
    def from_str(cls, text: str) -> Code:
        code = cls()
        for line in text.splitlines():
            if not line.strip():
                continue

            sides = line.split(" -> ")
            if len(sides) != 2:
                raise TuringSyntaxError("expected `lhs -> rhs` format")
            lhs, rhs = sides

            lhs_args = lhs.split(",")
            if len(lhs_args) != 2:
                raise TuringSyntaxError(
                    "expected following left side format: `<old_state>,<old_symbol>`"
                )

            rhs_args = rhs.split(",")
            if len(rhs_args) != 3:
                raise TuringSyntaxError(
                    "expected following right side format: `<new_state>,<new_symbol>,<move>`"
                )

            old_state, old_symbol = lhs_args
            new_state, new_symbol, move = rhs_args
            code.instructions[(old_state, old_symbol)] = (new_state, new_symbol, move)
        return code

    def go(self, state, symbol) -> Tuple[str, str, str] | None:
        data = self.instructions.get((state, symbol))
        if data is None:
            raise TuringLogicError(f"no valid transition from ({state}, {symbol})")
        return data
