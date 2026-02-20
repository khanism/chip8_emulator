import argparse
import sys
import pygame
from chip8 import Chip8
from display import Display
from input_handler import InputHandler

def main():
    parser = argparse.ArgumentParser(description="Antigravity Chip-8 Emulator")
    parser.add_argument("rom", help="Path to the Chip-8 ROM file to load")
    parser.add_argument("--scale", type=int, default=15, help="Display scale factor (default: 15)")
    parser.add_argument("--speed", type=int, default=10, help="CPU cycles per frame (60Hz). Default 10 = 600Hz.")
    args = parser.parse_args()

    # Initialize components
    cpu = Chip8()
    display = Display(scale_factor=args.scale)
    input_handler = InputHandler()

    # Load ROM
    try:
        with open(args.rom, "rb") as f:
            rom_data = f.read()
        cpu.load_rom(rom_data)
        print(f"Loaded ROM: {args.rom} ({len(rom_data)} bytes)")
    except Exception as e:
        print(f"Error loading ROM: {e}")
        sys.exit(1)

    clock = pygame.time.Clock()
    running = True

    while running:
        # Pygame loop runs at 60 FPS
        # 1 frame = 1 / 60 seconds
        
        # Poll inputs
        running = input_handler.process_events(cpu.keypad)
        
        # Run CPU cycles (e.g., 10 cycles per frame -> 600 cycles per sec)
        for _ in range(args.speed):
            cpu.cycle()
            
        # Update timers at 60Hz
        cpu.update_timers()
        
        # Update display if draw flag is set
        if cpu.draw_flag:
            display.draw(cpu.display)
            cpu.draw_flag = False
            
        # Handle sound
        if cpu.sound_timer > 0:
            display.play_sound()
        else:
            display.stop_sound()

        # Tick at 60 fps
        clock.tick(60)
        
    pygame.quit()
    sys.exit(0)

if __name__ == "__main__":
    main()
