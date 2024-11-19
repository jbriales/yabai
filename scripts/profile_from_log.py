#!/usr/bin/env python3
import sys
import plotly.express as px

# Run yabai logging to this file:
# ./bin/yabai -V | tee log
# Then copy to separate file to investigate scoped profiling:
# cp log log_copy


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
  
  try:
    # Split the line by the space character
    parts = line.strip().split(' | ')
    
    # Patching for now while I disabled ts:
    parts = ['NO_TS'] + parts
    
    timestamp_secs = parts[1]
    duration_ms = float(parts[2].rstrip('ms'))
    function_name = parts[3]
    label = parts[4]

    return dict(
      timestamp_secs = timestamp_secs,
      duration_s = duration_ms / 1000,
      function_name = function_name,
      label = label,
      block = f"{function_name} - {label}"
    )
  except Exception as e:
    print(f"Issue parsing line: {line}")
    # Do not raise, just return None
    return None

# def filter_nones(it):
#   if it is not None:
#     yield it

# Open the input file
with open(file_path, 'r') as file:
  entries = [
    parse_profile_line(line) for line in file if line.startswith('PROFILE') and line.endswith("END\n")
  ]

# Print the lines
# for e in entries:
#   print(e)

fig = px.box(entries, x='block', y='duration_s', labels={'block': 'Block', 'duration_ms': 'Duration (s)'})
fig.show()