import typing as _typing

########################
# Types                #
########################

# Represents a semitone interval (S -> 1, T -> 2)
SemitoneInterval  = int
# Represents a named interval: (Degree, Modifier)
NamedInterval     = _typing.Tuple[int, SemitoneInterval]
# Represents a scale: function from a named interval to a semitone interval
Scale             = _typing.Callable[[NamedInterval], SemitoneInterval]

########################
# Built-in Scales      #
########################

def CyclicScaleFromIntervals(LIST: _typing.List[SemitoneInterval], OCTAVE: SemitoneInterval)->Scale:
  """Generates a cyclic scale from a list of intervals sizes to the starting note.
  As an example, the major scale would be represented as:
  `CyclicScaleFromIntervals([0, 2, 3, 5, 7, 8, 11], 12)`.
  
  To instead define the scale using the distance to the previous interval,
  use `CyclicScaleFromIntervalDistances`.

  Args:
      LIST (List[SemitoneInterval]): List indexed by degree, containing semitones
      OCTAVE (SemitoneInterval): The octave size

  Returns:
      Scale: Cyclic scale of interval 'LIST' and periodicity OCTAVE
  """
  assert sorted(LIST)
  def scale(interval: NamedInterval)->SemitoneInterval:    
    if interval[0] < 0:
      octave = abs(interval[0]) // len(LIST)      
      return LIST[interval[0] % len(LIST)] - octave * OCTAVE + interval[1]
    else:
      octave = interval[0] // len(LIST)
      return LIST[interval[0] % len(LIST)] + octave * OCTAVE + interval[1]
  return scale

def CyclicScaleFromIntervalDistances(LIST: _typing.List[SemitoneInterval])->Scale:
  """Generates a cyclic scale from a list of distances to the previous interval.
  As an example, the major scale would be represented as:
  `CyclicScaleFromIntervalDistances([2, 2, 1, 2, 2, 2, 1])`.
  
  To instead define the scale using the distance to the starting note,
  use `CyclicScaleFromIntervals`.

  Args:
      LIST (List[SemitoneInterval]): List indexed by degree, containing semitones
      OCTAVE (SemitoneInterval): The octave size

  Returns:
      Scale: Cyclic scale of interval 'LIST' and periodicity OCTAVE
  """
  ret = [0]
  sum = 0
  for i in LIST:
    sum += i
    ret.append(ret[-1] + i)
  return CyclicScaleFromIntervals(ret[:-1], sum)

def ChromaticScale(interval: NamedInterval)->SemitoneInterval:
  """The chromatic scale: all the degrees are seperated by a single semitone.

  Args:
      interval (NamedInterval): The interval

  Returns:
      SemitoneInterval: The semitones representing the interval
  """
  return interval[0] + interval[1]

def MajorScale(interval: NamedInterval)->SemitoneInterval:
  """The diatonic major scale: T T S T T T S.

  Args:
      interval (NamedInterval): The interval

  Returns:
      SemitoneInterval: The semitones representing the interval
  """
  return CyclicScaleFromIntervals([0, 2, 4, 5, 7, 9, 11], 12)(interval)
def HarmonicMinorScale(interval: NamedInterval)->SemitoneInterval:
  """The harmonic minor scale: T S T T S TS S.

  Args:
      interval (NamedInterval): The interval

  Returns:
      SemitoneInterval: The semitones representing the interval
  """
  return CyclicScaleFromIntervals([0, 2, 3, 5, 7, 8, 11], 12)(interval)
def MelodicMinorScale(interval: NamedInterval)->SemitoneInterval:
  """The melodic minor scale: T S T T T T S.

  Args:
      interval (NamedInterval): The interval

  Returns:
      SemitoneInterval: The semitones representing the interval
  """
  return CyclicScaleFromIntervals([0, 2, 3, 5, 7, 9, 11], 12)(interval)

########################
# Composable functions #
########################
def SemitoneShift(scale: Scale, by: SemitoneInterval)->Scale:
  """Shifts the result of a scale by 'by' semitones.

  Args:
      scale (Scale): The scale to shift
      by (SemitoneInterval): The number of semitones to shift by

  Returns:
      Scale: The shifted scale
  """
  return lambda x: scale(x) + by

def ModeOf(scale: Scale, mode_number: int)->Scale:
  """Returns the nth mode of a scale, not normalized.
  The scale is not normalized meaning its first degree is not
  guaranteed to return 0.

  Args:
      scale (Scale): The scale whose nth mode to return
      mode_number (int): The mode number (n)

  Returns:
      Scale: The unnormalized nth mode of the scale
  """
  return lambda x: scale((x[0] + mode_number, x[1]))

def NormalizedModeOf(scale: Scale, mode_number: int)->Scale:
  """Returns the nth mode of a scale, normalized.
  In other words, this function does `NormalizedScale(ModeOf(...))`.

  Args:
      scale (Scale): The scale whose nth mode to return
      mode_number (int): The mode number (n)

  Returns:
      Scale: The normalized nth mode of the scale
  """
  return lambda x: scale((x[0] + mode_number, x[1])) - scale((mode_number, 0))

def NormalizedScale(scale: Scale)->Scale:
  """Returns a scale whose first degree evaluates to 0.

  Args:
      scale (Scale): The scale to normalize

  Returns:
      Scale: The normalized scale
  """
  return lambda x: scale(x) - scale((0, 0))

class Intervals:
  ZS = SemitoneInterval(0)
  S  = SemitoneInterval(1)
  T  = SemitoneInterval(2)
  TS = SemitoneInterval(3)
  TT = SemitoneInterval(4)
  
  d1 = (0, -1)
  P1 = (0,  0)
  A1 = (0,  1)

  d2 = (1, -2)
  m2 = (1, -1)
  M2 = (1,  0)
  A2 = (1,  1)
  
  d3 = (2, -2)
  m3 = (2, -1)
  M3 = (2,  0)
  A3 = (2,  1)
  
  d4 = (3, -1)
  P4 = (3,  0)
  A4 = (3,  1)
  
  d5 = (4, -1)
  P5 = (4,  0)
  A5 = (4,  1)
  
  d6 = (5, -2)
  m6 = (5, -1)
  M6 = (5,  0)
  A6 = (5,  1)
  
  d7 = (6, -2)
  m7 = (6, -1)
  M7 = (6,  0)
  A7 = (6,  1)
  
  d8 = (7, -1)
  P8 = (7,  0)
  A8 = (7,  1)