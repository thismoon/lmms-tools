import argparse
import os
import lxml.etree as ET
import random
import copy
import math
from utils.compression import compress, uncompress
from utils.specialprint import printe, filecolored
from utils.savefile import savefile, script_save
from utils.select import select_xml


def bpm_to_pitch(origin_bpm, new_bpm):
    semitones = -12 * math.log2(new_bpm / origin_bpm)
    return "{:.2f}".format(semitones)


parser = argparse.ArgumentParser(
    prog="pitch fixer",
    description="fixes the pitch of slicerT when automating tempo",
    formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=30),
)
parser.add_argument(
    "-i", "--input", type=str, required=True, metavar="file", help="input file"
)
parser.add_argument("-o", "--output", type=str, metavar="file", help="output file")
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

# get all valid slicerT instruments
slicert_instruments = []
for i in tracks:
    instrument = i.find("instrumenttrack/instrument/")
    if instrument is not None:
        if instrument.tag == "slicert":
            if instrument.attrib["syncEnable"] == "1":
                if (
                    i.find(
                        "instrumenttrack/fxchain/effect/GranularPitchShifterControls"
                    )
                    is not None
                ):
                    slicert_instruments.append(i)

# set the slicert instrument
if len(slicert_instruments) == 0:
    printe(
        "no valid slicerT instruments found. make sure it has the tempo sync on and a granular pitch shifter effect"
    )
elif len(slicert_instruments) == 1:
    slicert = slicert_instruments[0]
else:
    slicert = select_xml(slicert_instruments, "name")

origin_bpm = slicert.find("instrumenttrack/instrument/slicert").attrib["origBPM"]

# get the pitch shifter id
granular_effect = slicert.find(
    "instrumenttrack/fxchain/effect/GranularPitchShifterControls"
)
granular_effect.attrib.pop("pitch", None)

if granular_effect.find("pitch/") is not None:
    slicert_id = granular_effect.find("pitch/").attrib["id"]
else:
    slicert_id = str(random.randint(1000000, 9999999))
    id_element = ET.Element(
        "pitch", {"scale_type": "linear", "value": "0", "id": slicert_id}
    )
    granular_effect.insert(0, id_element)

# get the bpm id
if root.find("./head/bpm") is None:
    printe(
        "no bpm tag detected. make sure you have tempo linked to an automation track for it to generate"
    )
bpm_id = root.find("./head/bpm").attrib["id"]

# get all tempo tracks
tempo_tracks = []
for i in tracks:
    if i.attrib["type"] == "5":
        for x in i.findall("automationclip/object"):
            if x.attrib["id"] == bpm_id:
                tempo_tracks.append(i)
                break

# get the tempo track
if len(tempo_tracks) == 0:
    printe(
        "no tempo tracks found. make sure there is an automation track with clips linked to the tempo"
    )
elif len(tempo_tracks) == 1:
    tempo_track = tempo_tracks[0]
else:
    tempo_track = select_xml(tempo_tracks, "name")

# get rid of duplicate links
for i in tempo_track.findall("automationclip"):
    if len(i.findall("object")) > 1:
        objects = i.findall("object")
        for x in range(1, len(objects)):
            i.remove(objects[x])

pitch_track = copy.deepcopy(tempo_track)
pitch_track.attrib["name"] = "pitch"
clips = pitch_track.findall("automationclip")
for clip in clips:
    if clip.find("object").attrib["id"] == bpm_id:
        clip.attrib["name"] = "Granular Pitch Shifter>>Pitch"
        clip.find("object").attrib["id"] = slicert_id
        for i in clip.findall("time"):
            new_bpm = i.attrib["value"]
            new_bpm_out = i.attrib["outValue"]
            i.attrib["value"] = bpm_to_pitch(float(origin_bpm), float(new_bpm))
            i.attrib["outValue"] = bpm_to_pitch(float(origin_bpm), float(new_bpm_out))

root.find("./song/trackcontainer").append(pitch_track)

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
