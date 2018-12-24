#! /usr/bin/env python3

####################################################################################################

import pathlib
import yaml

####################################################################################################

dst_path = pathlib.Path(__file__).parent

####################################################################################################

def split_columns(*columns):
    return zip(*[x.strip().split('\n') for x in columns])

def write_yaml(filename, data):
    dst_file = dst_path.joinpath(filename)
    yaml_data = yaml.dump(data, default_flow_style=False)
    with (open(dst_file, 'w')) as fh:
        fh.write(yaml_data)
    print('Dumped', dst_file)

####################################################################################################

# cf. Table 2. Default Parameter File

parameters = '''
5161
5162
5163
5164
5165
5166
5181
5182
5183
5184
5185
5186
5211
5212
5213
5214
5215
5216
5220
5221
5222
5223
5224
5225
5226
5241
5242
5243
5244
5245
5246
5261
5262
5263
5264
5265
5266
5281
5282
5283
5284
5285
5286
5301
5302
5303
5304
5305
5306
5321
5322
5323
5324
5325
5326
5341
5342
5343
5344
5345
5346
5361
5362
5363
5364
5365
5366
5381
5382
5383
5384
5385
5386
'''

values = '''
0.0
0.0
0.0
0.0
0.0
0.0
0.0
0.0
0.0
0.0
0.0
0.0
0.0
0.0
0.0
0.0
0.0
0.0
1.0
0.0
0.0
0.0
0.0
0.0
0.0
0.0
0.0
0.0
0.0
0.0
0.0
0.0
0.0
0.0
0.0
0.0
0.0
0.0
0.0
0.0
0.0
0.0
0.0
0.0
0.0
0.0
0.0
0.0
0.0
0.0
0.0
0.0
0.0
0.0
0.0
0.0
0.0
0.0
0.0
0.0
0.0
0.0
0.0
0.0
0.0
0.0
0.0
0.0
0.0
0.0
0.0
0.0
0.0
'''

comments = '''
G28 home X
G28 home Y
G28 home Z
G28 home A
G28 home B
G28 home C
G30 home X
G30 home Y
G30 home Z
G30 home A
G30 home B
G30 home C
G92 offset X
G92 offset Y
G92 offset Z
G92 offset A
G92 offset B
G92 offset C
coord. system number
coord. system 1 X
coord. system 1 Y
coord. system 1 Z
coord. system 1 A
coord. system 1 B
coord. system 1 C
coord. system 2 X
coord. system 2 Y
coord. system 2 Z
coord. system 2 A
coord. system 2 B
coord. system 2 C
coord. system 3 X
coord. system 3 Y
coord. system 3 Z
coord. system 3 A
coord. system 3 B
coord. system 3 C
coord. system 4 X
coord. system 4 Y
coord. system 4 Z
coord. system 4 A
coord. system 4 B
coord. system 4 C
coord. system 5 X
coord. system 5 Y
coord. system 5 Z
coord. system 5 A
coord. system 5 B
coord. system 5 C
coord. system 6 X
coord. system 6 Y
coord. system 6 Z
coord. system 6 A
coord. system 6 B
coord. system 6 C
coord. system 7 X
coord. system 7 Y
coord. system 7 Z
coord. system 7 A
coord. system 7 B
coord. system 7 C
coord. system 8 X
coord. system 8 Y
coord. system 8 Z
coord. system 8 A
coord. system 8 B
coord. system 8 C
coord. system 9 X
coord. system 9 Y
coord. system 9 Z
coord. system 9 A
coord. system 9 B
coord. system 9 C
'''

####################################################################################################

data = {}
for parameter, value, comment in split_columns(parameters, values, comments):
    comment = comment.replace('coord.', 'coordinate')
    data[int(parameter)] = dict(value=float(value), meaning=comment)
write_yaml('rs274-default-parameter-file.yaml', data)

####################################################################################################

# Table 3. Word-starting Letters

letters = '''
A
B
C
D
F
G
H
I
J
K
L
M
N
P
Q
R
S
T
X
Y
Z
'''

meanings = '''
A-axis of machine
B-axis of machine
C-axis of machine
tool radius compensation number
feedrate
general function (see Table 5)
tool length offset index
X-axis offset for arcs / X offset in G87 canned cycle
Y-axis offset for arcs / Y offset in G87 canned cycle
Z-axis offset for arcs / Z offset in G87 canned cycle
number of repetitions in canned cycles / key used with G10
miscellaneous function (see Table 7)
line number
dwell time in canned cycles / dwell time with G4 / key used with G10
feed increment in G83 canned cycle
arc radius
canned cycle plane / spindle speed
tool selection
X-axis of machine
Y-axis of machine
Z-axis of machine
'''

####################################################################################################

data = {}
for letter, meaning in split_columns(letters, meanings):
    data[letter] = dict(meaning=meaning)
write_yaml('rs274-word-starting-letter.yaml', data)

####################################################################################################

# Table 5. G Codes
# Table 7. M Codes
# 3.7 Other Input Codes

gcodes = '''
G0
G1
G2
G3
G4
G10
G17
G18
G19
G20
G21
G28
G30
G38.2
G40
G41
G42
G43
G49
G53
G54
G55
G56
G57
G58
G59
G59.1
G59.2
G59.3
G61
G61.1
G64
G80
G81
G82
G83
G84
G85
G86
G87
G88
G89
G90
G91
G92
G92.1
G92.2
G92.3
G93
G94
G98
G99
M0
M1
M2
M3
M4
M5
M6
M7
M8
M9
M30
M48
M49
M60
F
S
T
'''

meanings = '''
rapid positioning
linear interpolation
circular/helical interpolation (clockwise)
circular/helical interpolation (counterclockwise)
dwell
coordinate system origin setting
XY-plane selection
XZ-plane selection
YZ-plane selection
inch system selection
millimeter system selection
return to home
return to secondary home
straight probe
cancel cutter radius compensation
start cutter radius compensation left
start cutter radius compensation right
tool length offset (plus)
cancel tool length offset
motion in machine coordinate system
use preset work coordinate system 1
use preset work coordinate system 2
use preset work coordinate system 3
use preset work coordinate system 4
use preset work coordinate system 5
use preset work coordinate system 6
use preset work coordinate system 7
use preset work coordinate system 8
use preset work coordinate system 9
set path control mode: exact path
set path control mode: exact stop
set path control mode: continuous
cancel motion mode (including any canned cycle)
canned cycle: drilling
canned cycle: drilling with dwell
canned cycle: peck drilling
canned cycle: right hand tapping
canned cycle: boring, no dwell, feed out
canned cycle: boring, spindle stop, rapid out
canned cycle: back boring
canned cycle: boring, spindle stop, manual out
canned cycle: boring, dwell, feed out
absolute distance mode
incremental distance mode
offset coordinate systems and set parameters
cancel offset coordinate systems and set parameters to zero
cancel offset coordinate systems but do not reset parameters
apply parameters to offset coordinate systems
inverse time feed rate mode
units per minute feed rate mode
initial level return in canned cycles
R-point level return in canned cycles
program stop
optional program stop
program end
turn spindle clockwise
turn spindle counterclockwise
stop spindle turning
tool change
mist coolant on
flood coolant on
mist and flood coolant off
program end, pallet shuttle, and reset
enable speed and feed overrides
disable speed and feed overrides
pallet shuttle and program stop
set feed rate
set spindle speed
select tool
'''

####################################################################################################

data = {}
for gcode, meaning in split_columns(gcodes, meanings):
    data[gcode] = dict(meaning=meaning)
write_yaml('rs274-gcodes.yaml', data)
