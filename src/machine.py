from typing import Deque, List
from collections import deque
from src.syntax_parser import Code


class TuringDumpFormatError(Exception):
    pass


class TuringLogicError(Exception):
    pass


class Machine:
    """
    Represent Turing machine.

    Attributes:
        state: current state of machine
    """

    _state: str
    _tape: Deque[str]
    _pointer: int
    _transitions: Code

    def __init__(self):
        self._tape = deque("#")
        self._pointer = 0
        self._state = "_start"

    @property
    def state(self):
        return self._state

    @classmethod
    def from_code(cls, code: Code) -> Machine:
        """
        Build machine from user code.
        """
        machine = cls()
        machine._transitions = code
        return machine

    def apply_dump(self, dump: str):
        """
        Change tape, pointer and state according to dump data
        """
        try:
            lhs, rhs = dump.split(";;;")
            self._tape = deque(lhs.split(";"))
            st, ptr = rhs.split(";")
            self._state = st
            self._pointer = int(ptr)
        except:
            raise TuringDumpFormatError(
                "wrong format of dump, use only program-generated dumps"
            )

    def clean(self):
        """
        Clean tape, reset pointer, go to '_start' state.
        """
        self.__init__()

    def place_input(self, input: List[str]):
        """
        Print input on tape starting from current pointer position.
        """
        self._pointer = len(self._tape)
        for symbol in input:
            self._tape.append(symbol)

        if self._pointer == len(self._tape):
            self._pointer -= 1

    def execute(self, steps: int = 1000000):
        """
        Simulate execution for n steps.
        """
        for _ in range(steps):
            if self._state == "_finish":
                break
            result = self._transitions.go(self._state, self._tape[self._pointer])
            if result is None:
                break
            new_state, new_symbol, move = result
            self._state = new_state
            self._tape[self._pointer] = new_symbol

            if move == "L":
                self._pointer -= 1
            elif move == "R":
                self._pointer += 1

            if self._pointer == -1:
                self._tape.appendleft("#")
                self._pointer = 0
            if self._pointer == len(self._tape):
                self._tape.append("#")

    def read_result(self) -> List[str]:
        """
        Read data that stored from current pointer position to first '#'.
        """
        if self._state != "_finish":
            raise TuringLogicError("machine is not in finished state")

        result = []
        ptr = self._pointer
        while ptr < len(self._tape) and self._tape[ptr] != "#":
            result.append(self._tape[ptr])
            ptr += 1
        return result

    def get_symbol(self, index: int) -> str:
        """
        get symbol on relative position from pointer
        """
        if self._pointer + index >= len(self._tape) or self._pointer + index < 0:
            return "#"
        return self._tape[self._pointer + index]

    def dump(self) -> str:
        """
        make string which contains dump of machine state
        """
        result = ""
        for symbol in self._tape:
            result += symbol
            result += ";"
        result += ";;"
        result += self.state
        result += ";"
        result += str(self._pointer)
        return result
