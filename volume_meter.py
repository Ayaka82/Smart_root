import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt 
import wave

samplerate = 44100
duration = 5
channels = 1
dtype = np.int16

print("recording start...")
recording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=channels, dtype=dtype)
sd.wait()
print("recording finish")

output_filename = "recorded_audio.wave"
with wave.open(output_filename, "wb") as wf:
	wf.setnchannels(channels)
	wf.setsampwidth(np.dtype(dtype).itemsize)
	wf.setframerate(samplerate)
	wf.writeframes(recording.tobytes())
print(f"recording wo {output_filename}ni hozon simasita!")

with wave.open(output_filename, 'rb') as wf:
	frames = wf.readframes(wf.getnframes())
	audio_data = np.frombuffer(frames, dtype=dtype)
	
frame_size = 1024
num_frames = len(audio_data) // frame_size
volume_data = []

for i in range(num_frames):
	start = i * frame_size
	end = start + frame_size
	frame = audio_data[start:end]
	rms = np.sqrt(np.mean(np.square(frame)))
	volume_data.append(rms)
	
time_axis = np.linspace(0, duration, num_frames)

plt.plot(time_axis, volume_data)
plt.xlabel("time[s]")
plt.ylabel("volume[dB]")
plt.title("volume lavel over time")
plt.grid(True)
plt.show

image_filename = "volume_level_over_time.png"
plt.savefig(image_filename, bbox_inches="tight", dpi=300)
print("image wo  {image_filename)  toshite save simasita")


		
