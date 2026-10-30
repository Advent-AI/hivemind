"""Round 2 for unrelated statements on gpt-6-luna, after the model's own account (luna-probes-2026-10-29/probe_junk.py): the four
keep kinds are defined by form, not by subject. Each arm edits one of those sentences; one shared fresh control on the same
pages; all jobs shuffled in one window (luna_arms.py's machinery with this arm set and its own store).

    python3 luna_arms_round2.py plan | send | sift
"""
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import luna_arms as la  # noqa: E402

la.RUN = HERE / 'luna-arms-round2-2026-10-29'
la.ARMS = {
    # probe j6: Intel's own quarterly results kept as "the company's own figure"
    'J1': {'failure': "another company's own figures kept as kind (1)",
           'edit': ("(1) The company's own figure, guidance or decision:",
                    "(1) A subject company's own figure, guidance or decision (another company's own results are not this kind):"),
           'pages': la.JUNK_PAGES},
    # probe j355: sized benchmark figures pass the reject clause that names only details "without a size"
    'J3': {'failure': 'product and benchmark figures kept because they carry a number',
           'edit': ('a product, game, driver or benchmark detail without a size', 'a product, game, driver or benchmark detail, with or without a figure'),
           'pages': la.JUNK_PAGES},
    # probes j355, j210: any named party's claim qualifies
    'J2': {'failure': "a named party's claims about anything kept as kind (3)",
           'edit': ("(3) A named party's claim or estimate:", "(3) A named party's claim or estimate about a subject company's business or market:"),
           'pages': la.JUNK_PAGES},
    # probe j381: any policy step against any company qualifies
    'J4': {'failure': 'policy steps against other companies kept as kind (4)',
           'edit': ('(4) A policy or regulatory decision or step:',
                    '(4) A policy or regulatory decision or step that bears on what a subject company may sell, to whom or where:'),
           'pages': la.JUNK_PAGES},
}

if __name__ == '__main__':
    {'plan': la.plan, 'send': la.send, 'sift': la.sift}[sys.argv[1]]()
