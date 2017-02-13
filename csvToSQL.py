#!/usr/bin/env python3

rooms = {}


# start high to not clobber other things
eID = 1000
rID = 1000

inputFile = "test.csv"
outputFile = "test.sql"

with open(inputFile) as f:
    with open(outputFile, "w+") as outF:
        outF.write("connect 'jdbc:derby:main;create=true';\n")
        for line in f:
            eID += 1
            parts = line.split("	")
            eName = parts[0].replace("'", "")
            room = parts[1].strip()
            if (room not in rooms):
                rID += 1
                outF.write(f"insert into Rooms (rID, name) values ({rID}, '{room}');\n")
            rooms[room] = rID

            outF.write(f"insert into Entries (eID, name) values ({eID}, '{eName}');\n")
            outF.write(f"insert into RoomEntryAssoc (eID, rID) values ({eID}, {rID});\n")
