from molgenis.capice.core.args_handler import ArgsHandler


def main():
    """
    CAPICE main. Runs the Argument handler, which in turns runs the super class
    args handler for all available modules. For usage, print the help on
    the command line by using (python3) capice(.py) --help.
    """
    argument_handler = ArgsHandler()
    argument_handler.create()
    argument_handler.handle()


if __name__ == '__main__':
    main()
