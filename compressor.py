import argparse
import os
from utils.compression import compress, uncompress
from utils.specialprint import printe, filecolored
from utils.savefile import savefile

parser = argparse.ArgumentParser(
    formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=30)
)
parser.add_argument(
    "-i", "--input", type=str, required=True, metavar="file", help="input file"
)
parser.add_argument("-o", "--output", type=str, metavar="file", help="output file")
parser.add_argument("-c", "--compress", action="store_true", help="compresses the file")
parser.add_argument(
    "-u", "--uncompress", action="store_true", help="uncompresses the file"
)
args = parser.parse_args()

if not os.path.isfile(args.input):
    printe(f"file '{filecolored(args.input)}' does not exist")
with open(args.input, "rb") as f:
    data = f.read()

if args.compress and args.uncompress:
    printe("choose either compressing or uncompressing")

if args.compress:
    compressed = compress(data)
    if args.output:
        saved = savefile(compressed, args.output)
        print(
            f"compressed '{filecolored(os.path.basename(args.input))}' to '{filecolored(os.path.basename(saved))}'"
        )
    else:
        print(compressed)

if args.uncompress:
    uncompressed = uncompress(data)
    if args.output:
        saved = savefile(uncompressed, args.output)
        print(
            f"uncompressed '{filecolored(os.path.basename(args.input))}' to '{filecolored(os.path.basename(saved))}'"
        )
    else:
        print(uncompressed)
