import argparse
import os
import lxml.etree as ET
from utils.compression import compress, uncompress
from utils.specialprint import printe, printw, filecolored
from utils.savefile import savefile, script_save

parser = argparse.ArgumentParser(
    prog="extract fx",
    description="extracts effects from tracks to fx channels",
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
    help="track numbers to extract effects from (start counting from 0). if not specified, every track will be applied",
)
parser.add_argument(
    "-c",
    "--color",
    action="store_true",
    help="colorize the fx channels with the track colors",
)

parser.add_argument("--overwrite", action="store_true", help="overwrite the output file or the input file if no output was specified")
args = parser.parse_args()

if not os.path.isfile(args.input):
    printe(f"file '{filecolored(args.input)}' does not exist")
with open(args.input, "rb") as f:
    data = f.read()

if args.input.endswith(".mmpz"):
    data = uncompress(data)

root = ET.fromstring(data)
tracks = root.findall("./song/trackcontainer/")
mixer = root.find("./song/mixer")

track_numbers = []
if args.tracks:
    for i in args.tracks:
        if i not in track_numbers:
            if i <= len(tracks) - 1:
                if tracks[i].attrib["type"] not in ["0", "2"]:
                    printw(
                        f"ignoring track {i} ({tracks[i].attrib["name"]}). it's neither an instrument or a sample"
                    )
                else:
                    track_numbers.append(i)
            else:
                printe(f"track {i} doesn't exist (start counting from 0)")
else:
    for i in range(len(tracks)):
        if tracks[i].attrib["type"] in ["0", "2"]:
            track_numbers.append(i)

for i in track_numbers:
    fx_chain = tracks[i][0].find("fxchain")
    if fx_chain is not None:
        if len(fx_chain):
            # remove the fx from track
            tracks[i][0].remove(fx_chain)
            # add it to fx chan
            chan_num = str(len(mixer))
            if tracks[i][0].get("mixch"):
                track_mixchan = tracks[i][0].get("mixch")
            else:
                track_mixchan = "0"
            tracks[i][0].attrib["mixch"] = chan_num
            chan = ET.Element("mixerchannel", {"name": tracks[i].attrib["name"], "num": chan_num}, )
            send = ET.Element("send", {"amount": "1", "channel": track_mixchan})
            if args.color:
                if tracks[i].get("color"):
                    chan.attrib["color"] = tracks[i].attrib["color"]
            mixer.append(chan)
            chan.append(fx_chain)
            chan.append(send)
            

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