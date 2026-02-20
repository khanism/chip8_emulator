# Python Chip-8 Emulator Implementation Plan

This plan details the architecture and steps required to build a fully functional Chip-8 emulator in Python. The emulator will use `pygame` for rendering the 64x32 monochrome graphical display, handling keyboard input, and playing sound.

## User Review Required

> [!NOTE]
> Please review the chosen dependencies and project structure. I have selected `pygame` as it provides an excellent balance of ease of use for 2D rendering and event handling in Python. Are you okay with proceeding using `pygame`? 

## Proposed Changes

The project will be organized into a modular structure to separate CPU logic from the graphical user interface.

### Project Structure
#### [NEW] requirements.txt
Will contain the required dependencies:
```
pygame>=2.5.0
```

#### [NEW] chip8.py
This will be the core CPU module. It will not have any Pygame dependencies, keeping the logic hardware-agnostic.
- **Memory**: 4096 bytes (0x000 to 0xFFF)
- **Registers**: 16 8-bit data registers (`V0`-`VF`), 1 16-bit index register (`I`), 8-bit delay timer, 8-bit sound timer.
- **Program Counter**: 16-bit `pc` initialized to 0x200.
- **Stack**: Array of 16 16-bit values and an 8-bit stack pointer (`sp`).
- **Display Buffer**: 64x32 boolean array representing pixels on/off state.
- **Keypad state**: Array of 16 booleans representing the state of keys 0-F.
- **Methods**: `load_rom()`, `cycle()`, and individual opcode handlers.

#### [NEW] display.py
This module will handle Pygame rendering.
- Initialize Pygame window.
- Method to draw the 64x32 display buffer onto the Pygame surface (scaled up so it's visible, e.g., 10x or 15x scale).
- Sound playback when the Chip-8 sound timer is active.

#### [NEW] input_handler.py
Map modern keyboards (QWERTY) to the 16-key Hexadecimal Chip-8 keypad:
```
Original Chip-8   =>  Modern Keyboard
1 2 3 C               1 2 3 4
4 5 6 D               Q W E R
7 8 9 E               A S D F
A 0 B F               Z X C V
```

#### [NEW] main.py
The entry point of the emulator.
- Initialize CPU, Display, and Input instances.
- Load the specified ROM file via command-line arguments.
- Contain the main event loop.
- Handle timing: CPU instructions typically run at around 500-700 Hz, while delay/sound timers strictly decrement at 60 Hz.

## Verification Plan

### Automated / Unit Tests
- Create unit tests for basic operations (e.g., ADD, SUB, bitwise operations) to ensure math behaves correctly.
- Test stack push/pop and flow control instructions like JMP and CALL.

