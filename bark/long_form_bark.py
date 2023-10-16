from IPython.display import Audio
import nltk  # we'll use this to split into sentences
nltk.download('punkt')
from scipy.io.wavfile import write as write_wav
import numpy as np
from bark.generation import (
    generate_text_semantic,
    preload_models, SAMPLE_RATE
)
from bark.api import semantic_to_waveform, generate_audio


script = """
These quotes are famous enough to be recognized by most native English speakers. Some come from written English (plays, books, or poems), others come from movies, and still others come from famous figures in history. Any of these can be quoted in a conversation, in whole or in part, They are so famous that the longer quotes are more often referred to with only the first part of the quote because people know the rest.
""".replace("\n", " ").strip()

def long_form_bark(script, SPEAKER="v2/en_speaker_9"):

    sentences = nltk.sent_tokenize(script)
    preload_models()

    silence = np.zeros(int(0.25 * SAMPLE_RATE))  # quarter second of silence
    pieces = []

    for i, (sentence) in enumerate(sentences):
        audio_array = generate_audio(sentence, history_prompt=SPEAKER)
        file_name = f"D:\text_to_speech\bark-tts\long_form_output_{i}.wav"
        write_wav(file_name, SAMPLE_RATE, audio_array)
        pieces += [audio_array, silence.copy()]

    Audio(np.concatenate(pieces), rate=SAMPLE_RATE)


#long_form_bark(script=script, SPEAKER="v2/en_speaker_9")