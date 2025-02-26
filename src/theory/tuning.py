import scales as _scales
import typing as _typing

# Represents a tuning system: function from semitones to frequency
TuningSystem = _typing.Callable[[_scales.SemitoneInterval], float]