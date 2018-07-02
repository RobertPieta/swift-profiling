# Swift Profiling
This repo contains a lightweight tool for running performance tests and generating executables from .swift files. The objective is to allow faster inspection and profiling for swift scripts.

Particularly, swift profiling can be used to profile a swift script linked to different framework versions. For example, the performance tests in `tests` were initially developed to find performance improvements in [swift-core-libs](https://github.com/apple/swift-corelibs-foundation).

# Configuring
Configuration for swift profiling is obtained from the `defaults.cfg` file. To get started, copy `defaults-template.cfg` to `defaults.cfg` with:
`cp defaults-template.cfg defaults.cfg`

Then, modify the `REFERENCE_FRAMEWORK_PATH` and `OPTIMIZED_FRAMEWORK_PATH` to point to the directories containing the reference and optimized builds of the framework you plan to file.

For example, a framework path might be `Users/your_username/Developer/Xcode/DerivedData/Foundation-duhmeclfpxruolgbplsgrnwtmotj/Build/Products/Release` if you are building your framework with Xcode.

For example, the `REFERENCE_FRAMEWORK_PATH` may point to a release build of the `SwiftFoundation` framework built from the master branch. `OPTIMIZED_FRAMEWORK_PATH` may point to a release build of `SwiftFoundation` built from a local branch with performance improvements.

# Running
First, make sure to update the `REFERENCE_FRAMEWORK_PATH` and `OPTIMIZED_FRAMEWORK_PATH` in `profile.py` to point to the reference and optimized framework you are looking to profile.

Then, run the program with `python profile.py`

# Adding Tests
Add performance tests to the `tests` directory, one test per file. Swift profiling will automatically discover tests if the test file matches the `TEST_FILE_PREFIX` and `TEST_FILE_POSTFIX` configuration parameters.

# Report
Running swift profiling generates a `report.txt` with the results of the tests. `report.txt` contains the following format for each performance test:

```
Performance test: test_name.swift
    Reference: 1.00
    New: 2.00
    Speedup: 2.00
```

# Inspection
Swift profiling puts generated executables in the `TEST_EXECUTABLE_DIR` subdirectory. You can use Instruments to profile an executable in detail by pointing Instruments to the executable target. 

This script will copy the reference and optimized frameworks into the respective `executables/optimized` and `executables/reference` folders allowing the scripts to run without further configuration.

# Author
[Robert](https://www.linkedin.com/in/robertpieta) is an engineer, entrepreneur, and co-founder of:

• [Onenigma](https://www.onenigma.com/), achieve business objectives with emerging technology

• [TypingID](https://www.typingid.com/), the user-friendly way to stop account takeover

# License
MIT