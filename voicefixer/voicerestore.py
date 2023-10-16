from voicefixer import VoiceFixer
import os
import ffmpeg
import wave
import numpy
import subprocess
from bark import SAMPLE_RATE, generate_audio, preload_models, save_as_prompt
from scipy.io.wavfile import write as write_wav

vf = VoiceFixer()

def restore_voice_chunks (pt_in: str, pt_out_chunk: str, wav_out: str, m = 2):
    """
    pt_in: folder path to input audio chunks
    pt_out: path to output audio
    m: mode of restoration
    """
    chunks = os.scandir(pt_in)
    for i, chunk in enumerate(chunks):
        vf.restore(input = chunk.path, output = f"{pt_out_chunk}/out_{i}.wav", mode = m)

        os.remove(chunk.path)
    
    inputs = []
    chunks = os.scandir(pt_out_chunk)
    for chunk in chunks:
        inputs.append(chunk.path)

    # List of input .wav files to concatenate
    input_files = inputs

    # Output file name
    output_file = wav_out

    # Build the FFmpeg command
    ffmpeg_command = [
        "ffmpeg",
        *sum([["-i", file] for file in input_files], []),  # Flatten the list of input files
        "-filter_complex",
        f"[0:a]{''.join([f'[{i}:a]' for i in range(1, len(input_files))])}concat=n={len(input_files)}:v=0:a=1[outa]",
        "-map",
        "[outa]",
        output_file,
    ]

    # Run the FFmpeg command
    subprocess.run(ffmpeg_command)

    print("Concatenation complete.")

    remove_chunks = os.scandir(pt_out_chunk)
    for chunk in remove_chunks:
        os.remove(chunk.path)
#restore_voice_chunks(r"./voicefixer/input", r"./voicefixer/output",r"./output.wav", m = 2) #test function