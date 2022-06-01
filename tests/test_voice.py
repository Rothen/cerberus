from mcp3008 import MCP3008
import pickle
import time
import numpy as np

mcp = MCP3008()
results = []

t_end = time.time() + 5

while time.time() < t_end:
    results.append(mcp.read_diff_1())

data = mcp.transform(results)

with open("voice.pkl", "wb") as myfile:
    pickle.dump(data, myfile)

print(np.mean(data))
print(np.max(data))
print(np.min(data))