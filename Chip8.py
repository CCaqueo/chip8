import pygame
import random
from VirtualRAM import *
from constants import *
from NBitRegister import *
from stack import *
from programmcounter import *

class Chip8():
    def __init__(self):
        self.ram = VirtualRAM(RAMSIZE)
        self.stack = Stack(STACKBITS, STACKSIZE)

        # Definicion de los registros V0 a VF
        self.V0 = NBitRegister(8)
        self.V1 = NBitRegister(8)
        self.V2 = NBitRegister(8)
        self.V3 = NBitRegister(8)
        self.V4 = NBitRegister(8)
        self.V5 = NBitRegister(8)
        self.V6 = NBitRegister(8)
        self.V7 = NBitRegister(8)
        self.V8 = NBitRegister(8)
        self.V9 = NBitRegister(8)
        self.Va = NBitRegister(8)
        self.Vb = NBitRegister(8)
        self.Vc = NBitRegister(8)
        self.Vd = NBitRegister(8)
        self.Ve = NBitRegister(8)
        self.Vf = NBitRegister(8)
        self.Vi = NBitRegister(16)

        self.V: dict[int, NBitRegister] = {0: self.V0, 1: self.V1, 2: self.V2, 3: self.V3, 4: self.V4, 5: self.V5, 
                                      6: self.V6, 7: self.V7, 8: self.V8, 9: self.V9, 10: self.Va, 11: self.Vb, 
                                      12: self.Vc, 13: self.Vd, 14: self.Ve, 15: self.Vf}

        # Definicion del Programm Counter y Stack Pointer. La clase ProgrammCounter inicializa el PC en 0x200.
        self.PC = ProgrammCounter(16)
        self.SP = NBitRegister(8)

        self.DT = NBitRegister(8)
        self.ST = NBitRegister(8)


        self.keys: dict[int, bool] = {0: False, 1: False, 2: False, 3: False, 
                                        4: False, 5: False, 6: False, 7: False,
                                        8: False, 9: False, 10: False, 11: False, 
                                        12: False, 13: False, 14: False, 15: False}

        self.digits: dict[int, int] = {0: 0x00, 1: 0x05, 2: 0x0a, 3: 0x0f, 4: 0x14, 
                                       5: 0x19, 6: 0x1e, 7: 0x23, 8: 0x28, 9: 0x2d, 
                                       0xA: 0x32, 0xB: 0x37, 0xC: 0x3c, 0xD: 0x41, 
                                       0xE: 0x46, 0xF: 0x4b}

        # Definicion de la pantalla como una matriz
        self.matriz_video = [0] * (ANCHO_CHIP8 * ALTO_CHIP8)

    def ciclo_cpu(self):
        #print(f"SP outside CALL: {self.SP.value:2x}")
        primer_byte = self.ram.read(self.PC.value)
        segundo_byte = self.ram.read(self.PC.value + 1)

        self.PC.value += 2

        if self.DT.value > 0:
            self.DT.value -= 1
        if self.ST.value > 0:
            self.ST.value -= 1

        opcode = (primer_byte << 8) | segundo_byte
        
        instruction = (opcode & 0xF000) >> 12
        match instruction:
            case 0:
                if opcode == 0x00E0:
                    self.CLS_00E0()

                elif opcode == 0x00EE:
                    self.RET_00EE()

            case 1:
                self.JP_1nnn(opcode & 0x0FFF)

            case 2:
                self.CALL_2nnn(opcode & 0x0FFF)

            case 3:
                self.SE_3xkk(self.V[(opcode & 0x0F00) >> 8], opcode & 0x00FF)

            case 4:
                self.SNE_4xkk(self.V[(opcode & 0x0F00) >> 8], opcode & 0x00FF)

            case 5:
                self.SE_5xy0(self.V[(opcode & 0x0F00) >> 8], self.V[(opcode & 0x00F0) >> 4])

            case 6:
                self.LD_6xkk(self.V[(opcode & 0x0F00) >> 8], opcode & 0x00FF)

            case 7:
                self.ADD_7xkk(self.V[(opcode & 0x0F00) >> 8], opcode & 0x00FF)

            case 8:
                VX = self.V[(opcode & 0x0F00) >> 8]
                VY = self.V[(opcode & 0x00F0) >> 4]

                match opcode & 0x000F:
                    case 0:
                        self.LD_8xy0(VX, VY)
                    case 1:
                        self.OR_8xy1(VX, VY)
                    case 2:
                        self.AND_8xy2(VX, VY)
                    case 3:
                        self.XOR_8xy3(VX, VY)
                    case 4:
                        self.ADD_8xy4(VX, VY)
                    case 5:
                        self.SUB_8xy5(VX, VY)
                    case 6:
                        self.SHR_8xy6(VX)
                    case 7:
                        self.SUBN_8xy7(VX, VY)
                    case 0xE:
                        self.SHL_8xyE(VX)
                    #case _:
                    #    raise ValueError("Not a valid instruction")

            case 9:
                self.SNE_9xy0(self.V[(opcode & 0x0F00) >> 8], self.V[(opcode & 0x00F0) >> 4])

            case 0xA:
                self.LD_Annn(opcode & 0x0FFF)
            case 0xB:
                self.JP_Bnnn(opcode & 0x0FFF)

            case 0xC:
                self.RND_Cxkk(self.V[(opcode & 0x0F00) >> 8], opcode & 0x00FF)

            case 0xD:
                self.DRW_Dxyn(self.V[(opcode & 0x0F00) >> 8], self.V[(opcode & 0x00F0) >> 4], opcode & 0x000F)

            case 0xE:
                VX = self.V[(opcode & 0x0F00) >> 8]

                if opcode & 0x00FF == 0x9E:
                    self.SKP_Ex9E(VX)
                elif opcode & 0x00FF == 0xA1:
                    self.SKNP_ExA1(VX)

            case 0xF:
                VX = self.V[(opcode & 0x0F00) >> 8]
                byte2 = opcode & 0x00FF

                match byte2:
                    case 0x07:
                        self.LD_Fx07(VX)
                    case 0x0A:
                        self.LD_Fx0A(VX)
                    case 0x15:
                        self.LD_Fx15(VX)
                    case 0x18:
                        self.LD_Fx18(VX)
                    case 0x1E:
                        self.ADD_Fx1E(VX)
                    case 0x29:
                        self.LD_Fx29(VX)
                    case 0x33:
                        self.LD_Fx33(VX)
                    case 0x55:
                        self.LD_Fx55(VX)
                    case 0x65:
                        self.LD_Fx65(VX)
                    #case _:
                    #    raise ValueError("Not a valid instruction")
            #case _:
            #    raise ValueError("Not a valid instruction")
        

    def load_rom(self, rom):
        for i in range(len(rom)):
            #print(f"Byte {i}: {rom[i]:2x} | Address: {0x200+i:2x}")
            self.ram.write(0x200 + i, rom[i])

    def renderizar_pantalla(self, ventana) -> None:
        # Limpiar la pantalla física con color negro (RGB: 0, 0, 0)
        ventana.fill((0, 0, 0))

        # Recorrer nuestra matriz lógica de 64x32
        for y in range(ALTO_CHIP8):
            for x in range(ANCHO_CHIP8):

                # Calcular el índice en la lista plana
                indice = y * ANCHO_CHIP8 + x

                # Si el píxel en nuestra matriz interna es 1 (encendido)
                if self.matriz_video[indice] == 1:
                    # Dibujamos un rectángulo blanco en la ventana física
                    # pygame.Rect(x_real, y_real, ancho_real, alto_real)
                    rectangulo = pygame.Rect(x * ESCALA, y * ESCALA, ESCALA, ESCALA)
                    pygame.draw.rect(ventana, (255, 255, 255), rectangulo)

        # Le decimos a Pygame que actualice el monitor con lo que dibujamos
        pygame.display.flip()

    # Clear the display.
    def CLS_00E0(self) -> None:
        self.matriz_video = [0] * (ANCHO_CHIP8 * ALTO_CHIP8)

    # The interpreter sets the program counter to the address at the top of the stack, then subtracts 1 from the stack pointer.
    def RET_00EE(self) -> None:
        self.PC.value = self.stack.read(self.SP.value)
        self.SP.value -= 0x01

    # The interpreter sets the program counter to nnn.
    def JP_1nnn(self, addr: int) -> None:
        self.PC.value = addr

    # The interpreter increments the stack pointer, then puts the current PC on the top of the stack. The PC is then set to nnn.
    def CALL_2nnn(self, addr: int) -> None:
        print(f"SP: {self.SP.value:2x}")
        print(f"PC: {self.PC.value:2x}")
        self.stack.write(self.SP.value, self.PC.value)
        self.SP.value += 0x1
        self.PC.value = addr

    # The interpreter compares register Vx to kk, and if they are equal, increments the program counter by 2.
    def SE_3xkk(self, VX: NBitRegister, kk: int) -> None:
        if VX.value == kk:
            self.PC.value += 0x02

    # The interpreter compares register Vx to kk, and if they are not equal, increments the program counter by 2.
    def SNE_4xkk(self, VX: NBitRegister, kk: int) -> None:
        if VX.value != kk:
            self.PC.value += 0x02

    # The interpreter compares register Vx to register Vy, and if they are equal, increments the program counter by 2.
    def SE_5xy0(self, VX: NBitRegister, VY: NBitRegister) -> None:
        if VX.value == VY.value:
            self.PC.value += 0x02

    # The interpreter puts the value kk into register Vx.
    def LD_6xkk(self, VX:NBitRegister, kk: int) -> None:
        VX.value = kk

    # Adds the value kk to the value of register Vx, then stores the result in Vx.
    def ADD_7xkk(self, VX: NBitRegister, kk: int) -> None:
        result = VX.value + kk
        VX.value = result

    # Stores the value of register Vy in register Vx.
    def LD_8xy0(self, VX: NBitRegister, VY: NBitRegister) -> None:
        VX.value = VY.value

    # Performs a bitwise OR on the values of Vx and Vy, then stores the result in Vx. A bitwise OR compares the corrseponding bits from two values, and if either bit is 1, then the same bit in the result is also 1. Otherwise, it is 0.
    def OR_8xy1(self, VX: NBitRegister, VY: NBitRegister) -> None:
        result = VX.value | VY.value 
        VX.value = result

    # Performs a bitwise AND on the values of Vx and Vy, then stores the result in Vx. A bitwise AND compares the corrseponding bits from two values, and if both bits are 1, then the same bit in the result is also 1. Otherwise, it is 0.
    def AND_8xy2(self, VX: NBitRegister, VY: NBitRegister) -> None:
        result = VX.value & VY.value
        VX.value = result

    # Performs a bitwise exclusive OR on the values of Vx and Vy, then stores the result in Vx. An exclusive OR compares the corrseponding bits from two values, and if the bits are not both the same, then the corresponding bit in the result is set to 1. Otherwise, it is 0.
    def XOR_8xy3(self, VX: NBitRegister, VY: NBitRegister) -> None:
        result = VX.value ^ VY.value
        VX.value = result

    # The values of Vx and Vy are added together. If the result is greater than 8 bits (i.e., > 255,) VF is set to 1, otherwise 0. Only the lowest 8 bits of the result are kept, and stored in Vx.
    def ADD_8xy4(self, VX: NBitRegister, VY: NBitRegister) -> None:
        result = VX.value + VY.value
        if result > 255:
            self.Vf.value = 1
        VX.value = result

    # If Vx > Vy, then VF is set to 1, otherwise 0. Then Vy is subtracted from Vx, and the results stored in Vx.
    def SUB_8xy5(self, VX: NBitRegister, VY: NBitRegister) -> None:
        if VX.value > VY.value:
            self.Vf.value = 1
        else:
            self.Vf.value = 0
        result = VX.value - VY.value
        VX.value = result

    # If the least-significant bit of Vx is 1, then VF is set to 1, otherwise 0. Then Vx is divided by 2.
    def SHR_8xy6(self, VX: NBitRegister) -> None:
        if VX.value & 0x01:
            self.Vf.value = 1
        else:
            self.Vf.value = 0
        VX.value = VX.value >> 1

    # If Vy > Vx, then VF is set to 1, otherwise 0. Then Vx is subtracted from Vy, and the results stored in Vx.
    def SUBN_8xy7(self, VX: NBitRegister, VY: NBitRegister) -> None:
        if VY.value > VX.value:
            self.Vf.value = 1
        else: 
            self.Vf.value = 0
        result = VY.value - VX.value
        VX.value = result

    # If the most-significant bit of Vx is 1, then VF is set to 1, otherwise to 0. Then Vx is multiplied by 2.
    def SHL_8xyE(self, VX: NBitRegister) -> None:
        if VX.value & 0x80:
            self.Vf.value = 1
        else:
            self.Vf.value = 0
        VX.value = VX.value << 1

    # The values of Vx and Vy are compared, and if they are not equal, the program counter is increased by 2.
    def SNE_9xy0(self, VX: NBitRegister, VY: NBitRegister) -> None:
        if VX.value != VY.value:
            self.PC.value += 0x02

    # The value of register I is set to nnn.
    def LD_Annn(self, addr: int) -> None:
        self.Vi.value = addr

    # The program counter is set to nnn plus the value of V0.
    def JP_Bnnn(self, addr: int) -> None:
        self.PC.value = (addr + self.V0.value) & 0xFFF

    # The interpreter generates a random number from 0 to 255, which is then ANDed with the value kk. The results are stored in Vx. See instruction 8xy2 for more information on AND.
    def RND_Cxkk(self, VX: NBitRegister, kk: int) -> None:
        VX.value = random.randint(0, 255)
        VX.value = VX.value & kk

    # The interpreter reads n bytes from memory, starting at the address stored in I. These bytes are then displayed as sprites on screen at coordinates (Vx, Vy). Sprites are XORed 
    # onto the existing screen. If this causes any pixels to be erased, VF is set to 1, otherwise it is set to 0. If the sprite is positioned so part of it is outside the coordinates 
    # of the display, it wraps around to the opposite side of the screen. See instruction 8xy3 for more information on XOR, and section 2.4, Display, for more information on the Chip-8 
    # screen and sprites.
    def DRW_Dxyn(self, VX: NBitRegister, VY: NBitRegister, n: int) -> None:
        starting_point = self.Vi.value # Posicion desde la que se comienza a leer en la RAM
        x_cord = VX.value
        y_cord = VY.value
        read_from_memory: int = 0
        flag: bool = False

        for i in range(0, n):
            read_from_memory = self.ram.read(starting_point + i) # Se extrae el byte desde la ram
            bits = [int(b) for b in f"{read_from_memory:08b}"]   # Se transforma el valor a una lista de bits

            for j in range(len(bits)):
                x_teorica = x_cord + j
                y_teorica = y_cord + i

                x_real = x_teorica % 64
                y_real = y_teorica % 32

                idx = (y_real * ANCHO_CHIP8) + x_real
                pixel = self.matriz_video[idx]
                self.matriz_video[idx] = bits[j] ^ self.matriz_video[idx]   # Se aplica un XOR a cada pixel para encender/apagar.
                 
                if pixel == 1 and self.matriz_video[idx] == 0:  # Si al aplicar el XOR, se apago el pixel, se levanta el flag.
                    flag = True
        if flag:
            self.Vf.value = 1
        else: 
            self.Vf.value = 0

    # Checks the keyboard, and if the key corresponding to the value of Vx is currently in the down position, PC is increased by 2.
    def SKP_Ex9E(self, VX: NBitRegister) -> None:
        if self.keys[VX.value & 0x0F]:
            self.PC.value += 2

    # Checks the keyboard, and if the key corresponding to the value of Vx is currently in the up position, PC is increased by 2.
    def SKNP_ExA1(self, VX: NBitRegister) -> None:
        if not self.keys[VX.value & 0x0F]:
            self.PC.value += 2

    # The value of DT is placed into Vx.
    def LD_Fx07(self, VX: NBitRegister) -> None:
        VX.value = self.DT.value

    # All execution stops until a key is pressed, then the value of that key is stored in Vx. 
    def LD_Fx0A(self, VX: NBitRegister) -> None:

        tecla_presionada = False
    
        # Revisamos si hay AL MENOS UNA tecla presionada en este exacto momento
        for i in range(16):
            if self.keys[i]:
                # Si encontramos una tecla presionada, guardamos su valor en Vx
                VX.value = i
                tecla_presionada = True
                break # Salimos del ciclo 'for'

        # Si terminamos de revisar las 16 teclas y ninguna está presionada...
        if not tecla_presionada:
            # Retrocedemos el PC. 
            # (Asumiendo que tu ciclo principal ya sumó 2 al PC durante el Fetch)
            self.PC.value -= 2

    # DT is set equal to the value of Vx.
    def LD_Fx15(self, VX: NBitRegister) -> None:
        self.DT.value = VX.value

    # ST is set equal to the value of Vx.
    def LD_Fx18(self, VX: NBitRegister) -> None:
        self.ST.value = VX.value

    # The values of I and Vx are added, and the results are stored in I.
    def ADD_Fx1E(self, VX: NBitRegister) -> None:
        self.Vi.value += VX.value

    # The value of I is set to the location for the hexadecimal sprite corresponding to 
    # the value of Vx. See section 2.4, Display, for more information on the Chip-8 hexadecimal font.
    def LD_Fx29(self, VX: NBitRegister) -> None:
        self.Vi.value = self.digits[VX.value]

    # The interpreter takes the decimal value of Vx, and places the hundreds digit in memory at location 
    # in I, the tens digit at location I+1, and the ones digit at location I+2.
    def LD_Fx33(self, VX: NBitRegister) -> None:
        hundreds = (VX.value // 100) % 10
        tens = (VX.value % 100) // 10
        ones = VX.value % 10
        self.ram.write(self.Vi.value, hundreds)
        self.ram.write(self.Vi.value + 1, tens)
        self.ram.write(self.Vi.value + 2, ones)

    # The interpreter copies the values of registers V0 through Vx into memory, starting at the address in I.
    def LD_Fx55(self, VX: NBitRegister) -> None:
        idx = 0
        while VX != self.V[idx]:
            self.ram.write(self.Vi.value + idx, self.V[idx].value)
            idx += 1
        self.ram.write(self.Vi.value + idx, VX.value)

    # The interpreter reads values from memory starting at location I into registers V0 through Vx.
    def LD_Fx65(self, VX: NBitRegister) -> None:
        idx = 0
        while VX != self.V[idx]:
            self.V[idx].value = self.ram.read(self.Vi.value + idx)
            idx += 1
        VX.value = self.ram.read(self.Vi.value + idx)