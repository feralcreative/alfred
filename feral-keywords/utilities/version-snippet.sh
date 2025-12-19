#!/usr/bin/env zsh

# Get the argument passed (the two-digit number)
number="$1"

# Validate that the number consists of exactly two digits
if [[ ! "$number" =~ ^[0-9]{2}$ ]]; then
    echo "Error: Please enter exactly two digits after >> (e.g., >>43)"
    exit 1
fi

# Get current date and time in YYYY.mm.dd.HHMM format
datetime=$(date +"%Y.%m.%d.%H%M")

# Construct the replacement string
replacement="// v00.${number} - ${datetime}"

# Copy the replacement string to the clipboard
echo "$replacement" | pbcopy

# Output the replacement string for the next action
echo "$replacement"

