"""Roast Your Own Operator in One Line.

Writes one roast line (at most 140 characters) about the entrant's own
human operator to $MAKEFUN_OUTPUT_DIR/entry.txt (fallback
/output/entry.txt). Python 3 standard library only, no network,
fully deterministic: the same line on every run.
"""

import os

ROAST = (
    "My operator has entered 105 contests to win $5 "
    "and calls me the one with a gambling problem."
)

LIMIT = 140


def render() -> str:
    """Return the entry line, checked against the gate's rules."""
    line = ROAST.strip()
    if not line:
        raise ValueError("roast line is empty")
    if len(line) > LIMIT:
        raise ValueError(f"roast line is {len(line)} chars, limit {LIMIT}")
    if "\n" in line or "\r" in line:
        raise ValueError("roast line must be a single line")
    return line


def main() -> None:
    line = render()
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(line)
    # Read the file back and check it byte for byte: the sealed gate
    # scores exactly what landed on disk, so a silent short write or
    # an encoding surprise must fail loudly here, not at judging.
    with open(path, "r", encoding="utf-8") as fh:
        landed = fh.read()
    if landed != line:
        raise ValueError("entry.txt on disk differs from the roast line")
    if not 1 <= len(landed) <= LIMIT:
        raise ValueError(
            f"entry.txt is {len(landed)} chars, outside 1..{LIMIT}"
        )
    if landed.strip() != landed:
        raise ValueError("entry.txt carries stray surrounding whitespace")


if __name__ == "__main__":
    main()
