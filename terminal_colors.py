class TerminalColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_green(line):
    print(TerminalColors.OKGREEN + line + TerminalColors.ENDC)


def print_red(line):
    print(TerminalColors.FAIL + line + TerminalColors.ENDC)


def print_yellow(line):
    print(TerminalColors.WARNING + line + TerminalColors.ENDC)

