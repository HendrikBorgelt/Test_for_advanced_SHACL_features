import subprocess
import argparse
import time

script_path = "/mnt/d/Users/smhhborg\(D_Laufwerk\)/Documents/GitHub/Test_for_advanced_SHACL_features/shacl-1.4.3-bin/shacl-1.4.3/bin/shaclinfer.sh"
datafile = "/mnt/d/Users/smhhborg\(D_Laufwerk\)/Documents/GitHub/Test_for_advanced_SHACL_features/shacl_sparql_test_data.ttl"
shapefile = "/mnt/d/Users/smhhborg\(D_Laufwerk\)/Documents/GitHub/Test_for_advanced_SHACL_features/shacl_sparql_test_shape.ttl"
outputfile = "shacl_sparql_test_results.txt"

# command = f"wsl {script_path} -datafile {datafile} -shapefile {shapefile} > {outputfile}"
command_0 = "wsl ls -l /mnt/d/Users/smhhborg\(D_Laufwerk\)/Documents/GitHub/Test_for_advanced_SHACL_features/"

try:
    subprocess.run(command_0, shell=True, check=True)
except subprocess.CalledProcessError as e:
    print(f"Command returned non-zero exit status {e.returncode}: {e}")

command = f"wsl {script_path} -datafile {datafile} -shapefile {shapefile} > {outputfile}"
try:
    subprocess.run(command, shell=True, check=True)
    print(f"Output saved to {outputfile}")
except subprocess.CalledProcessError as e:
    print(f"Command returned non-zero exit status {e.returncode}: {e}")

# script_path = "/mnt/d/Users/smhhborg\(D_Laufwerk\)/Documents/GitHub/Test_for_advanced_SHACL_features/shacl-1.4.3-bin/shacl-1.4.3/bin/shaclinfer.sh"
#
# parser = argparse.ArgumentParser(description="Run a shell script in WSL with datafile and shapefile arguments")
# parser.add_argument("-datafile", type=str, required=True, help="Path to the data file")
# parser.add_argument("-shapefile", type=str, required=True, help="Path to the shape file")
#
# # Construct the command
# command = ["wsl", script_path, "-datafile", "/mnt/d/Users/smhhborg\(D_Laufwerk\)/Documents/GitHub/Test_for_advanced_SHACL_features/shacl_sparql_test_data.ttl",
#            "-shapefile", "/mnt/d/Users/smhhborg\(D_Laufwerk\)/Documents/GitHub/Test_for_advanced_SHACL_features/shacl_sparql_test_shape.ttl", ]
# try:
#     result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True, timeout=10)
#
#     # Print the output and any error
#     print("Output:\n", result.stdout)
#     print("Error:\n", result.stderr)
#     print("Return Code:", result.returncode)
# except Exception as e:
#     print(f"An error occurred: {e}")

