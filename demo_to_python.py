import subprocess
from subprocess import Popen, PIPE, TimeoutExpired


file_path="output.txt"

f= open("filter.txt","w")

def main():
        def read_data_5s():
                w=open("output.txt", "w")
                result = subprocess.Popen(["sudo", "../bin/demo_ranging_controlee"], stdout=PIPE, stderr=PIPE, text=True)
                try:
                    stdout, stderr = result.communicate(timeout=3)
                except TimeoutExpired:
                    result.kill()
                    stdout, stderr = result.communicate()
                    w.write(stdout)
        def filter(file_path):
            blocks = []
            with open(file_path, "r") as f:
                lines = f.readlines()

            i = 0
            while i < len(lines):
                # Look for the start of a block by finding the "TWR[0].nLos" line
                if "TWR[0].nLos" in lines[i] and "APP" in lines[i]:
                    try:
                        # Extract values from the next four lines
                        nLos_line = lines[i]
                        distance_line = lines[i + 1]
                        aoa_azimuth_line = lines[i + 2]
                        aoa_elevation_line = lines[i + 3]

                        # Split on ':' and take the last part, then strip whitespace
                        nLos_str = nLos_line.split(":")[-1].strip()
                        distance_str = distance_line.split(":")[-1].strip()
                        aoa_azimuth_str = aoa_azimuth_line.split(":")[-1].strip()
                        aoa_elevation_str = aoa_elevation_line.split(":")[-1].strip()

                        # Convert strings to numbers (assuming nLos and distance are integers, others floats)
                        nLos = int(nLos_str)
                        distance = int(distance_str)
                        aoa_azimuth = float(aoa_azimuth_str)
                        aoa_elevation = float(aoa_elevation_str)

                        # Store in a dictionary (you could also store in a list if preferred)
                        block = {
                            "nLos": nLos,
                            "distance": distance,
                            "aoa_azimuth": aoa_azimuth,
                            "aoa_elevation": aoa_elevation
                        }
                        blocks.append(block)
                        # Skip the next 4 lines as they have been processed
                        i += 4
                    except (IndexError, ValueError) as e:
                        # If the block is incomplete or conversion fails, skip the block and continue
                        #print(f"Warning: Skipping incomplete or invalid block starting at line {i}: {e}")
                        i += 1
                else:
                    i += 1
            return blocks, len(blocks)

        #stdout, stderr = process.communicate()
        read_data_5s()
        return filter("output.txt")
