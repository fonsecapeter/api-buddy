from yaspin import Spinner

INTERVAL = 100
SINGLE = '='
DOUBLE = '=='
TRIPLE = '==='
LEFT = '['
RIGHT = ']'

spin = Spinner((
    f'  {LEFT}    {RIGHT}',
    f'  {LEFT}{SINGLE}   {RIGHT}',
    f'  {LEFT}{DOUBLE}  {RIGHT}',
    f'  {LEFT}{TRIPLE} {RIGHT}',
    f'  {LEFT} {TRIPLE}{RIGHT}',
    f'  {LEFT}  {DOUBLE}{RIGHT}',
    f'  {LEFT}   {SINGLE}{RIGHT}',
    f'  {LEFT}  {DOUBLE}{RIGHT}',
    f'  {LEFT} {TRIPLE}{RIGHT}',
    f'  {LEFT}{TRIPLE} {RIGHT}',
    f'  {LEFT}{DOUBLE}  {RIGHT}',
    f'  {LEFT}{SINGLE}   {RIGHT}',
), INTERVAL)
