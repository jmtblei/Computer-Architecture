"""CPU functionality."""

import sys

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010
class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        #Add list properties to the CPU class to hold 256 bytes of memory 
        self.ram = [0] * 256
        #and 8 general-purpose registers.
        self.reg = [0] * 8
        #stores program counter
        self.PC = self.reg[0]
    
    def ram_read(self, address):
        #ram_read() should accept the address to read and return the value stored there.
        return self.ram_read[address]
    
    def ram_write(self, value, address):
        #raw_write() should accept a value to write, and the address to write it to.
        self.ram[address] = value

    def load(self, program):
        """Load a program into memory."""
        try:
            address = 0
            with open(program) as f:
                for line in f:
                    comment_split = line.split("#")
                    number = comment_split[0].strip()
                    if number == "":
                        continue
                    value = int(number, 2)
                    self.ram_write(value, address)
                    address += 1
        except FileNotFoundError:
            print(f"{program} not found")
            sys.exit(2)
        if len(sys.argv) != 2:
            sys.exit(1)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        elif op == "MUL":
            self.reg[reg_a] = (self.reg[reg_a]) * (self.reg[reg_b])
            return 2
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

    def run(self):
        """Run the CPU."""
        running = True
        while running:
            #if-else cascade for actions
            IR = self.ram[self.PC]
            #setting operand a and b
            operand_a = self.ram[self.PC + 1]
            operand_b = self.ram[self.PC + 2]            
            if IR == HLT:
                #halt the program if instruction register matches halt value
                running = False
            elif IR == LDI:
                #set value of instruction register to integer
                self.reg[operand_a] = operand_b
                self.PC += 2
            elif IR == PRN:
                #print the value at instruction register
                print(self.reg[operand_a])
                self.PC += 1
            elif IR == MUL:
                self.PC += self.alu("MUL", operand_a, operand_b)
            else:
                #handle error
                print("Unknown command")
                sys.exit(1)
            self.PC += 1

