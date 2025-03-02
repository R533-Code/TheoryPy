from ..theory import scales as _scales
import typing as _typing
import math   as _math

# Represents a tuning system: function from semitones to frequency
TuningSystem = _typing.Callable[[_scales.SemitoneInterval], float]

def EqualTemperamentTuning(zero_semitone_freq: float)->TuningSystem:
  """Generates the standard twelve-tone equal temperament

  Args:
      zero_semitone_freq (float): The frequency of the 0-semitone

  Returns:
      TuningSystem: The standard twelve-tone equal temperament
  """
  # the hardcoded constant is the twelfth root of 2
  return lambda x: zero_semitone_freq * pow(1.0594630943592953, x)

def CyclicTuningFromRatios(ratios: _typing.List[float], cycle_ratio: float, zero_semitone_freq: float)->TuningSystem:
  """Generates a tuning system from ratios.

  Args:
      ratios (_typing.List[float]): The ratios
      cycle_ratio (float): The cycle (or octave) ratio (which is usually 2.0)
      zero_semitone_freq (float): The frequency of the semitone 0

  Returns:
      TuningSystem: A tuning system from ratios
  """
  LEN = len(ratios)
  def tuning_system(semitone: _scales.SemitoneInterval)->float:
    return zero_semitone_freq * ratios[semitone % LEN] * (cycle_ratio**(semitone // LEN))
  return tuning_system

def JustIntonationTuning(zero_semitone_freq: float)->TuningSystem:
  """Generates the just intonation tuning system

  Args:
      zero_semitone_freq (float): The frequency of the semitone 0

  Returns:
      TuningSystem: The just intonation tuning system
  """
  return CyclicTuningFromRatios(
    [1.0, 16/15, 9/8, 6/5, 5/4, 4/3, 45/32, 3/2, 8/5, 5/3, 9/5, 15/8],
    2.0, zero_semitone_freq
  )

def PythagoreanTuning(zero_semitone_freq: float)->TuningSystem:
  """Generates the Pythagorian tuning system

  Args:
      zero_semitone_freq (float): The frequency of the semitone 0

  Returns:
      TuningSystem: The Pythagorean tuning system
  """
  # Ratios from wikipedia
  return CyclicTuningFromRatios(
    [1.0, 256/243, 9/8, 32/27, 81/64, 4/3, 729/512, 3/2, 128/81, 27/16, 16/9, 243/128],
    2.0, zero_semitone_freq
  )

def MeantoneTemperamentTuning(zero_semitone_freq: float)->TuningSystem:
  """Generates the mean temperament tuning system

  Args:
      zero_semitone_freq (float): The frequency of the semitone 0

  Returns:
      TuningSystem: The mean temperament tuning system
  """
  # Ratios from wikipedia
  return CyclicTuningFromRatios(
    [1.0, 1.0449, 1.1180, 1.1963, 1.2500, 1.3375, 1.3975, 1.4953, 1.5625, 1.6719, 1.7889, 1.8692],
    2.0, zero_semitone_freq
  )