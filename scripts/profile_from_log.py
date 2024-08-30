#!/usr/bin/env python3
import sys
import plotly.express as px


# Check if the file path is provided as a command-line argument
# if len(sys.argv) < 2:
  # print("Please provide the file path as a command-line argument.")
  # sys.exit(1)

# Get the file path from the command-line argument
# file_path = sys.argv[1]
file_path = "/Users/jesusbriales/Code/yabai/log_copy"

def parse_profile_line(line):
  # Example line:
  # PROFILE | 1724915018 | 1.9383ms | event_loop_run | loop body

  # Split the line by the space character
  parts = line.strip().split(' | ')

  function_name = parts[3]
  label = parts[4]

  return dict(
    timestamp_secs = parts[1],
    duration_s = float(parts[2].rstrip('ms')) / 1000,
    function_name = function_name,
    label = label,
    block = f"{function_name} - {label}"
  )

# Open the input file
with open(file_path, 'r') as file:
  entries = [
    parse_profile_line(line) for line in file if line.startswith('PROFILE') and line.endswith("END\n")
  ]

# Print the lines
for e in entries:
  print(e)

fig = px.box(entries, x='block', y='duration_s', labels={'block': 'Block', 'duration_ms': 'Duration (s)'})
fig.show()