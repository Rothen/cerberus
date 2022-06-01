from mcp3008 import MCP3008
import numpy as np
import pickle
import time

mcp = MCP3008()
values = []

# while True:
print(mcp.transform([mcp.read()]))
print(mcp.transform([mcp.read_1()]))
print(mcp.transform([mcp.read_diff()]))
print(mcp.transform([mcp.read_diff_1()]))