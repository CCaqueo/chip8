from NBitRegister import *
from constants import *

class StackPointer(NBitRegister):
    def __init__(self, n, value=0):
        super().__init__(n, value)
        