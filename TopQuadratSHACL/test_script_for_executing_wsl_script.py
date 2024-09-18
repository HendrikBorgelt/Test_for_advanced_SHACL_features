import subprocess
import argparse


def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Run a shell script in WSL with arguments")
    parser.add_argument("-datafile", type=str, required=True, help="Path to the data file")
    parser.add_argument("-shapefile", type=str, required=True, help="Path to the shape file")

    # Parse the arguments
    args = parser.parse_args()

    # Define the path to your script
    script_path = "/mnt/d/Users/smhhborg\(D_Laufwerk\)/Documents/GitHub/Test_for_advanced_SHACL_features/shacl-1.4.3-bin/shacl-1.4.3/bin/shaclinfer.sh"

    # Construct the command
    command = ["wsl", script_path, "-datafile", args.datafile, "-shapefile", args.shapefile]

    # Use subprocess to run the script with the provided arguments
    try:
        result = subprocess.run(command, shell=True, text=True)

        # Print the output and any error
        print("Output:\n", result.stdout.strip())
        print("Error:\n", result.stderr)
        print("Return Code:", result.returncode)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
