from typing import Deque, List
from collections import deque
from src.syntax_parser import Code, TuringLogicError


class Machine:
    state: str
    tape: Deque[str]
    pointer: int
    transitions: Code

    def __init__(self):
        self.tape = deque("#")
        self.pointer = 0
        self.state = "_start"

    @classmethod
    def from_code(cls, code: Code) -> Machine:
        machine = cls()
        machine.transitions = code
        return machine

    def clean(self):
        self.__init__()

    def place_input(self, input: List[str]):
        self.pointer = len(self.tape)
        for symbol in input:
            self.tape.append(symbol)

        if self.pointer == len(self.tape):
            self.pointer -= 1

    def execute(self, steps: int = 1000000):
        for _ in range(steps):
            if self.state == "_finish":
                break
            new_state, new_symbol, move = self.transitions.go(
                self.state, self.tape[self.pointer]
            )
            self.state = new_state
            self.tape[self.pointer] = new_symbol

            if move == "L":
                self.pointer -= 1
            elif move == "R":
                self.pointer += 1

            if self.pointer == -1:
                self.tape.appendleft("#")
            if self.pointer == len(self.tape):
                self.tape.append("#")

    def read_result(self) -> List[str]:
        if self.state != "_finish":
            raise TuringLogicError("machine is not in finished state")

        result = []
        ptr = self.pointer
        while ptr < len(self.tape) and self.tape[ptr] != "#":
            result.append(self.tape[ptr])
            ptr += 1
        return result
