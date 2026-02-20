import pygame
from typing import List

class InputHandler:
    def __init__(self):
        # Map modern keyboard keys to standard Chip-8 16-key keypad
        # 1 2 3 C => 1 2 3 4
        # 4 5 6 D => Q W E R
        # 7 8 9 E => A S D F
        # A 0 B F => Z X C V
        self.keymap = {
            pygame.K_x: 0x0,
            pygame.K_1: 0x1,
            pygame.K_2: 0x2,
            pygame.K_3: 0x3,
            pygame.K_q: 0x4,
            pygame.K_w: 0x5,
            pygame.K_e: 0x6,
            pygame.K_a: 0x7,
            pygame.K_s: 0x8,
            pygame.K_d: 0x9,
            pygame.K_z: 0xA,
            pygame.K_c: 0xB,
            pygame.K_4: 0xC,
            pygame.K_r: 0xD,
            pygame.K_f: 0xE,
            pygame.K_v: 0xF
        }

    def process_events(self, keypad_buffer: List[bool]) -> bool:
        """
        Polls Pygame events and updates the keypad state.
        Returns False if the emulator should quit (Window closed).
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                if event.key in self.keymap:
                    keypad_buffer[self.keymap[event.key]] = True
                    
            if event.type == pygame.KEYUP:
                if event.key in self.keymap:
                    keypad_buffer[self.keymap[event.key]] = False
                    
        return True
