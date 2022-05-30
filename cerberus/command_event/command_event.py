from cerberus.const import *

class CommandEvent:
    def __init__(self, original_command: int, crc: int, calc_crc: int, cmd_length: int):
        self.original_command = original_command
        self.crc = crc
        self.calc_crc = calc_crc
        self.cmd_length = cmd_length

        self.__calculate_nearest_command(self.original_command, cmd_length)

    def __calculate_nearest_command(self, cmd: int, length: int) -> tuple:
        distance = float('inf')
        nearest_command = 0x0

        commands_to_check = LONG_COMMANDS

        if length == 16:
            commands_to_check = SHORT_COMMANDS

        for control_key in commands_to_check:
            hamming_distance = self.hamming_distance(cmd, commands_to_check[control_key])

            if distance > hamming_distance:
                distance = hamming_distance
                nearest_command = commands_to_check[control_key]

        self.cmd = nearest_command
        self.distance = distance
    
    def hamming_distance(self, n1: int, n2: int) -> int:
        x = n1 ^ n2
        setBits = 0
    
        while (x > 0) :
            setBits += x & 1
            x >>= 1
        
        return setBits