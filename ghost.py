import argparse
import os
import lxml.etree as ET
from utils.compression import compress, uncompress
from utils.specialprint import printe, filecolored
from utils.savefile import savefile

parser = argparse.ArgumentParser(
    description="exports ghost notes to a midi clip file (xpt/xptz)",
    formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=30),
)
parser.add_argument("-i", "--input", type=str, required=True, metavar="file", help="input file")
parser.add_argument("-o", "--output", type=str, metavar="file.xpt(z)", help="output file")
args = parser.parse_args()

if not os.path.isfile(args.input):
    printe(f"file '{filecolored(args.input)}' does not exist")
with open(args.input, "rb") as f:
    data = f.read()

if args.input.endswith(".mmpz"):
    data = uncompress(data)

root = ET.fromstring(data)

ghost_notes = root.find("song/pianoroll/ghostnotes")
if ghost_notes is None:
    printe("can't find ghost notes")

data = ET.tostring(root, encoding="UTF-8", xml_declaration=True)


midiclip = ET.Element(
        "lmms-project", {"version": "29", "type": "midiclip"}
    )
midiclip.append(ET.Element("head"))
midiclip.append(ET.Element("midiclip"))
for note in ghost_notes:
    note.tag = "note"
    note.attrib["vol"] = "100"
    midiclip.find("midiclip").append(note)

data = ET.tostring(midiclip, encoding="UTF-8", xml_declaration=True, pretty_print=True)

if args.output:
    if args.output.endswith(".xptz"):
        data = compress(data)
    savefile(data, args.output)
else:
    print(data.decode())
