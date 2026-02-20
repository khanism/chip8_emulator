import pygame
from typing import List

class Display:
    def __init__(self, scale_factor: int = 15):
        # Initialize pygame display
        pygame.init()
        
        self.width = 64
        self.height = 32
        self.scale = scale_factor
        
        # Create a window scaled up from 64x32
        self.screen = pygame.display.set_mode((self.width * self.scale, self.height * self.scale))
        pygame.display.set_caption("Antigravity Chip-8 Emulator")
        
        self.color_on = (230, 230, 230) # Off-white
        self.color_off = (20, 20, 20)   # Dark gray
        
        # A simple beep sound for the sound timer
        # Pygame's mixer doesn't easily let us generate tones directly without extra code
        # We will create a simple array-based sound dynamically or load it
        # Actually it's easier to create a Sound object from a buffer or we can just ignore for strict compliance,
        # but let's init mixer
        pygame.mixer.init()
        self._setup_beep()
        self.is_beeping = False

    def _setup_beep(self):
        """Creates a simple square wave beep sound."""
        import numpy as np
        
        sample_rate = 44100
        duration = 0.1 # 100 ms
        freq = 440.0 # Hz (A4)
        
        # Generate wave
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        wave = np.sin(freq * t * 2 * np.pi)
        
        # Convert to 16-bit integers
        audio = np.int16(wave * 32767)
        # Duplicate to stereo (2 channels)
        stereo_audio = np.column_stack((audio, audio))
        
        from pygame.mixer import Sound, pre_init
        pygame.mixer.pre_init(sample_rate, -16, 2, 512)
        try:
            self.beep = pygame.sndarray.make_sound(stereo_audio)
        except Exception:
            self.beep = None # In case numpy isn't available or sound fails

    def draw(self, display_buffer: List[bool]):
        """Renders the Chip-8 64x32 display buffer onto the screen."""
        self.screen.fill(self.color_off)
        
        for y in range(self.height):
            for x in range(self.width):
                if display_buffer[y * self.width + x]:
                    rect = pygame.Rect(
                        x * self.scale,
                        y * self.scale,
                        self.scale,
                        self.scale
                    )
                    pygame.draw.rect(self.screen, self.color_on, rect)
                    
        pygame.display.flip()
        
    def play_sound(self):
        if self.beep and not self.is_beeping:
            self.beep.play(-1) # Loop indefinitely
            self.is_beeping = True
            
    def stop_sound(self):
        if self.beep and self.is_beeping:
            self.beep.stop()
            self.is_beeping = False
