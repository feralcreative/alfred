on run
    try
        tell application "Finder"
            -- Get the currently selected files in Finder.
            set fileList to selection

            -- Loop through each selected file.
            repeat with aFile in fileList
                try
                    set oldName to name of aFile
                    set newName to my sanitizeFilename(oldName)
                    set name of aFile to newName
                on error errMsg number errNum
                    -- Display an alert if there's an error renaming this file
                    display alert "Error renaming file" message errMsg
                end try
            end repeat
        end tell

        -- Notify when the process is complete
        display notification "Filenames have been sanitized." with title "Alfred Workflow"
    on error errMsg number errNum
        -- Display a general error alert
        display alert "General Error" message errMsg
    end try
end run

-- Handler to sanitize the filename.
on sanitizeFilename(fName)
    -- Convert filename to lowercase.
    set fName to my toLowerCase(fName)

    -- Remove accents
    set fName to my removeAccents(fName)

    -- Define a list of special characters you want to remove.
    set specialChars to {"(", ")", "#", "*", "^", "!", "$", "\\", "|", ",", ":", "%", "?", "\"", "'", "~", "/", "=", ";", "{", "}"}

    -- Loop over each special character and remove it from the filename.
    repeat with thisChar in specialChars
        set fName to my replaceText(fName, thisChar, "")
    end repeat

    -- Replace spaces and underscores with dashes.
    set fName to my replaceText(fName, " ", "-")
    set fName to my replaceText(fName, "_", "-")
    
    -- Replace "&" with "and".
    set fName to my replaceText(fName, "&", "and")

    -- Remove duplicate dashes
    set fName to my replaceText(fName, "-----", "-")
    set fName to my replaceText(fName, "----", "-")
    set fName to my replaceText(fName, "---", "-")
    set fName to my replaceText(fName, "--", "-")

    -- Remove any trailing dashes before the file extension
    set fName to my replaceText(fName, "-.", ".")
    set fName to my replaceText(fName, "-@", "@")

    return fName
end sanitizeFilename

-- Handler to replace text in a string.
on replaceText(theText, theSearch, theReplacement)
    -- This function replaces all occurrences of theSearch with the replacement in theText.
    set AppleScript's text item delimiters to theSearch
    set theList to every text item of theText
    set AppleScript's text item delimiters to theReplacement
    set newText to theList as text
    set AppleScript's text item delimiters to ""
    return newText
end replaceText

-- Handler to convert text to lowercase.
on toLowerCase(theText)
    -- This function converts theText to all lowercase letters.
    -- Uses the 'do shell script' command to leverage the shell's 'tr' command.
    set theLowerText to do shell script "echo " & quoted form of theText & " | tr '[:upper:]' '[:lower:]'"
    return theLowerText
end toLowerCase

-- Handler to remove accents from characters.
on removeAccents(theText)
    set accentedChars to "áàâãäåçéèêëíìîïñóòôõöúùûü?ÿ"
    set unaccentedChars to "aaaaaaceeeeiiiinooooouuuuyy"
	
    set newText to ""
    repeat with i from 1 to (length of theText)
        set thisChar to character i of theText
        set accentIndex to offset of thisChar in accentedChars
        if accentIndex is not 0 then
            set thisChar to character accentIndex of unaccentedChars
        end if
        set newText to newText & thisChar
    end repeat
    return newText
end removeAccents