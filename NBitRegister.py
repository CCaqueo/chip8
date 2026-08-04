class NBitRegister:
    def __init__(self, n, value=0):
        self.n = n
        
        # Generates a mask with 'n' ones (e.g., n=8 creates 0xFF)
        self._mask = (1 << n) - 1 
        
        # Applies the mask to keep the value within the n-bit range
        self._value = value & self._mask

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        # Keeps value within 8 bits (e.g., 256 becomes 0, -1 becomes 255)
        self._value = new_value & self._mask

    def __str__(self):
        return f"Dec: {self._value} | Hex: 0x{self._value:02X} | Bin: {self._value:08b}"

