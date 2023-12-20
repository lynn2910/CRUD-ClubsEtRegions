RESET = '\033[0m'
BLACK = '\033[30m'
RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
BLUE = '\033[34m'
MAGENTA = '\033[35m'
CYAN = '\033[36m'
WHITE = '\033[37m'


def info(message):
    print(f'{BLUE}[INFO] {message}{RESET}')


def warn(message):
    print(f'{YELLOW}[WARN] {message}{RESET}')


def error(message):
    print(f'{RED}[ERROR] {message}{RESET}')


def trace(message):
    print(f'{BLUE}[TRACE] {message}{RESET}')
