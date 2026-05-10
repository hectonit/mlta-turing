from typing import List, Tuple


class TuringSyntaxError(Exception):
    pass


class Instruction:
    old_state: str
    old_symbol: str
    new_state: str
    new_symbol: str
    move: str

    def __init__(self, line: str):
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

        self.old_state, self.old_symbol = lhs_args
        self.new_state, self.new_symbol, self.move = rhs_args

        if self.old_symbol.count("*") > 1:
            raise TuringSyntaxError("only one '*' is allowed in symbols")
        if self.new_symbol.count("*") > 1:
            raise TuringSyntaxError("only one '*' is allowed in symbols")

        if "*" not in self.old_symbol and "*" in self.new_symbol:
            raise TuringSyntaxError("wrong pattern usage, cannot go to any symbol")

    def match(self, state: str, symbol: str) -> Tuple[str, str, str] | None:
        """
        Check if instruction matches state and symbol.

        Parameters:
            state: current state of machine
            symbol: current symbol on tape

        Returns:
            (new_state, new_symbol, move) in case of successfull match
        """
        if state != self.old_state:
            return None

        if "*" in self.old_symbol:
            lhs, rhs = self.old_symbol.split("*")
            if symbol.startswith(lhs) and symbol.endswith(rhs):
                if len(rhs) == 0:
                    star = symbol[len(lhs) :]
                else:
                    star = symbol[len(lhs) : -len(rhs)]
                return (self.new_state, self.new_symbol.replace("*", star), self.move)
        else:
            if symbol == self.old_symbol:
                return (self.new_state, self.new_symbol, self.move)

    def is_pattern(self) -> bool:
        return "*" in self.old_symbol


class Code:
    _instructions: List[Instruction]

    def __init__(self):
        self._instructions = list()

    @classmethod
    def from_str(cls, text: str) -> Code:
        code = cls()
        for line in text.splitlines():
            if not line.strip():
                continue

            code._instructions.append(Instruction(line))
        return code

    def go(self, state: str, symbol: str) -> Tuple[str, str, str] | None:
        """
        Find right instruction and return new state
        """
        next_machine_state = None
        star_used = False
        for instruction in self._instructions:
            transition = instruction.match(state, symbol)
            if transition is None:
                continue

            if next_machine_state is None or star_used:
                next_machine_state = transition
                star_used = instruction.is_pattern()

        return next_machine_state
