#!/bin/zsh

# Function to send a notification
function notify() {
    # Use osascript to show a notification
    osascript -e "display notification \"$1\" with title \"$2\""
}

# Notify that the workflow has started
notify "Optimizing images with ImageOptim..." "ImageOptim Processor"

# Get the file paths from the selection
FILES=("$@")

# Path to ImageOptim
IMAGE_OPTIM_PATH="/Applications/ImageOptim.app/Contents/MacOS/ImageOptim"

# Process each file with ImageOptim
for FILE in "${FILES[@]}"; do
    "$IMAGE_OPTIM_PATH" "$FILE"
done

# Notify that the workflow has finished
notify "Image optimization completed!" "ImageOptim Processor"