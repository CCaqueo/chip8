import sys
from renderizar_pantalla import *
from Chip8 import *

def main():

     rom = sys.argv[1]

     chip8 = Chip8()
     ventana = inicializar_ventana()
     clock = pygame.time.Clock()

     with open(rom, "rb") as rom_file:
         # Read all bytes
         rom_data = rom_file.read()
         chip8.load_rom(rom_data)
     

     teclas_chip8 = {
         pygame.K_0: 0,
         pygame.K_1: 1,
         pygame.K_2: 2,
         pygame.K_3: 3,
         pygame.K_4: 4,
         pygame.K_5: 5,
         pygame.K_6: 6,
         pygame.K_7: 7,
         pygame.K_8: 8,
         pygame.K_9: 9,
         pygame.K_a: 10,
         pygame.K_b: 11,
         pygame.K_c: 12,
         pygame.K_d: 13,
         pygame.K_e: 14,
         pygame.K_f: 15
     }

     running = True
     while running:

          for event in pygame.event.get():
               if event.type == pygame.QUIT:
                   running = False

               elif event.type == pygame.KEYDOWN:
                    # Verificamos si la tecla presionada está en nuestro diccionario
                    if event.key in teclas_chip8:
                         indice = teclas_chip8[event.key]
                         chip8.keys[indice] = True                    
                
               elif event.type == pygame.KEYUP:
                    # Hacemos lo mismo cuando se suelta la tecla
                    if event.key in teclas_chip8:
                        indice = teclas_chip8[event.key]
                        chip8.keys[indice] = False

          # Se añade el ciclo for para que la CPU corra a 600 MHz 
          for _ in range(10):
               chip8.ciclo_cpu()

          if chip8.DT.value > 0:
               chip8.DT.value -= 1
          if chip8.ST.value > 0:
               chip8.ST.value -= 1

          # La pantalla solo se renderiza si se ejecutó la instrucción DRW_Dxyn.
          if chip8.draw_flag:
              chip8.renderizar_pantalla(ventana=ventana)
              chip8.draw_flag = False

          clock.tick(60)

     pygame.quit()
        

if __name__ == "__main__":
        main()
