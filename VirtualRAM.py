class VirtualRAM:
    def __init__(self, size_bytes):
        # Initialize memory filled with zeros
        self.memory = bytearray(size_bytes)

        # Initialize the digit sprites in the interpreter area of the memory
        # 0
        self.memory[0x00] = 0xF0
        self.memory[0x01] = 0x90
        self.memory[0x02] = 0x90
        self.memory[0x03] = 0x90
        self.memory[0x04] = 0xF0
        # 1
        self.memory[0x05] = 0x20
        self.memory[0x06] = 0x60
        self.memory[0x07] = 0x20
        self.memory[0x08] = 0x20
        self.memory[0x09] = 0x70
        # 2
        self.memory[0x0a] = 0xF0
        self.memory[0x0b] = 0x10
        self.memory[0x0c] = 0xF0
        self.memory[0x0d] = 0x80
        self.memory[0x0e] = 0xF0
        # 3
        self.memory[0x0f] = 0xF0
        self.memory[0x10] = 0x10
        self.memory[0x11] = 0xF0
        self.memory[0x12] = 0x10
        self.memory[0x13] = 0xF0
        # 4
        self.memory[0x14] = 0x90
        self.memory[0x15] = 0x90
        self.memory[0x16] = 0xF0
        self.memory[0x17] = 0x10
        self.memory[0x18] = 0x10
        # 5
        self.memory[0x19] = 0x90
        self.memory[0x1a] = 0x90
        self.memory[0x1b] = 0xF0
        self.memory[0x1c] = 0x10
        self.memory[0x1d] = 0x10
        # 6
        self.memory[0x1e] = 0xF0
        self.memory[0x1f] = 0x80
        self.memory[0x20] = 0xF0
        self.memory[0x21] = 0x90
        self.memory[0x22] = 0xF0
        # 7
        self.memory[0x23] = 0xF0
        self.memory[0x24] = 0x10
        self.memory[0x25] = 0x20
        self.memory[0x26] = 0x40
        self.memory[0x27] = 0x40
        # 8
        self.memory[0x28] = 0xF0
        self.memory[0x29] = 0x90
        self.memory[0x2a] = 0xF0
        self.memory[0x2b] = 0x90
        self.memory[0x2c] = 0xF0
        # 9
        self.memory[0x2d] = 0xF0
        self.memory[0x2e] = 0x90
        self.memory[0x2f] = 0xF0
        self.memory[0x30] = 0x10
        self.memory[0x31] = 0xF0
        # A
        self.memory[0x32] = 0xF0
        self.memory[0x33] = 0x90
        self.memory[0x34] = 0xF0
        self.memory[0x35] = 0x90
        self.memory[0x36] = 0x90  
        # B
        self.memory[0x37] = 0xE0
        self.memory[0x38] = 0x90
        self.memory[0x39] = 0xE0
        self.memory[0x3a] = 0x90
        self.memory[0x3b] = 0xE0 
        # C
        self.memory[0x3c] = 0xF0
        self.memory[0x3d] = 0x80
        self.memory[0x3e] = 0x80
        self.memory[0x3f] = 0x80
        self.memory[0x40] = 0xF0 
        # D
        self.memory[0x41] = 0xE0
        self.memory[0x42] = 0x90
        self.memory[0x43] = 0x90
        self.memory[0x44] = 0x90
        self.memory[0x45] = 0xE0 
        # E
        self.memory[0x46] = 0xF0
        self.memory[0x47] = 0x80
        self.memory[0x48] = 0xF0
        self.memory[0x49] = 0x80
        self.memory[0x4a] = 0xF0
        # F
        self.memory[0x4b] = 0xF0
        self.memory[0x4c] = 0x80
        self.memory[0x4d] = 0xF0
        self.memory[0x4e] = 0x80
        self.memory[0x4f] = 0x80

        self.size = size_bytes        

    def read(self, address):
        self._validate_address(address)
        return self.memory[address]

    def write(self, address, value):
        self._validate_address(address)
        if not (0 <= value <= 0xFF):
            raise ValueError("Value must be a single byte (512-255)")
        self.memory[address] = value

    def _validate_address(self, address):
        if not (0 <= address < self.size):
            raise IndexError("Segmentation fault: Address out of bounds")

# Example Usage:
#ram = VirtualRAM(size_bytes=1024) # 1 KB of RAM
#ram.write(0x00A, 42)              # Write 42 to hex address 0x0A
#print(ram.read(0x00A))            # Outputs: 42
