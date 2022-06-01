import re

import re

regex = r"GOT: (0x?[a-fA-F0-9]+), CRC: (0|1), CALC_CRC: (0|1)"

test_str = "GOT: 0x123f4, CRC: 0, CALC_CRC: 0"

matches = re.findall(regex, test_str)
print(matches)

''' for matchNum, match in enumerate(matches, start=1):
    
    print ("Match {matchNum} was found at {start}-{end}: {match}".format(matchNum = matchNum, start = match.start(), end = match.end(), match = match.group()))
    
    for groupNum in range(0, len(match.groups())):
        groupNum = groupNum + 1
        
        print ("Group {groupNum} found at {start}-{end}: {group}".format(groupNum = groupNum, start = match.start(groupNum), end = match.end(groupNum), group = match.group(groupNum)))
'''