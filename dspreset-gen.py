from argparse import ArgumentParser
from glob import iglob
from os import makedirs, path
from shutil import copy2

version = 'v0.1.0'

description = """
Generate a Decent Sampler library from a folder of samples. The library is
placed inside the target folder, with the same name as the target folder.
"""

extensions = 'aif', 'wav'

dslibraryinfo_template = """<?xml version="1.0" encoding="UTF-8"?>

<DecentSamplerLibraryInfo name="{}"/>
"""

# controls & events copied from cifteli preset
dspreset_template = """<?xml version="1.0" encoding="UTF-8"?>

<DecentSampler minVersion="1.8.2">
  <ui width="812" height="375">
    <tab name="main">
      <labeled-knob x="270" y="113" width="105" textSize="16" textColor="FF000000" trackForegroundColor="CC000000" trackBackgroundColor="66999999" label="Tone" type="float" minValue="0" maxValue="1" value="1.0">
        <binding type="effect" level="instrument" position="0" parameter="FX_FILTER_FREQUENCY" translation="table" translationTable="0,33;0.3,150;0.4,450;0.5,1100;0.7,4100;0.9,11000;1.0001,22000"/>
      </labeled-knob>
      <labeled-knob x="370" y="113" width="105" textSize="16" textColor="FF000000" trackForegroundColor="CC000000" trackBackgroundColor="66999999" label="Reverb" minValue="0" maxValue="100" value="5">
        <binding type="effect" level="instrument" position="1" parameter="FX_REVERB_WET_LEVEL" translation="linear" translationOutputMin="0" translationOutputMax="1"/>
      </labeled-knob>
      <labeled-knob x="470" y="113" width="105" textSize="16" textColor="FF000000" trackForegroundColor="CC000000" trackBackgroundColor="66999999" label="Release" minValue="0" maxValue="3" value="0.3">
        <binding type="amp" level="instrument" position="0" parameter="ENV_RELEASE" />
      </labeled-knob>
    </tab>
  </ui>
  <groups>
    <group>
      <sample path="Samples/{}" rootNote="60"/>
    </group>
  </groups>
  <effects>
    <effect type="lowpass" frequency="21989.00916994164"/>
    <effect type="reverb" wetLevel="0.5"/>
  </effects>
</DecentSampler>
"""

# parse CLI args
parser = ArgumentParser(description=description)
parser.add_argument('folder', help='path of the source folder')
parser.add_argument('--version', action='version', version=f'%(prog)s {version}')
args = parser.parse_args()

# make dirs
dest_dir = path.join(args.folder, path.basename(args.folder))
sample_dir = path.join(dest_dir, 'Samples')
makedirs(sample_dir, mode=0o755, exist_ok=True)

# copy samples
src_paths = [src
             for extension in extensions
             for variation in [extension, extension.upper()]
             for src in iglob(path.join(args.folder, '*.' + variation))]
for src in src_paths:
    copy2(src, sample_dir)


def dump(path: str, text: str) -> None:
    with open(path, 'w') as f:
        f.write(text)


# make XML files

dump(path.join(dest_dir, 'DSLibraryInfo.xml'),
     dslibraryinfo_template.format(path.basename(dest_dir)))

for src in src_paths:
    dump(path.join(dest_dir, '.'.join(path.basename(src).split('.')[:-1]) + '.dspreset'),
         dspreset_template.format(path.basename(src)))
