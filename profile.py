
import os
import timeit
import subprocess

# Directory to contain generated executables
TEST_EXECUTABLE_DIR = "./executables"

# Filename prefix and postfix used to determine if a file is a test file
TEST_FILE_PREFIX = "test_"
TEST_FILE_POSTFIX = ".swift"

# Name of the framework
FRAMEWORK_NAME = "SwiftFoundation"

# The REFERENCE_SWIFT_FOUNDATION_PATH provides the path to the SwiftFoundation.framework baseline for time profiling
# Path to the directory containing the SwiftFoundation.framework, Release build
REFERENCE_FRAMEWORK_PATH = "/Users/Onenigma/Library/Developer/Xcode/DerivedData/Foundation-ggmfmobbfygwlnbglyxwneaxfkgi/Build/Products/Release"
REFERENCE_EXECUTABLE_SUBDIRECTORY = "reference"

# The OPTIMIZED_SWIFT_FOUNDATION_PATH provides the path to the new SwiftFoundation.framework to compare
# Path to the directory containing the SwiftFoundation.framework, Release build
OPTIMIZED_FRAMEWORK_PATH = "/Users/Onenigma/Library/Developer/Xcode/DerivedData/Foundation-duhmeclfpxruolgbplsgrnwtmotj/Build/Products/Release"
OPTIMIZED_EXECUTABLE_SUBDIRECTORY = "optimized"

# File name and path for the generated report file, containing the results of the profiling tests
REPORT_PATH = "./"
REPORT_NAME = "report.txt"

# The number of iterations a test performs
TEST_ITERATIONS = 25

# Discover all test files
test_files = [f for f in os.listdir(".") if os.path.isfile(f) and f.startswith(TEST_FILE_PREFIX) and f.endswith(TEST_FILE_POSTFIX)]

# Create the executable directories
reference_executable_path = os.path.join(*[TEST_EXECUTABLE_DIR, REFERENCE_EXECUTABLE_SUBDIRECTORY])
if not os.path.exists(reference_executable_path):
	os.mkdir(reference_executable_path)

optimized_executable_path = os.path.join(*[TEST_EXECUTABLE_DIR, OPTIMIZED_EXECUTABLE_SUBDIRECTORY])
if not os.path.exists(optimized_executable_path):
	os.mkdir(optimized_executable_path)

# Copy the framework into the executable directories
os.system("rm -rf {}.framework".format(
	os.path.join(reference_executable_path, FRAMEWORK_NAME)
))

os.system("cp -a {}.framework {}.framework".format(
	os.path.join(REFERENCE_FRAMEWORK_PATH, FRAMEWORK_NAME),
	os.path.join(reference_executable_path, FRAMEWORK_NAME)
))

os.system("rm -rf {}.framework".format(
	os.path.join(optimized_executable_path, FRAMEWORK_NAME)
))

os.system("cp -a {}.framework {}.framework".format(
	os.path.join(OPTIMIZED_FRAMEWORK_PATH, FRAMEWORK_NAME),
	os.path.join(optimized_executable_path, FRAMEWORK_NAME)
))

# Define the process for executing a test
def test_executable_path(test_name, test_extension):
	return os.path.join(*[TEST_EXECUTABLE_DIR, test_extension, test_name])

def create_compile_command(test_name, file_name, swift_foundation_path, test_path):
	return [
		#
		"swiftc", "-O", "-whole-module-optimization", 

		# Link the SwiftFoundation.framework
		"-F", swift_foundation_path,

		# The output executable name
		"-o", test_path, 

		# The file that will be compiled
		filename,

		# Link the -rpath and -@executable_path to the compiler
		"-Xlinker", "-rpath", "-Xlinker", "@executable_path/", 
	]

def time_process_execution(run_command):
	assert TEST_ITERATIONS > 0, "The number of test iterations must be greater than 0"

	# Time the run command for a number of TEST_ITERATIONS
	time = timeit.timeit(
		stmt = "subprocess.call({})".format(run_command), 
		setup = "import subprocess;",
		number = TEST_ITERATIONS
	)

	# Return the average time for each iteration
	return time / TEST_ITERATIONS

def execute_test_file(filename, swift_foundation_path, test_extension):
	test_name = "{}.exec.{}".format(filename, test_extension)
	test_path = test_executable_path(test_name, test_extension)

	# Compile the executable
	compile_command = create_compile_command(test_name, filename, swift_foundation_path, test_path)
	subprocess.call(compile_command)

	# Runs the executable
	run_command = [
		"{}".format(test_path)
	]

	return time_process_execution(run_command)

# Define the report 
report = {}

# For each test file, run reference and swift capturing run time
for filename in test_files:
	print("Profiling: {}".format(filename))

	print("\t- reference")
	reference = execute_test_file(filename, REFERENCE_FRAMEWORK_PATH, REFERENCE_EXECUTABLE_SUBDIRECTORY)
	print("\t\t{}".format(reference))

	print("\t- optimized")
	optimized = execute_test_file(filename, OPTIMIZED_FRAMEWORK_PATH, OPTIMIZED_EXECUTABLE_SUBDIRECTORY)
	print("\t\t{}".format(optimized))

	report[filename] = {
		'reference': reference,
		'optimized': optimized
	}

# Create a report with each test name, run times, and speedup
report_text = ""

# For each file and result append the report status
for (filename, results) in sorted(report.items(), key=lambda x: x[0]):
	result_text = "Performance test: {}\n\tReference: {}\n\tNew: {}\n\tSpeedup: {}\n".format(
		filename,
		results['reference'],
		results['optimized'],
		results['reference'] / results['optimized'] if results['optimized'] != 0 else 0
	)

	report_text += result_text + "\n"

# Write the report to the REPORT_PATH
with open(os.path.join(REPORT_PATH, REPORT_NAME), "w") as report_file:
	report_file.write(report_text)
