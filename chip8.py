import random

class Chip8:
    def __init__(self):
        # 4096 bytes of memory (0x000 - 0xFFF)
        self.memory = bytearray(4096)
        
        # 16 8-bit registers (V0 - VF)
        self.v = bytearray(16)
        
        # 16-bit index register
        self.i = 0
        
        # 16-bit program counter, starts at 0x200
        self.pc = 0x200
        
        # Stack: array of 16 16-bit values
        self.stack = [0] * 16
        # Stack pointer
        self.sp = 0
        
        # Timers (8-bit)
        self.delay_timer = 0
        self.sound_timer = 0
        
        # Display: 64x32 monochrome pixels
        self.display = [False] * (64 * 32)
        
        # Keypad state: 16 keys (0-F)
        self.keypad = [False] * 16
        
        # Flag to indicate if display needs to be updated
        self.draw_flag = False
        
        # Load the standard Chip-8 8x5 fontset into memory (0x050 - 0x09F)
        fontset = [
            0xF0, 0x90, 0x90, 0x90, 0xF0, # 0
            0x20, 0x60, 0x20, 0x20, 0x70, # 1
            0xF0, 0x10, 0xF0, 0x80, 0xF0, # 2
            0xF0, 0x10, 0xF0, 0x10, 0xF0, # 3
            0x90, 0x90, 0xF0, 0x10, 0x10, # 4
            0xF0, 0x80, 0xF0, 0x10, 0xF0, # 5
            0xF0, 0x80, 0xF0, 0x90, 0xF0, # 6
            0xF0, 0x10, 0x20, 0x40, 0x40, # 7
            0xF0, 0x90, 0xF0, 0x90, 0xF0, # 8
            0xF0, 0x90, 0xF0, 0x10, 0xF0, # 9
            0xF0, 0x90, 0xF0, 0x90, 0x90, # A
            0xE0, 0x90, 0xE0, 0x90, 0xE0, # B
            0xF0, 0x80, 0x80, 0x80, 0xF0, # C
            0xE0, 0x90, 0x90, 0x90, 0xE0, # D
            0xF0, 0x80, 0xF0, 0x80, 0xF0, # E
            0xF0, 0x80, 0xF0, 0x80, 0x80  # F
        ]
        
        for i, byte in enumerate(fontset):
            self.memory[0x050 + i] = byte

    def load_rom(self, rom_data: bytes):
        """Loads ROM data into memory starting at 0x200."""
        for i, byte in enumerate(rom_data):
            self.memory[0x200 + i] = byte

    def cycle(self):
        """Executes a single CPU cycle."""
        # 1. Fetch instruction
        # A Chip-8 instruction is 2 bytes long.
        opcode = (self.memory[self.pc] << 8) | self.memory[self.pc + 1]
        print(hex(opcode))
        
        # Increment PC before execution
        self.pc += 2
        
        # 2. Decode and execute instruction
        self.execute_opcode(opcode)

    def execute_opcode(self, opcode: int):
        """Decodes and executes the given 16-bit opcode."""
        # Extract common variables from opcode
        # X: 2nd nibble (used for register VX)
        x = (opcode & 0x0F00) >> 8
        # Y: 3rd nibble (used for register VY)
        y = (opcode & 0x00F0) >> 4
        # N: 4th nibble (4-bit number)
        n = opcode & 0x000F
        # NN: 2nd byte (8-bit number)
        nn = opcode & 0x00FF
        # NNN: 12-bit address
        nnn = opcode & 0x0FFF
        
        # Leading nibble tells us the instruction type
        instruction_type = (opcode & 0xF000) >> 12

        match instruction_type:
            case 0x0:
                if opcode == 0x00E0:
                    # 00E0: Clear the display
                    self.display = [False] * (64 * 32)
                    self.draw_flag = True
                elif opcode == 0x00EE:
                    # 00EE: Return from a subroutine
                    self.pc = self.stack[self.sp - 1]
                    self.sp -= 1
            case 0x1:
                # 1NNN: Jump to address NNN
                self.pc = nnn
            case 0x2:
                # 2NNN: Call subroutine at NNN
                self.stack[self.sp] = self.pc
                self.sp += 1
                self.pc = nnn
            case 0x3:
                # 3XNN: Skip next instruction if VX == NN
                if self.v[x] == nn:
                    self.pc += 2
            case 0x4:
                # 4XNN: Skip next instruction if VX != NN
                if self.v[x] != nn:
                    self.pc += 2
            case 0x5:
                # 5XY0: Skip next instruction if VX == VY
                if self.v[x] == self.v[y]:
                    self.pc += 2
            case 0x6:
                # 6XNN: Set VX = NN
                self.v[x] = nn
            case 0x7:
                # 7XNN: Add NN to VX
                self.v[x] = (self.v[x] + nn) & 0xFF
            case 0x8:
                # 8-series operations
                match n:
                    case 0x0:
                        self.v[x] = self.v[y]
                    case 0x1:
                        self.v[x] |= self.v[y]
                        # self.v[0xF] = 0 # Some quirks might need VF to be reset
                    case 0x2:
                        self.v[x] &= self.v[y]
                    case 0x3:
                        self.v[x] ^= self.v[y]
                    case 0x4:
                        total = self.v[x] + self.v[y]
                        self.v[x] = total & 0xFF
                        self.v[0xF] = 1 if total > 255 else 0
                    case 0x5:
                        flag = 1 if self.v[x] >= self.v[y] else 0
                        self.v[x] = (self.v[x] - self.v[y]) & 0xFF
                        self.v[0xF] = flag
                    case 0x6:
                        flag = self.v[x] & 0x1
                        self.v[x] = (self.v[x] >> 1)
                        self.v[0xF] = flag
                    case 0x7:
                        flag = 1 if self.v[y] >= self.v[x] else 0
                        self.v[x] = (self.v[y] - self.v[x]) & 0xFF
                        self.v[0xF] = flag
                    case 0xE:
                        flag = (self.v[x] & 0x80) >> 7
                        self.v[x] = (self.v[x] << 1) & 0xFF
                        self.v[0xF] = flag
            case 0x9:
                # 9XY0: Skip next instruction if VX != VY
                if self.v[x] != self.v[y]:
                    self.pc += 2
            case 0xA:
                # ANNN: Set I = NNN
                self.i = nnn
            case 0xB:
                # BNNN: Jump to address NNN + V0
                self.pc = nnn + self.v[0]
            case 0xC:
                # CXNN: Set VX = random byte & NN
                self.v[x] = random.randint(0, 255) & nn
            case 0xD:
                # DXYN: Draw sprite
                x_coord = self.v[x] % 64
                y_coord = self.v[y] % 32
                self.v[0xF] = 0
                
                for row in range(n):
                    sprite_byte = self.memory[self.i + row]
                    for col in range(8):
                        sprite_pixel = sprite_byte & (0x80 >> col)
                        if sprite_pixel:
                            # Screen wrapping might be handled differently in different interpreters. Standard is to wrap or clip.
                            # We implement clipping as per standard original Chip-8 behavior
                            px = x_coord + col
                            py = y_coord + row
                            if px < 64 and py < 32:
                                screen_idx = py * 64 + px
                                if self.display[screen_idx]:
                                    self.v[0xF] = 1
                                self.display[screen_idx] ^= True
                
                self.draw_flag = True
            case 0xE:
                if nn == 0x9E:
                    # EX9E: Skip next instruction if key in VX is pressed
                    if self.keypad[self.v[x]]:
                        self.pc += 2
                elif nn == 0xA1:
                    # EXA1: Skip next instruction if key in VX is not pressed
                    if not self.keypad[self.v[x]]:
                        self.pc += 2
            case 0xF:
                match nn:
                    case 0x07:
                        self.v[x] = self.delay_timer
                    case 0x0A:
                        # FX0A: Wait for key press
                        key_pressed = False
                        for idx, state in enumerate(self.keypad):
                            if state:
                                self.v[x] = idx
                                key_pressed = True
                                break
                        if not key_pressed:
                            # Wait by re-executing this instruction
                            self.pc -= 2
                    case 0x15:
                        self.delay_timer = self.v[x]
                    case 0x18:
                        self.sound_timer = self.v[x]
                    case 0x1E:
                        self.i += self.v[x]
                        # Original behavior says VF not affected, though Amiga interpreter sets VF if I > 0xFFF.
                        # We will skip VF setting to be safe for most ROMs.
                    case 0x29:
                        # FX29: Set I to location of sprite for digit VX
                        self.i = 0x050 + (self.v[x] * 5)
                    case 0x33:
                        # FX33: Store BCD representation of VX at I, I+1, I+2
                        val = self.v[x]
                        self.memory[self.i] = val // 100
                        self.memory[self.i + 1] = (val // 10) % 10
                        self.memory[self.i + 2] = val % 10
                    case 0x55:
                        # FX55: Store V0 to VX in memory starting at I
                        for reg_idx in range(x + 1):
                            self.memory[self.i + reg_idx] = self.v[reg_idx]
                        # Legacy interpreters mutated I! (self.i += x + 1). Modern ones do not.
                        # Setting not to mutate is generally safer for newer ROMs.
                    case 0x65:
                        # FX65: Fill V0 to VX with values from memory starting at I
                        for reg_idx in range(x + 1):
                            self.v[reg_idx] = self.memory[self.i + reg_idx]
            case _:
                print(f"Unknown opcode: {hex(opcode)}")

    def update_timers(self):
        """Updates the delay and sound timers. Should be called at 60Hz."""
        if self.delay_timer > 0:
            self.delay_timer -= 1
        
        if self.sound_timer > 0:
            self.sound_timer -= 1
