on run
    try
        -- Get the current working directory in Finder using do shell script to get the front window path.
        set currentDirectory to (do shell script "osascript -e 'tell application \"Finder\" to get the POSIX path of (target of window 1 as alias)'")

        -- Define possible suffixes
        set suffixes to {"@2x", "@3x", "@4x", "@100px", "@1920x1080", "@512w"}
        
        -- Create 40 text files in the current directory.
        set filenamesWithSuffix to {}
        
        repeat 40 times
            -- Generate a random filename using words
            set randomName to my generateRandomWordName()
            
            -- Determine if a suffix should be added
            if (count filenamesWithSuffix) < 6 then
                if (random number 1) > 0.85 then
                    -- Append a suffix to this file name
                    set suffix to some item of suffixes
                    set randomName to randomName & suffix
                    set end of filenamesWithSuffix to randomName
                end if
            end if

            -- Set the path for the new file
            set newFilePosix to currentDirectory & randomName & ".txt"
            
            -- Create and write to the new text file
            do shell script "echo 'test' > " & quoted form of newFilePosix
        end repeat
    
        -- Ensure all suffixes are used if not naturally selected
        repeat with remainingSuffix in suffixes
            if (count filenamesWithSuffix) < 6 then
                -- Generate another filename for the remaining suffix
                set randomName to my generateRandomWordName() & remainingSuffix
                set newFilePosix to currentDirectory & randomName & ".txt"
                do shell script "echo 'test' > " & quoted form of newFilePosix
                set end of filenamesWithSuffix to randomName
            end if
        end repeat
    
        display notification "40 text files have been created." with title "File Creation Complete"
    on error errMsg number errNum
        display alert "Error" message errMsg
    end try
end run

-- Helper function to generate a random name using random words.
on generateRandomWordName()
    -- Define a list of random words.
    set wordList to {"apple", "banana", "orange", "grape", "pear", "peach", "melon", "berry", "mango", "kiwi"}
    -- Extend the word list to at least 500 words for more variation.

    set numberOfWords to 5 -- Number of words per filename
    set randomName to ""
    
    -- Loop to generate a random name by combining random words.
    repeat numberOfWords times
        -- Pick a random word from the word list
        set randomWord to some item of wordList
        
        -- Randomize case styles: uppercase or alternating caps
        if (random number 1) > 0.5 then
            set randomWord to my randomizeCase(randomWord) -- Alternating caps
        else
            set randomWord to my allUpperCase(randomWord) -- All uppercase
        end if

        -- Add random accents
        set randomWord to my addRandomAccents(randomWord)

        -- Add separators including doubled or tripled spaces and underscores
        set separatorPool to {" ", "  ", "   ", "_", "__", "___"}
        set randomSeparator to some item of separatorPool

        -- Append the constructed part to build the filename
        set randomName to randomName & randomWord & randomSeparator
    end repeat
    
    -- Remove trailing separator
    set trailingSeparators to {" ", "_"}
    repeat with sep in trailingSeparators
        if randomName ends with sep or randomName ends with (sep & sep) or randomName ends with (sep & sep & sep) then
            set randomName to text 1 through -(1 + (count sep)) of randomName
        end if
    end repeat
    
    return randomName
end generateRandomWordName

-- Helper function to convert a word to all uppercase.
on allUpperCase(inputWord)
    return do shell script "echo " & quoted form of inputWord & " | tr '[:lower:]' '[:upper:]'"
end allUpperCase

-- Helper function to randomize the case of each letter in a word (Alternating Caps).
on randomizeCase(inputWord)
    set randomizedWord to ""
    repeat with i from 1 to (length of inputWord)
        set thisChar to character i of inputWord
        if (i mod 2) is equal to 0 then
            set randomizedWord to randomizedWord & (do shell script "echo " & quoted form of thisChar & " | tr '[:lower:]' '[:upper:]'")
        else
            set randomizedWord to randomizedWord & (do shell script "echo " & quoted form of thisChar & " | tr '[:upper:]' '[:lower:]'")
        end if
    end repeat
    return randomizedWord
end randomizeCase

-- Helper function to add random accents to like characters.
on addRandomAccents(inputWord)
    set accentedMap to {Â
        {"a", "‡", "ˆ", "‰", "‹", "Š"}, Â
        {"e", "Ž", "", "", "‘"}, Â
        {"i", "’", "“", "”", "•"}, Â
        {"o", "—", "˜", "™", "›", "š"}, Â
        {"u", "œ", "", "ž", "Ÿ"}, Â
        {"A", "ç", "Ë", "å", "Ì", "€"}, Â
        {"E", "ƒ", "é", "æ", "è"}, Â
        {"I", "ê", "í", "ë", "ì"}, Â
        {"O", "î", "ñ", "ï", "Í", "…"}, Â
        {"U", "ò", "ô", "ó", "†"}}
    
    set accentedWord to ""
    repeat with i from 1 to (length of inputWord)
        set thisChar to character i of inputWord
        set newChar to thisChar
        
        repeat with accentList in accentedMap
            set baseChar to item 1 of accentList
            if thisChar is equal to baseChar then
                if (random number 1) > 0.7 then
                    set newChar to some item of accentList
                end if
                exit repeat
            end if
        end repeat
        
        set accentedWord to accentedWord & newChar
    end repeat
    return accentedWord
end addRandomAccents
