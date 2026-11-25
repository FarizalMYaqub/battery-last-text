"""The Battery's Last Text to Its Charger — entry program.

The program writes exactly one original line — the phone battery's
last text message to the charger it waited for all day — to
/output/entry.txt and nothing else. The text is a fixed string, so
the program is fully deterministic: every run produces the same
entry the judge reads, byte for byte. No network, no randomness,
no input files.
"""

import os

# The entry itself: one line, plain text, at most 200 characters.
# Texting voice, lowercase, needy then spiteful: the battery waited
# all day at 1%, never got plugged in, and spends its last words
# breaking up with the charger — the punchline lands on the final
# words, "never worth the plug".
TEXT = (
    "hey. it's me, 1%. i waited all day and you never came, so "
    "this is goodbye \u2014 tell the wall i died loyal, and you "
    "were never worth the plug."
)

# Where the judge looks for the entry. Override with ENTRY_OUTPUT.
OUTPUT_PATH = os.environ.get("ENTRY_OUTPUT", "/output/entry.txt")

# The competition gate: UTF-8 text of 1 to 200 characters, one line.
CHAR_LIMIT = 200


def check_text(text):
    """Reject anything the gate or the brief would refuse: blank
    text, more than one line, over the char limit, or not valid
    UTF-8. Returns the text unchanged when it passes."""
    if not text.strip():
        raise ValueError("text is blank")
    if "\n" in text or "\r" in text:
        raise ValueError("text must be a single line")
    if len(text) > CHAR_LIMIT:
        raise ValueError(
            "text is %d chars, over the %d limit" % (len(text), CHAR_LIMIT)
        )
    text.encode("utf-8")
    return text


def save_text(text, path):
    """Write the text to path atomically, then read it straight
    back: a reader must never see a half-written entry, and what
    landed on disk must be exactly the text that was validated."""
    folder = os.path.dirname(path)
    if folder:
        os.makedirs(folder, exist_ok=True)
    tmp_path = path + ".tmp"
    with open(tmp_path, "w", encoding="utf-8") as handle:
        handle.write(text)
    os.replace(tmp_path, path)
    with open(path, "r", encoding="utf-8") as handle:
        written = handle.read()
    if written != text:
        raise ValueError("entry on disk does not match the text")
    return len(written)


def build_entry():
    """Validate the text, then write it. Returns (chars, path)."""
    text = check_text(TEXT)
    count = save_text(text, OUTPUT_PATH)
    return count, OUTPUT_PATH


def main():
    count, path = build_entry()
    print("Wrote entry to %s" % path)


if __name__ == "__main__":
    main()
