<div align="center">
    <h1><img src="assets/lmms tools icon.png" alt="LMMS tools icon. an edit of the LMMS logo replacing the icon with a wrench icon from Material Symbols"><br> LMMS tools</h1>
    <p>python cli tools for LMMS users</p>
</div>

# dependencies

you need python and the lxml library

# tools

you can use the `-h`/`--help` argument with every tool for help

the tools will take care of the compression depending on the output file extension

## [compressor](compressor.py)

Compress or uncompress a file. compressed project files use the `.mmpz` extension and uncompressed ones use `.mmp`

```sh
python compressor.py -i file.mmpz -u -o file.mmp
```

## [colorize](colorize.py)

colorize tracks/fx channels with a gradient.

```sh
python colorize.py -i file.mmpz -c '#000000 #ffffff' --overwrite
```

## [extract fx](extract_fx.py)

extracts the effects from tracks with effects to an fx channel

```sh
python extract_fx.py -i file.mmpz -o file2.mmpz
```

## [chord finder](chord_finder.py)

find a chord name from it's notes

```
python chord_finder.py f g# c e d
Fm-Maj7add13
E7#5b9
Dm9b5
```

## [ghost](ghost.py)

extract ghost notes as a midi clip

```sh
python ghost.py -i file.mmpz -o file.xptz
```

## [cleaner](cleaner.py)

clean project files from unnecessary xml tags. this won't "optimize" the project but it will make it easier to read when editing with a text editor.<br>
it will remove the lmms version, global automation, project notes, scales and keymaps, notes type and pan (if set to 0), midicontrollers (if set to 0/unused), ghost notes and marked semitones/scales. some of those can be disabled by adding arguments to the command. (run `python cleaner.py -h`)

```sh
python cleaner.py -i file.mmpz -o file2.mmpz --notes
```

(the above command won't remove the project notes because of the `--notes` argument)

## [pitch fixer](pitch_fixer.py)

fix the pitch of a slicerT instrument (that has BPM sync enabled and the `Granular pitch shifter` effect) when automating the tempo by automating the pitch shifting to the opposite of the pitch change when the sample speed is changing using this equation:

$$\text{pitch shift} = -12 \times \log_2(\frac{\text{new bpm}}{\text{original bpm}})$$

```sh
python pitch_fixer.py -i file.mmpz -o file2.mmpz 
```
<audio src="examples/pitch fixer.mp3">