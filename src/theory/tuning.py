from ..theory import scales as _scales
import typing as _typing
import math   as _math

# Represents a tuning system: function from semitones to frequency
TuningSystem = _typing.Callable[[_scales.SemitoneInterval], float]

def EqualTemperamentTuning(zero_semitone_freq: float)->TuningSystem:
  return lambda x: zero_semitone_freq * pow(1.0594630943592953, x)

def JustIntonationTuning(zero_semitone_freq: float)->TuningSystem:
  INTONATION = [1.0, 16/15, 9/8, 6/5, 5/4, 4/3, 45/32, 3/2, 8/5, 5/3, 9/5, 15/8]
  LEN = len(INTONATION)
  def tuning_system(semitone: _scales.SemitoneInterval)->float:
    return zero_semitone_freq * INTONATION[semitone % LEN] * (2**(semitone // LEN))
  return tuning_system