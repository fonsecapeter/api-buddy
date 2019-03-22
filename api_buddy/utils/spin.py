from colorama import Fore, Style
from typing import List
from yaspin import Spinner

INTERVAL = 80
OPEN = f'{Style.BRIGHT}'
CLOSE = f'{Style.RESET_ALL}'
COLORS = (Fore.GREEN, Fore.BLUE, Fore.MAGENTA, Fore.RED, Fore.YELLOW)

frames: List[str] = []
for color in COLORS:
    frames += (
        f'{OPEN}{color}=>  {CLOSE}',
        f'{OPEN}{color}==> {CLOSE}',
        f'{OPEN}{color}===>{CLOSE}',
        f'{OPEN}{color} ==={CLOSE}',
        f'{OPEN}{color}  =={CLOSE}',
        f'{OPEN}{color}   ={CLOSE}',
        f'{OPEN}{color}   <{CLOSE}',
        f'{OPEN}{color}  <={CLOSE}',
        f'{OPEN}{color} <=={CLOSE}',
        f'{OPEN}{color}<==={CLOSE}',
        f'{OPEN}{color}=== {CLOSE}',
        f'{OPEN}{color}==  {CLOSE}',
        f'{OPEN}{color}=   {CLOSE}',
        f'{OPEN}{color}    {CLOSE}',
        f'{OPEN}{color}>   {CLOSE}',
    )

spin = Spinner(frames, INTERVAL)
