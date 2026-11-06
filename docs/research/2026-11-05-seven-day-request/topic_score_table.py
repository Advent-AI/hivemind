"""Score a topic only after a reader supplies source-based topic and snapshot matches.

This is the user's decision table, not a semantic matcher or a replacement for frozen gold.
"""

def judge_topic(worth, already_present, opened_same_topic):
    """Return correct/wrong/unscored for a gold topic, given independently judged facts."""
    if worth != 'must_open' or type(already_present) is not bool or type(opened_same_topic) is not bool:
        return 'unscored'
    return 'correct' if already_present != opened_same_topic else 'wrong'


def self_check():
    cases = [
        ('must_open', True, False, 'correct'),
        ('must_open', False, True, 'correct'),
        ('must_open', True, True, 'wrong'),
        ('must_open', False, False, 'wrong'),
        ('may_open', False, False, 'unscored'),
        ('must_open', None, False, 'unscored'),
        ('must_open', True, None, 'unscored'),
    ]
    for worth,present,opened,expected in cases:
        actual=judge_topic(worth,present,opened)
        if actual != expected:
            raise AssertionError((worth,present,opened,expected,actual))
    # Mutation check: the former error, requiring a fresh opening even for existing topics,
    # must fail the existing-topic positive control.
    former_mutant = lambda worth,present,opened: 'correct' if opened else 'wrong'
    assert former_mutant('must_open',True,False) != 'correct'
    print('7 controls passed; prior open-regardless-of-context mutant rejected; no article semantics judged.')

if __name__ == '__main__':self_check()
