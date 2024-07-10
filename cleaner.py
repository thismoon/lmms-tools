import argparse
import os
import lxml.etree as ET
from utils.compression import compress, uncompress
from utils.specialprint import printe, filecolored
from utils.savefile import savefile, script_save

parser = argparse.ArgumentParser(
    prog="cleaner",
    description="cleans project files (used for readability. for reducing file size, use the compressor tool)",
    formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=30),
)
parser.add_argument(
    "-i", "--input", type=str, required=True, metavar="file", help="input file"
)
parser.add_argument("-o", "--output", type=str, metavar="file", help="output file")
parser.add_argument(
    "--microtone",
    action="store_true",
    help="keep the scales and keymaps (use this if the project uses microtonality)",
)
parser.add_argument("--notes", action="store_true", help="keep the project notes")
parser.add_argument("--ghost", action="store_true", help="keep the ghost notes")
parser.add_argument(
    "--scale", action="store_true", help="keep the marked semitones/scale"
)

parser.add_argument(
    "--overwrite",
    action="store_true",
    help="overwrite the output file or the input file if no output was specified",
)
args = parser.parse_args()

if not os.path.isfile(args.input):
    printe(f"file '{filecolored(args.input)}' does not exist")
with open(args.input, "rb") as f:
    data = f.read()

if args.input.endswith(".mmpz"):
    data = uncompress(data)

root = ET.fromstring(data)

song = root.find("song")

# remove creator version
root.attrib.pop("creatorversion", None)

# remove global automation
global_automation = song.find("track")
if global_automation is not None:
    song.remove(global_automation)

# remove project notes
if not args.notes:
    project_notes = song.find("projectnotes")
    if project_notes is not None:
        song.remove(project_notes)

if not args.microtone:
    # remove scales
    scales = song.find("scales")
    if scales is not None:
        song.remove(scales)
    # remove keymaps
    keymaps = song.find("keymaps")
    if keymaps is not None:
        song.remove(keymaps)

# clean notes
for i in song.findall("trackcontainer/track/midiclip/note"):
    # remove 0 panning
    if i.get("pan"):
        if i.attrib["pan"] == "0":
            i.attrib.pop("pan", None)
    # remove type 0
    if i.get("type"):
        if i.attrib["type"] == "0":
            i.attrib.pop("type", None)

# remove midi controllers if all values are equal to 0
for i in song.findall("trackcontainer/track/instrumenttrack"):
    midicontrollers = i.find("midicontrollers")
    if midicontrollers is not None:
        if all(x == "0" for x in midicontrollers.attrib.values()):
            i.remove(midicontrollers)

pianoroll = song.find("pianoroll")

# remove ghost notes
if not args.ghost:
    ghostnotes = pianoroll.find("ghostnotes")
    if ghostnotes is not None:
        pianoroll.remove(ghostnotes)

# remove marked semitones/scale
if not args.scale:
    markedSemiTones = pianoroll.find("markedSemiTones")
    if markedSemiTones is not None:
        pianoroll.remove(markedSemiTones)

header = '<?xml version="1.0"?>\n<!DOCTYPE lmms-project>\n'.encode()
data = header + ET.tostring(root)

if args.output:
    if args.output.endswith(".mmpz"):
        data = compress(data)
    if args.overwrite:
        script_save(data, args.output, "overwrite")
    else:
        savefile(data, args.output)
elif args.overwrite:
    if args.input.endswith(".mmpz"):
        data = compress(data)
    script_save(data, args.input, "overwrite")
else:
    print(data.decode())
