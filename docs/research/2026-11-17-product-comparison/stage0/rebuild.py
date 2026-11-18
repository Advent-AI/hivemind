"""Rebuilds every derived file of the reading chain from its primary data, and lists the stored derived files that differ (D675, Codex
round 19). The verdict is a function of the primary data only:
- the run stores (the draws under the run root);
- the readers' own answers: the mapping readers' answers (`map-*.txt`), the third readers' marks (`third/`), the deck's control
  confirmations (`control-confirmations.jsonl`, its last attempt) and the card marks (rounds 0-2, read by `mark_cards.build_readings`);
- the frozen inputs (the matter list, the verdict rule, the census).

Everything else is derived, and is rebuilt here in a temporary folder by the same code that wrote it:
- the eligibility check;
- the libraries and the mapping key;
- the mapping (`mapping.json`);
- the deck key and the card texts.

The deck's reader confirmations are replayed from their record, in the order the deck asks for them. No reader is called: a call that
escapes the replay is refused. The stored files are compared by canonical JSON (sorted keys, so 1 is not true) or by bytes for card
texts."""
import json
import shutil
import tempfile
from pathlib import Path


def canonical(path):
    return json.dumps(json.loads(Path(path).read_text()), sort_keys=True, ensure_ascii=False)


def replay(record_path):
    """The deck's confirmation step, answered from the last recorded attempt in the order the deck asks."""
    lines = [line for line in Path(record_path).read_text().splitlines() if line.strip()]
    recorded = iter(json.loads(lines[-1])['attempt']) if lines else iter(())

    def confirmed(card_text, supported):
        entry = next(recorded, None)
        role = 'supported control' if supported else 'plant'
        if entry is None or entry.get('role') != role:
            raise SystemExit('refused: the recorded control confirmations do not match the deck the inputs rebuild')
        return entry['admitted'], entry['mark']
    confirmed.remaining = lambda: sum(1 for _ in recorded)
    return confirmed


def differences(run_root, mapping_out, deck_folder, key_folder):
    """The derived files whose stored content differs from what the primary data rebuild (an empty list when every one matches)."""
    import census_readers
    import eligibility
    import mapping
    import mark_cards
    mapping_out, deck_folder, key_folder = Path(mapping_out), Path(deck_folder), Path(key_folder)
    saved = (mapping.KEY_FOLDER, mark_cards.KEY, mark_cards.confirmed_by_reader, census_readers.run)

    def no_reader(family, prompt):
        raise SystemExit('refused: a rebuild never calls a reader')
    with tempfile.TemporaryDirectory() as scratch:
        scratch = Path(scratch)
        keys, out, deck = scratch / 'keys', scratch / 'mapping-out', scratch / 'deck'
        confirmed = replay(key_folder / 'control-confirmations.jsonl')
        try:
            mapping.KEY_FOLDER = keys                               # mark_cards reads the same module's KEY_FOLDER
            mark_cards.KEY = keys / 'deck-key.json'
            census_readers.run = no_reader
            mark_cards.confirmed_by_reader = confirmed
            eligibility.write(eligibility.check(run_root), scratch / 'eligibility.json')
            mapping.export(run_root, out, scratch / 'eligibility.json')
            for answer in mapping_out.glob('map-L*-*.txt'):
                shutil.copy2(answer, out / answer.name)
            if (mapping_out / 'third').is_dir():
                shutil.copytree(mapping_out / 'third', out / 'third')
            mapping.result(out)
            mark_cards.deck(out, deck)
            if confirmed.remaining():
                raise SystemExit('refused: the recorded control confirmations hold more than the deck the inputs rebuild asks for')
        finally:
            mapping.KEY_FOLDER, mark_cards.KEY, mark_cards.confirmed_by_reader, census_readers.run = saved
        differ = []
        json_pairs = [(out / 'eligibility.json', mapping_out / 'eligibility.json'), (out / 'mapping.json', mapping_out / 'mapping.json'),
                      (keys / 'mapping-key.json', key_folder / 'mapping-key.json'), (keys / 'deck-key.json', key_folder / 'deck-key.json')]
        json_pairs += [(p, mapping_out / p.name) for p in sorted(out.glob('library-L*.json'))]
        for rebuilt, stored in json_pairs:
            if not stored.exists() or canonical(rebuilt) != canonical(stored):
                differ.append(str(stored))
        if {p.name for p in mapping_out.glob('library-L*.json')} != {p.name for p in out.glob('library-L*.json')}:
            differ.append(f'{mapping_out}/library-L*.json (a different set of libraries)')
        rebuilt_cards = {p.name: p.read_bytes() for p in deck.glob('C*.txt')}
        stored_cards = {p.name: p.read_bytes() for p in deck_folder.glob('C*.txt')}
        differ += [str(deck_folder / name) for name in sorted(set(rebuilt_cards) | set(stored_cards))
                   if rebuilt_cards.get(name) != stored_cards.get(name)]
        return differ
