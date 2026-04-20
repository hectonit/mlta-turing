import argparse
from src.syntax_parser import Code
from src.machine import Machine


def main():
    argv_parser = argparse.ArgumentParser(
        description="Runs code from given file on turing machine"
    )
    argv_parser.add_argument("filename")
    args = argv_parser.parse_args()
    with open(args.filename, "r") as file:
        code = Code.from_str(file.read())
    machine = Machine.from_code(code)
    input_str = list(input().split())
    machine.place_input(input_str)
    machine.execute()
    print(*machine.read_result())


if __name__ == "__main__":
    main()
