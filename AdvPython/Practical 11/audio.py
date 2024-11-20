import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import resample
import soundfile as sf  # To save audio files

# 1. Audio Loading and Visualization
def load_audio(file_path):
    audio, sr = librosa.load(file_path, sr=None)
    return audio, sr

def visualize_waveform(audio, sr):
    plt.figure(figsize=(10, 4))
    librosa.display.waveshow(audio, sr=sr)
    plt.title("Audio Waveform")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.show()

# 2. Audio Manipulation Operations

# a. Change Playback Speed (Resampling method)
def change_speed_resample(audio, sr, speed_factor):
    num_samples = int(len(audio) / speed_factor)
    return resample(audio, num_samples)

# b. Apply Echo Effect
def apply_echo(audio, sr, delay_ms, decay_factor=0.5):
    delay_samples = int(delay_ms * sr / 1000)
    echo_audio = np.zeros_like(audio)
    echo_audio[delay_samples:] = audio[:-delay_samples]
    echo_audio += decay_factor * audio
    return echo_audio

# c. Clip Audio
def clip_audio(audio, sr, start_time, end_time):
    start_sample = int(start_time * sr)
    end_sample = int(end_time * sr)
    return audio[start_sample:end_sample]

# 3. Spectral Analysis
def plot_spectrogram(audio, sr):
    D = librosa.amplitude_to_db(np.abs(librosa.stft(audio)), ref=np.max)
    plt.figure(figsize=(12, 6))
    librosa.display.specshow(D, sr=sr, x_axis='time', y_axis='log')
    plt.title("Spectrogram")
    plt.colorbar(format="%+2.0f dB")
    plt.show()

# Save the manipulated audio to a new file
def save_audio(audio, sr, filename):
    sf.write(filename, audio, sr)
    print(f"Audio saved as {filename}")

# Command-Line Menu for Interactive User Selection
def cli_menu():
    file_path = input("Enter the path of the audio file: ")
    audio, sr = load_audio(file_path)

    while True:
        print("\nSelect an option:")
        print("1. Change Playback Speed")
        print("2. Apply Echo Effect")
        print("3. Clip Audio")
        print("4. Show Spectrogram")
        print("5. Visualize Waveform")
        print("6. Exit")

        choice = input("Enter choice (1-6): ")

        if choice == '1':
            speed_factor = float(input("Enter playback speed factor (e.g., 1.0 for normal, 0.5 for half-speed): "))
            audio = change_speed_resample(audio, sr, speed_factor)
            print(f"Playback speed changed to {speed_factor}x")
            save_audio(audio, sr, "edited_audio_speed.wav")

        elif choice == '2':
            delay_ms = float(input("Enter echo delay in milliseconds (e.g., 300 for 300 ms): "))
            audio = apply_echo(audio, sr, delay_ms)
            print(f"Echo effect applied with {delay_ms} ms delay")
            save_audio(audio, sr, "edited_audio_echo.wav")

        elif choice == '3':
            start_time = float(input("Enter start time in seconds: "))
            end_time = float(input("Enter end time in seconds: "))
            audio = clip_audio(audio, sr, start_time, end_time)
            print(f"Audio clipped from {start_time}s to {end_time}s")
            save_audio(audio, sr, "edited_audio_clip.wav")

        elif choice == '4':
            plot_spectrogram(audio, sr)
            print("Spectrogram displayed")

        elif choice == '5':
            visualize_waveform(audio, sr)
            print("Waveform visualized")

        elif choice == '6':
            print("Exiting...")
            break
        else:
            print("Invalid choice, please try again.")

# Main program entry point
if __name__ == "__main__":
    cli_menu()
