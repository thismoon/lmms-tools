import argparse
import os
import lxml.etree as ET
from utils.compression import compress, uncompress
from utils.specialprint import printe, filecolored
from utils.gradient import generate_gradient
from utils.savefile import savefile, script_save

parser = argparse.ArgumentParser(
    description="colorizes tracks (or fx channels) with a gradient",
    formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=30),
)
parser.add_argument("-i", "--input", type=str, required=True, metavar="file", help="input file")
parser.add_argument("-o", "--output", type=str, metavar="file", help="output file")
parser.add_argument(
    "-c",
    type=str,
    required=True,
    metavar="'color1 color2'",
    help="gradient colors between quotes. e.g. -c '#ffffff #000000'",
)
parser.add_argument(
    "-f",
    "--fx",
    action="store_true",
    help="colorize the fx channels instead of the tracks (including the master)",
)
parser.add_argument(
    "-r",
    "--range",
    type=int,
    nargs=2,
    metavar=("n", "n"),
    help="(optional) number of the first and last tracks to color. start counting from 0",
)
parser.add_argument("--overwrite", action="store_true", help="overwrite the output file or the input file if no output was specified")
args = parser.parse_args()

if not os.path.isfile(args.input):
    printe(f"file '{filecolored(args.input)}' does not exist")
with open(args.input, "rb") as f:
    data = f.read()

colors = []
for i in args.c.split():
    if not i.startswith("#"):
        i = "#" + i
    colors.append(i)

if args.input.endswith(".mmpz"):
    data = uncompress(data)

root = ET.fromstring(data)

if args.fx:
    items = root.findall("./song/mixer/")
else:
    items = root.findall("./song/trackcontainer/")

if args.range:
    args.range.sort()
    starting_item, ending_item = args.range[0], args.range[1]
    if ending_item > len(items):
        ending_item = len(items) - 1
    item_count = ending_item - starting_item + 1

else:
    item_count = len(items)
    starting_item = 0

gradient_colors = generate_gradient(colors[0], colors[1], item_count)
for i in range(item_count):
    item = items[i + starting_item]
    item.set("color", gradient_colors[i])

header = "<?xml version=\"1.0\"?>\n<!DOCTYPE lmms-project>\n".encode()
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
