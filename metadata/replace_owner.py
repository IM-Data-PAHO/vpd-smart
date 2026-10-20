#!/usr/bin/env python3
"""Replace every "lastUpdatedBy" and "createdBy" object and "owner" value with the VPD METADATA user.

Usage: python replace_owner.py file1.json [file2.json ...] or *.json to process all files available
Text is edited in place (formatting preserved) and the result is validated as JSON.
"""

import json
import re
import sys

USER_ID = "PuGe1xoZb0k"

USER_REF_RE = re.compile(r'("(lastUpdatedBy|createdBy)"\s*:\s*)\{[^{}]*\}')
OWNER_RE = re.compile(r'("owner"\s*:\s*)"[^"]*"')


def replace_last_updated(match):
    # Reuse the indentation of the line holding the key
    start = match.string.rfind("\n", 0, match.start()) + 1
    indent = re.match(r"[ \t]*", match.string[start:]).group(0)
    inner = indent + "    "
    return (
        f'{match.group(1)}{{\n'
        f'{inner}"id": "{USER_ID}",\n'
        f'{inner}"code": null,\n'
        f'{inner}"name": "VPD METADATA",\n'
        f'{inner}"displayName": "VPD METADATA",\n'
        f'{inner}"username": "vpd_metadata"\n'
        f'{indent}}}'
    )


ORG_UNITS_RE = re.compile(r'"organisationUnits"\s*:\s*\[')


def empty_organisation_units(text):
    """Empty every "organisationUnits" array, matching brackets outside strings."""
    out, pos, count, removed = [], 0, 0, 0
    for m in ORG_UNITS_RE.finditer(text):
        if m.start() < pos:
            continue
        depth, i, in_str = 1, m.end(), False
        while depth:
            c = text[i]
            if in_str:
                if c == "\\":
                    i += 1
                elif c == '"':
                    in_str = False
            elif c == '"':
                in_str = True
            elif c == "[":
                depth += 1
            elif c == "]":
                depth -= 1
            i += 1
        removed += text.count("{", m.end(), i - 1)
        out.append(text[pos:m.end()] + "]")
        pos = i
        count += 1
    out.append(text[pos:])
    return "".join(out), count, removed


SYSTEM_RE = re.compile(r'\A(\s*\{)\s*"system"\s*:\s*\{[^{}]*\}\s*,')


def process(path):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    counts = {"lastUpdatedBy": 0, "createdBy": 0}

    def repl(match):
        counts[match.group(2)] += 1
        return replace_last_updated(match)

    text = USER_REF_RE.sub(repl, text)
    text, n_ow = OWNER_RE.subn(rf'\1"{USER_ID}"', text)
    text, n_sys = SYSTEM_RE.subn(r"\1", text)
    text, n_ou, n_removed = empty_organisation_units(text)
    json.loads(text)  # fail before writing if the result is invalid
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    print(
        f"{path}: {counts['lastUpdatedBy']} lastUpdatedBy, "
        f"{counts['createdBy']} createdBy, {n_ow} owner replaced, {n_sys} system block deleted, {n_ou} organisationUnits arrays emptied ({n_removed} organisationUnits deleted)"
    )


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    for p in sys.argv[1:]:
        process(p)
