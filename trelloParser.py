import json

with open("5IktL1TM.json") as f:
    board = json.load(f)

cards = board["cards"]
cards.sort(key=lambda x: x["pos"])

lists = {}

for lst in board["lists"]:
    if lst["closed"] != True:
        lists[lst["id"]] = lst["name"]

def formatDesc(card):
    print(card)
    if card["desc"] != "":
        desc = card["desc"]
        desc = "<li>" + desc.strip().replace("\n", "<br/>\n") + "\n</li>"
        return "<ul>" + desc + "</ul>"
    else:
        return ""

with open("/home/adam/scratch/out.html", "w") as f:
    f.write("<body>\n")
    for listID, listName in lists.items():
        f.write(f"{listName}:\n<ul>\n")
        for card in cards:
            if card["idList"] == listID:
                f.write("<li>" + card["name"] + "\n")
                f.write(formatDesc(card))
                f.write("</li>")
        f.write("</ul>")
    f.write("</body>")

