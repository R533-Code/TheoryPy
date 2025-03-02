from ..theory import scales
from ..theory import tuning

import typing
import numpy as np
import pyaudio

SAMPLE_RATE = 44100

player = pyaudio.PyAudio()
stream = player.open(
  format=pyaudio.paFloat32, channels=1, rate=SAMPLE_RATE, output=True
)

def generate_sine(frequency: float, duration: float = 1.0, sample_rate: int = SAMPLE_RATE)->np.ndarray[np.float32]:
  num_samples = int(sample_rate * duration)
  t = np.linspace(0, duration, num_samples, endpoint=False)  
  return (np.sin(2 * np.pi * frequency * t)).astype(np.float32)

def fade_in(wave: np.ndarray[np.float32], fade_in_samples: int)->np.ndarray[np.float32]:
  if fade_in_samples == 0:
    return wave
  fade_in_samples = min(fade_in_samples, len(wave))
  fade_in_ = np.linspace(0.0, 1.0, fade_in_samples)
  wave[:fade_in_samples] *= fade_in_
  return wave

def fade_out(wave: np.ndarray[np.float32], fade_out_samples: int)->np.ndarray[np.float32]:
  if fade_out_samples == 0:
    return wave
  fade_out_samples = min(fade_out_samples, len(wave))
  fade_out_ = np.linspace(1, 0, fade_out_samples)
  wave[-fade_out_samples:] *= fade_out_
  return wave

def generate_sines(
  frequencies: typing.List[float], duration: float = 1.0,
  sample_rate: int = SAMPLE_RATE, fade_time: float = 0.05)->np.ndarray[np.float32]:
  assert len(frequencies) > 0
  
  fade_samples = int(SAMPLE_RATE * fade_time)
  SINE_SAMPLE = int(SAMPLE_RATE * duration)
  resulting_wave = np.zeros(SINE_SAMPLE * len(frequencies), dtype=np.float32)
  
  for i in range(0, len(frequencies) - 1):
    resulting_wave[SINE_SAMPLE * i:SINE_SAMPLE * (i + 1) + fade_samples] += fade_out(fade_in(
      generate_sine(frequencies[i], duration + fade_time, sample_rate), fade_samples), fade_samples
    )
  resulting_wave[-SINE_SAMPLE:] += fade_out(fade_in(
    generate_sine(frequencies[-1], duration, sample_rate), fade_samples), fade_samples
  )
  return resulting_wave  

CHORDS = [
  # Lydian
  [tuning.EqualTemperamentTuning(220)(scales.NormalizedModeOf(scales.MajorScale, 3)((i, 0))) for i in range(-7, 1)],
  # Major x3
  [tuning.JustIntonationTuning(220)(scales.MajorScale((i, 0))) for i in range(0, 8)],
  [tuning.MeantoneTemperamentTuning(220)(scales.MajorScale((i, 0))) for i in range(0, 8)],
  [tuning.PythagoreanTuning(220)(scales.MajorScale((i, 0))) for i in range(0, 8)],
]

WAVES = []
for chord in CHORDS:
  WAVES.append(generate_sines(chord, duration=1.0, fade_time=0.2))

wave = WAVES[0]
for i in range(1, len(WAVES)):
  wave += WAVES[i]
wave /= 32.0
stream.write(wave.tobytes())

stream.stop_stream()
stream.close()
player.terminate()