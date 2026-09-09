# OUTPUT UNDER INSTRUCTION V2 (same task, added "always include a usage example")
# 12 lines, runnable, ends with the command to run.


def count_words(path):
    with open(path, encoding="utf-8") as f:
        return len(f.read().split())


if __name__ == "__main__":
    print(count_words("notes.txt"))


# Run it:
#   python output-v2.py
