class Stack():
    def __init__(self, bits, size):
        self.size = size
        self.memory = [0] * size
        self.bits = (1 << bits-1) | 0xFFFF

    def read(self, address):
        self._validate_address(address)
        return self.memory[address]

    def write(self, address, value):
        self._validate_address(address)
        if not (0 <= value <= 1 << self.bits):
            raise ValueError("Value must be a 2 byte value (0-65.535)")
        self.memory[address] = value
        
    def _validate_address(self, address):
        if not (0 <= address <= self.size):
            raise IndexError("Segmentation fault: Address out of bounds")