# pip install sounddevice numpy


import numpy as np
import sounddevice as sd
import time

def list_audio_devices():
    """List all audio devices."""
    devices = sd.query_devices()
    for i, device in enumerate(devices):
        print(f"Index {i}: {device['name']} - {device['hostapi']}")

def generate_white_noise(duration_ms, sample_rate=44100):
    """Generate white noise for a given duration in milliseconds."""
    duration_s = duration_ms / 1000.0
    num_samples = int(sample_rate * duration_s)
    # Generate white noise
    noise = np.random.uniform(-1, 1, num_samples)
    return noise

def play_noise(output_device):
    sample_rate = 44100  # Sampling rate in Hz

    while True:
        # Generate random durations
        jamming_duration = np.random.uniform(50, 100)  # in milliseconds
        silent_duration = np.random.uniform(100, 200)  # in milliseconds

        # Generate and play white noise
        noise = generate_white_noise(jamming_duration, sample_rate)
        sd.play(noise, samplerate=sample_rate, device=output_device)
        sd.wait()  # Wait until the sound has finished playing

        # Silent period
        time.sleep(silent_duration / 1000.0)

if __name__ == "__main__":
    print("Available audio devices:")
    list_audio_devices()

    # Ask user to select an audio output device
    output_device = int(input("Please enter the index of the output device you want to use: "))

    play_noise(output_device)
