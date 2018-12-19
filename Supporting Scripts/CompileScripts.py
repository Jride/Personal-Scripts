import sys
import os
import glob
import subprocess
from pathlib import Path

###################################################################
# Compiles all Python and Swift files and checks for correct syntax
###################################################################

scripts_dir = os.path.abspath(os.path.join(__file__ ,"../.."))

### Compile Python files
python_files_count = 0
for file_name in glob.iglob(scripts_dir + "/**/*.py", recursive=True):
    if file_name == __file__:
        continue

    python_files_count += 1
    result = subprocess.run("python3 -m py_compile \"%s\"" % file_name, shell = True, stderr=subprocess.PIPE).stderr.decode('utf-8')

    if result != None and result != "":
        print("\n")
        print("Error Compiling " + file_name)
        print("\n")
        print(result)
        exit(1)

### Compile Swift files
swift_files_count = 0
for file_name in glob.iglob(scripts_dir + "/**/*.swift", recursive=True):
    if file_name == __file__:
        continue

    swift_files_count += 1
    result = subprocess.run("swiftc -o SwiftTemporaryBuild \"%s\"" % file_name, shell = True, stderr=subprocess.PIPE).stderr.decode('utf-8')

    if os.path.exists("SwiftTemporaryBuild"):
        os.remove("SwiftTemporaryBuild")

    if result != None and result != "":
        if "error" in result:
            print("\n")
            print("Error Compiling " + file_name)
            print("\n")
            print(result)
            exit(1)
        else:
            print("\n")
            print("Warnings Compiling " + file_name)
            print("\n")
            print(result)
        
### Report success
def printFileTypeReport(file_type_name, number):
    if number == 0:
        print("No %s files found" % file_type_name)
    else:
        files = "file" if number == 1 else "files"
        print("%s %s %s compiled successfully" % (number, file_type_name, files))


print("\n")
printFileTypeReport("Python", python_files_count)
printFileTypeReport("Swift", swift_files_count)
print("\n")
