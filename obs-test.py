import obspy
import numpy as np

'''
TRIGGERED
2023-05-17 02:37:15 [Processor] Max PGA Values (Acceleration (m/s$^2$))
{
    "ENE": 0.011891705588669957,
    "ENN": 5657.48357826317,
    "ENZ": 5657.480782259755
}
2023-05-17 02:37:15 [Processor] Signal deconvolution set to DISP
2023-05-17 02:37:15 [Processor] Alert stream units are displacement (m)
2023-05-17 02:37:15 [Processor] Deconv Channel: DISP     Units: Displacement (m)
2023-05-17 02:37:15 [Processor] Max PGD Values (Displacement (m))
{
    "ENE": 4.06369070205492e-05,
    "ENN": 55.20254009397969,
    "ENZ": 55.2025469241524
}
{
    "floor_num": 8,
    "event_time": "2023-05-17T02:37:15.30Z",
    "axis_with_max_drift": "z",
    "acceleration": {
        "x": 0.011891705588669957,
        "y": 5657.48357826317,
        "z": 5657.480782259755
    },
    "displacement": {
        "x": 4.06369070205492e-05,
        "y": 55.20254009397969,
        "z": 55.2025469241524
    },
    "intensity": {
        "x": "I",
        "y": "X+",
        "z": "X+"
    },
    "drift": {
        "x": 0.0020318453510274597,
        "y": 2760.1270046989844,
        "z": 2760.12734620762
    },
    "over_drift_thresh": {
        "x": false,
        "y": true,
        "z": true
    }
}
'''

stream = [
  ['EHZ', 1684291035.313, 478406, 93276, 293724, 51653, 138622, 15407, 15178, -31014, -74374, -85504, -133682, -139356, -175930, -186945, -211692, -224979, -240612, -252791, -263164, -273019, -281533, -287876, -293554, -298624, -301442],
  ['ENN', 1684291035.313, -278104, -445287, -489067, -502289, -487139, -500876, -488428, -501749, -493884, -497647, -494357, -492132, -493823, -495797, -492239, -494641, -496915, -495805, -495060, -494764, -495687, -497559, -496481, -493395, -493205],
  ['ENZ', 1684291035.313, 3390879, 3459204, 3451986, 3420112, 3472224, 3413988, 3466424, 3421814, 3455059, 3434320, 3447924, 3440650, 3443303, 3442080, 3443664, 3442998, 3440775, 3441493, 3441334, 3442053, 3442564, 3441176, 3440477, 3440582, 3443123],
  ['ENE', 1684291035.313, -144526, -494065, -277963, -367751, -330370, -328836, -353493, -323347, -354485, -327598, -344716, -328785, -339004, -334232, -337232, -337285, -339470, -336225, -338558, -337831, -336275, -338446, -337172, -337347, -334539]
]


def get_trace(chan):
  # found_channel = next((st for st in stream if chan in st), None)
  found_channel = next((st for st in stream if chan == st[0]), None)
  if not found_channel:
    return None

  # l = list(found_channel)
  l = found_channel
  # print(l)
  timestamp = l[1]
  data = np.array(l[2:])

  # Create a new Trace object
  trace = obspy.Trace(data)

  # print(timestamp)
  # Set the sample rate and start time
  trace.stats.sampling_rate = 100.0  # Set the sample rate to 100 Hz
  trace.stats.starttime = obspy.UTCDateTime(timestamp)  # Set the start time
  return trace

def get_disp(trace):
  # First integration to get velocity (where trace.data is acceleration data from our accelerometers)
  vel_data = np.cumsum(trace.data)
  # Second integration to get displacement
  disp_data = np.cumsum(vel_data)
  # re-assign to trace data
  trace.data = disp_data
  trace.detrend(type='linear')
  return trace

def get_max_data():
  channels = ['ENN', 'ENZ', 'ENE']
  for ch in channels:
    tr = get_trace(ch)
    tr_disp = get_disp(tr)
    pgd = max(abs(tr_disp.data))
    print('%s max disp: %f' % (ch, pgd))

get_max_data()