from gtts import gTTS
from pydub.playback import play
from pydub import AudioSegment

# import subprocess

def play_tts(pgd, pga):
  text = ("Peak displacement is %.2f meters" \
                                  + " and peak acceleration is %.2f meters-per-second-squared ") % (pgd, pga)
  speech = gTTS(text=text, lang="en", slow=False)
  filename = "./eq_displacement.mp3"
  print(text)
  speech.save(filename)
  sound = AudioSegment.from_file(filename, format="mp3")
  try:
    play(sound)
  except Exception as e:
    print('Unable to play', filename, e)
  # subprocess.call(["ffmpeg", "-i", filename])

play_tts(1, 2)
