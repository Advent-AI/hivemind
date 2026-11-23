"""Locate a complete normalized quote while retaining original source text."""
from array import array

from hivemind.extraction import GLYPHS, normalise


def build_index(text):
    """Map the normalized, casefolded source back to original character offsets."""
    chars = []
    source_indices = array('Q')
    pending = None
    for offset, character in enumerate(text.translate(GLYPHS)):
        if character.isspace():
            if pending is None:
                pending = offset
            continue
        if pending is not None and chars and chars[-1] not in '([' and character not in ",.;:!?')]":
            chars.append(' ')
            source_indices.append(pending)
        pending = None
        chars.append(character)
        source_indices.append(offset)
    normalized = ''.join(chars).lower()
    if normalized != normalise(text):
        raise ValueError('source normalization mapping differs from the existing normalizer')
    lower_indices = array('Q')
    for character, offset in zip(chars, source_indices):
        lower_indices.extend([offset] * len(character.lower()))
    if len(normalized) != len(lower_indices):
        raise ValueError('source lowercase mapping has inconsistent length')
    folded = normalized.casefold()
    folded_indices = array('Q')
    for character, offset in zip(normalized, lower_indices):
        folded_indices.extend([offset] * len(character.casefold()))
    if len(folded) != len(folded_indices):
        raise ValueError('source casefold mapping has inconsistent length')
    return folded, folded_indices


def find_quote(quote, text, index):
    """Return a complete source slice when every canonical matching slice is identical."""
    target = normalise(quote)
    if not target:
        return None
    search = target.casefold()
    folded, indices = index
    position = 0
    value = None
    while True:
        position = folded.find(search, position)
        if position < 0:
            return value
        span = text[indices[position]:indices[position + len(search) - 1] + 1]
        if normalise(span) == target:
            if value is None:
                value = span
            elif value != span:
                return None
        position += 1
