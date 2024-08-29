#!/usr/bin/env python3
import sys


# Check if the file path is provided as a command-line argument
# if len(sys.argv) < 2:
  # print("Please provide the file path as a command-line argument.")
  # sys.exit(1)

# Get the file path from the command-line argument
# file_path = sys.argv[1]
file_path = "/Users/jesusbriales/Code/yabai/log"

def parse_profile_line(line):
  # Example line:
  # PROFILE | 1724915018 | 1.9383ms | event_loop_run | loop body

  # Split the line by the space character
  parts = line.strip().split(' | ')

  return dict(
    timestamp_secs = parts[1],
    duration_ms = float(parts[2].rstrip('ms')),
    function_name = parts[3],
    label = parts[4]
  )

# Open the input file
with open(file_path, 'r') as file:
  entries = [
    parse_profile_line(line) for line in file if line.startswith('PROFILE')
  ]

# Print the lines
for e in entries:
  print(e)

# # Extract the function names and duration values
# function_names = [e['function_name'] for e in entries]
# durations = [e['duration_ms'] for e in entries]

# # Create a boxplot
# plt.boxplot(durations, labels=function_names)
# plt.xlabel('Function Name')
# plt.ylabel('Duration (ms)')
# plt.title('Boxplot of Duration per Function Name')
# plt.show()