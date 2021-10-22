from src.main.python.core.args_handler import ArgsHandler


def main():
    argument_handler = ArgsHandler()
    argument_handler.create()
    argument_handler.handle()


if __name__ == '__main__':
    main()
