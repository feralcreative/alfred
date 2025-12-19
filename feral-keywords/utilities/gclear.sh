#!/usr/bin/env zsh
# Clear Google Drive cache
find ~/Library/Application\ Support/Google/DriveFS -type d -exec test -e '{}'/content_cache \; -exec rm -rf {}/content_cache \;

