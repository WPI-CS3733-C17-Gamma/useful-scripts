#!/usr/bin/env python3
import re
from collections import defaultdict

class Entry:
    def __init__(self, string):
        parts = string.replace("'", "''").split(", ")
        if len(parts) >= 3:
            self.title = ", ".join(parts[2:])
        else:
            self.title = ""
        self.name = ", ".join(parts[:2])

outString = ""
roomList = defaultdict(list)

with open("/home/adam/scratch/HospitalDirectory.csv") as f:
    for line in f:
        name, rooms = line.strip().split("\t")
        for room in re.split(r" and |/|, ", rooms):
            roomList[room].append(Entry(name.strip()))

roomIDs = {}
rID = 1000
eID = 1000
for room in roomList.keys():
    rID += 1
    roomIDs[room] = rID
    outString += f"INSERT INTO Rooms (rID, name) VALUES ({rID}, '{room}');\n"

for room, entries in roomList.items():
    for entry in entries:
        outString += f"INSERT INTO Entries (eID, name, title) VALUES ({eID}, '{entry.name}', '{entry.title}')\n"
        outString += f"INSERT INTO RoomEntryAssoc (eID, rID) VALUES ({eID}, {roomIDs[room]});\n"
        eID += 1


print(outString)
