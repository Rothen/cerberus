from spidev import SpiDev
import numpy as np
 
class MCP3008:
    read_command = 0b11 << 6
    read_diff_command = 0b10 << 6
    read_channel_0 = read_command | (0 & 0x07) << 3  
    read_channel_1 = read_command | (1 & 0x07) << 3  
    read_channel_0_diff = read_diff_command | (0 & 0x07) << 3  
    read_channel_1_diff = read_diff_command | (1 & 0x07) << 3  

    def __init__(self, bus = 0, device = 0):
        self.bus, self.device = bus, device
        self.spi = SpiDev()
        self.open()
 
    def open(self):
        self.spi.open(self.bus, self.device)
        self.spi.max_speed_hz = 100000 # 75kHz, not 1MHz
    
    def read(self) -> list[int]:
        return self.spi.xfer2([self.read_channel_0, 0x0, 0x0])
    
    def read_1(self) -> list[int]:
        return self.spi.xfer2([self.read_channel_1, 0x0, 0x0])
    
    def read_diff(self) -> list[int]:
        return self.spi.xfer2([self.read_channel_0_diff, 0x0, 0x0])
    
    def read_diff_1(self) -> list[int]:
        return self.spi.xfer2([self.read_channel_1_diff, 0x0, 0x0])

    def transform(self, results: np.array) -> np.array:
        transformed_results = []

        for result in results:
            int_val = (result[0] & 0x01) << 9
            int_val |= (result[1] & 0xFF) << 1
            int_val |= (result[2] & 0x80) >> 7
            transformed_results.append(int_val & 0x3FF)
        
        return np.array(transformed_results)
            
            
    def close(self):
        self.spi.close()