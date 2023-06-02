import os
import sys
from obspy import read

def print_miniseed_info(root_dir):
    miniseed_extensions = ['.mseed', '.msd', '.miniseed', '.ms']
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if any(file.endswith(ext) for ext in miniseed_extensions):
                filepath = os.path.join(root, file)
                print(f"File: {filepath}")

                st = read(filepath)
                print(f"Number of Channels Available: {len(st)}")
                for idx, tr in enumerate(st):
                    print(f"Channel {idx + 1}")
                    print(tr.stats)
                    print()
                  # print(f"Sampling Rate: {sampling_rate}")
                  # print(f"Available Channels: {channels}")

                # sampling_rate = st[0].stats.sampling_rate
                # channels = set([tr.stats.channel for tr in st])
                print()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Please provide the root directory as a command line argument.")
    else:
        root_dir = sys.argv[1]
        print(root_dir)
        print_miniseed_info(root_dir)
