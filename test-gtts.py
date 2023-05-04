from gtts import gTTS
from pydub.playback import play
from pydub import AudioSegment, utils

from io import BytesIO
import subprocess

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

def play_combined_audio():
  # sound 1
  sound1 = AudioSegment.from_file("./eq_displacement.mp3", format="mp3")

  # sound 2
  text = "this is the second audio"
  speech = gTTS(text=text, lang="en", slow=True)
  # Convert the audio data to an in-memory file-like object
  audio_file = BytesIO()
  speech.write_to_fp(audio_file)
  audio_file.seek(0)

  # Load the audio data into pydub
  sound2 = AudioSegment.from_file(audio_file, format='mp3')

  final_audio = sound1 + sound2
  final_audio_path = './final-audio.wav'
  # play(final_audio)
  final_audio.export(final_audio_path, format="wav")
  PLAYER = utils.get_player_name()
  subprocess.call([PLAYER,"-nodisp", "-autoexit", "-hide_banner", final_audio_path], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
  # subprocess.run(['play', '-q', '-t', 'wav', '-'], input=final_audio_path, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)


# play_tts(1, 2)

# play_tts_no_save()

play_combined_audio()