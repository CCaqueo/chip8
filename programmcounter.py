from NBitRegister import *
from constants import *

class ProgrammCounter(NBitRegister):
    def __init__(self, n, value=PC_INITIAL):
        super().__init__(n, value)