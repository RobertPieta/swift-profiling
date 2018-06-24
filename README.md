This repo contains a lightweight tool for running performance tests and generating executables from .swift files. The objective is to allow faster inspection and profiling versus existing options.

# Running
First, make sure to update the `REFERENCE_FRAMEWORK_PATH` and `OPTIMIZED_FRAMEWORK_PATH` in `profile.py` to point to the reference and optimized framework you are looking to profile.

Then, run the program with `python profile.py`

# Inspection
Executables are generated in the `executables` subdirectory. You can use instruments to profile an executable in detail by pointing Instruments to the executable.

# License
MIT