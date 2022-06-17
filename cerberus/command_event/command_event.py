from cerberus.const import *

class CommandEvent:
    def __init__(self, original_command: int, crc: int, calc_crc: int, cmd_length: int = None):
        self.original_command = original_command
        self.crc = crc
        self.calc_crc = calc_crc

        if cmd_length == None:
            self.cmd_length = 32 if self.original_command > 0xFFFF else 16
        else:
            self.cmd_length = cmd_length

        self.__calculate_nearest_command(self.original_command, cmd_length)

    def __calculate_nearest_command(self, cmd: int, length: int) -> tuple:
        hamming_distance = float('inf')
        nearest_command = 0x0

        commands_to_check = LONG_COMMANDS

        if length == 16:
            commands_to_check = SHORT_COMMANDS

        for control_key in commands_to_check:
            current_hamming_distance = self.calculate_hamming_distance(cmd, commands_to_check[control_key])

            if hamming_distance > current_hamming_distance:
                hamming_distance = current_hamming_distance
                nearest_command = commands_to_check[control_key]

        self.cmd = nearest_command
        self.hamming_distance = hamming_distance
        self.distance = int(bin(cmd ^ nearest_command).rstrip('0'), 2) if bin(cmd ^ nearest_command).rstrip('0') != '0b' else 0
    
    def calculate_hamming_distance(self, n1: int, n2: int) -> int:
        x = n1 ^ n2
        setBits = 0
    
        while (x > 0) :
            setBits += x & 1
            x >>= 1
        
        return setBits