import sys, os
try:
  from pydub.playback import play
  from pydub import AudioSegment, utils
  pydub_exists = True
  # avoids import error that arises between pydub 0.23.1 and 0.25.1
  global PLAYER
  PLAYER = utils.get_player_name()
  # TEST['d_pydub'][1] = True
except ImportError as e:
  global ERR
  ERR = e
  pydub_exists = False

sound = ''

def load_sound():
    try:
      soundloc = '/Users/jadurani/code/socket-study/doorbell.wav'
      sound = AudioSegment.from_file(soundloc, format="mp3")
      # printM('Loaded %.2f sec alert sound from %s' % (len(sound)/1000., soundloc))
      wavloc = '%s.wav' % os.path.splitext(soundloc)[0]
      if 'ffplay' in PLAYER:
        if not os.path.isfile(wavloc):
          sound.export(wavloc, format="wav")
          print('Wrote wav version of sound file %s' % (wavloc))
      play(sound)
    except FileNotFoundError as e:
      print("Error loading player", e)

load_sound()
