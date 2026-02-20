from chip8 import Chip8

def test_basic_opcodes():
    cpu = Chip8()
    # Program:
    # 0x200: 00 E0  - Clear Screen
    # 0x202: 60 10  - V0 = 16
    # 0x204: 61 10  - V1 = 16
    # 0x206: A0 50  - I = 0x050 (Address of '0' font)
    # 0x208: D0 15  - Draw sprite at (V0, V1) height 5
    # 0x20A: 12 0A  - JMP 0x20A (Infinite loop)
    
    rom = bytes([
        0x00, 0xE0,
        0x60, 0x10,
        0x61, 0x10,
        0xA0, 0x50,
        0xD0, 0x15,
        0x12, 0x0A
    ])
    
    cpu.load_rom(rom)
    
    # Run 6 instructions
    for _ in range(6):
        cpu.cycle()
        
    assert cpu.pc == 0x20A, f"Expected PC=0x20A, got {hex(cpu.pc)}"
    assert cpu.v[0] == 16, f"Expected V0=16, got {cpu.v[0]}"
    assert cpu.v[1] == 16, f"Expected V1=16, got {cpu.v[1]}"
    assert cpu.i == 0x050, f"Expected I=0x050, got {hex(cpu.i)}"
    
    # Check if a pixel was rendered at (16, 16)
    idx = 16 * 64 + 16
    assert cpu.display[idx] == True, "Expected display buffer at (16,16) to be True"
    assert cpu.draw_flag == True, "Expected draw_flag to be True"

    print("Basic opcode tests passed successfully!")

if __name__ == "__main__":
    test_basic_opcodes()
