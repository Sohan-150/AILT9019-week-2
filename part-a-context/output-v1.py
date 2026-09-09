# OUTPUT UNDER INSTRUCTION V1 ("You are helping me build a small Python tool.")
# ~40 lines, prose around it, nothing you can copy-paste and run.


def count_words(filepath):
    """Count the number of words in a file.

    This function opens the file at the given path, reads its entire
    contents into memory, splits the text on whitespace, and returns
    the number of resulting tokens. Note that this approach loads the
    whole file at once, which is fine for small files but may not be
    appropriate for very large ones, in which case you would want to
    iterate line by line and accumulate the count instead. Also note
    that punctuation attached to a word (for example a trailing comma)
    will be counted as part of that word, since we are splitting on
    whitespace only.
    """
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()
    words = text.split()
    return len(words)


# No usage example, no command, no __main__ block.
# Left as a library function only.
