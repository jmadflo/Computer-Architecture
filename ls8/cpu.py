"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0

    def load(self):
        """Load a program into memory."""

        address = 0

        # # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1
        with open(sys.argv[1], 'r') as program:
            for instruction in program:
                if '#' in instruction:
                    instruction = instruction.split()[0]
                else:
                    instruction = instruction.replace('\n', '')
                self.ram[address] = int(instruction, 2)
                address += 1
            # print(self.ram)
                

    def ram_read(self, slot):
        return self.ram[slot]

    def ram_write(self, slot, val):
        self.ram[slot] = val
        
    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()
    
    # def LDI():
    #     reg_slot = self.ram[self.pc + 1]
    #     val = self.ram[self.pc + 2]
    #     self.reg[reg_slot] = val
    #     self.pc += 3


    def run(self):
        """Run the CPU."""
        running = True
        while running:
            instruction = self.ram_read(self.pc)

            if instruction == 0b00000001: # HLT
                running = False
            elif instruction == 0b10000010: # LDI
                reg_slot = self.ram[self.pc + 1]
                val = self.ram[self.pc + 2]
                self.reg[reg_slot] = val
                self.pc += 3
            elif instruction == 0b01000111: # PRN
                reg_slot = self.ram[self.pc + 1]
                print(self.reg[reg_slot])
                self.pc += 2
            elif instruction == 0b10100010: # MUL
                reg_slot_1 = self.ram[self.pc + 1]
                reg_slot_2 = self.ram[self.pc + 2]
                self.alu('MUL', reg_slot_1, reg_slot_2)
                self.pc += 3