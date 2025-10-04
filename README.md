# sanitize-filenames.alfredworkflow

This [Alfred](https://www.alfredapp.com/) workflow calls a very simple applescript that sanitizes your filenames for web use by removing special characters and converting to [kebab-case](https://feral.ly/kebab-case).

The script makes the following changes to your selected files:

- Converts filenames to lowercase

- Removes special characters from filenames: `\ * { } ^ : , $ ! = # ( ) % ? " ' ; / \ [ ] ~ |`

- Replaces "&" with "and"

- Replace spaces and underscores with dashes
