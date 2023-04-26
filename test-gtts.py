from gtts import gTTS
from pydub.playback import play
from pydub import AudioSegment

from io import BytesIO
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

def play_tts_no_save():
  text = "I love myself, I am thankful to be alive right now"
  speech = gTTS(text=text, lang="en", slow=True)
  # Convert the audio data to an in-memory file-like object
  audio_file = BytesIO()
  speech.write_to_fp(audio_file)
  audio_file.seek(0)

  # Load the audio data into pydub
  audio_data = AudioSegment.from_file(audio_file, format='mp3')

  # Play the audio
  play(audio_data)

# play_tts(1, 2)

play_tts_no_save()