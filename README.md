# TheoryPi
A small python library for musical theory.
## `theory` module
### `theory.scales`
A module containing useful primitives to define and work with scales.
### `theory.tuning`
A module containing useful primitives to calculate frequencies from scales.

## Run code:
The project is still in early development.

For now, a single dependency is needed to output audio: [`pyaudio`](https://pypi.org/project/PyAudio/).
To install it, run:
```
pip install pyaudio
```

To run the code, from the project directory (the parent of `src`) run:
```
python -m src.ui.test
```