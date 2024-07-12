import argparse
import os
import lxml.etree as ET
from utils.compression import compress, uncompress
from utils.specialprint import printe, filecolored
from utils.savefile import savefile, script_save

parser = argparse.ArgumentParser(
    prog="height",
    description="change the height of the tracks",
    formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=30),
)
parser.add_argument(
    "-i", "--input", type=str, required=True, metavar="file", help="input file"
)
parser.add_argument("-o", "--output", type=str, metavar="file", help="output file")
parser.add_argument(
    "-t",
    "--tracks",
    type=int,
    nargs="*",
    metavar="n",
    help="track numbers to change the height of (start counting from 0). if not specified, every track will be changed",
)
parser.add_argument(
    "-ht",
    "--height",
    type=int,
    required=True,
    metavar="n",
    help="the height of the channels in pixels (minimum accepted by LMMS is 32)",
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
tracks = root.findall("./song/trackcontainer/")

track_numbers = []
if args.tracks:
    for i in args.tracks:
        if i not in track_numbers:
            if i <= len(tracks) - 1:
                track_numbers.append(i)
            else:
                printe(f"track {i} doesn't exist (start counting from 0)")
else:
    for i in range(len(tracks)):
        track_numbers.append(i)

for i in track_numbers:
    if args.height > 32:
        tracks[i].attrib["trackheight"] = str(args.height)
    else:
        tracks[i].attrib.pop("trackheight", None)


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
