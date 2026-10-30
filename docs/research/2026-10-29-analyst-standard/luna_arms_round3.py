"""Round 3 on gpt-6-luna (D236): the two sentences rewritten after the generality check, each alone beside one shared fresh
control, all jobs shuffled into one window (luna_arms.py's machinery, its own store).
- J3b: the benchmark sentence in the standard's words (§2: no business scale), narrowed to feature or performance details so a
  trial or regulatory result is not caught, and keeping a competitor's comparison against the company's product (Alex's
  boundary ruling, AMD 100 kW). Guards: two competitor-comparison articles outside the measured sets.
- O: the binding-obligation list per D236 (a stated, not yet completed equity stake; the company's own borrowing excluded).

    python3 luna_arms_round3.py plan | send | sift
"""
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import luna_arms as la  # noqa: E402

la.RUN = HERE / 'luna-arms-round3-2026-10-29'
EXTRA = {'amd0708': 'gnews:1b5a3359dd0644861c0fce42', 'amd0919': 'gnews:bc6460bfdf755efe3b6d2447'}
_ids = la.input_ids
la.input_ids = lambda: dict(_ids(), **EXTRA)

la.ARMS = {
    'J3b': {'failure': 'product and benchmark figures kept because they carry a number (standard §2 wording)',
            'edit': ('a product, game, driver or benchmark detail without a size',
                     "a product, game, driver or benchmark detail about features or performance that gives no business scale "
                     "(units, revenue, customers, capacity), even with a technical figure, unless a competitor sets it against the company's product"),
            'pages': la.JUNK_PAGES + ['amd0708', 'amd0919']},
    'O': {'failure': 'amount questions on completed or unsized stakes and on the company\'s own borrowing (D236)',
          'edit': ("(a guarantee, financing, an equity stake, a purchase commitment, a backstop of customers' capacity or revenue)",
                   "(a guarantee, financing it extends to others, a purchase commitment, a backstop of customers' capacity or revenue, "
                   "or an equity stake whose size is stated and is not yet completed; its own borrowing is not one)"),
          'pages': la.QUESTION_PAGES},
}

la.control_pages = lambda: sorted({p for arm in la.ARMS.values() for p in arm['pages']}, key=str)   # page keys mix call ids and names

if __name__ == '__main__':
    {'plan': la.plan, 'send': la.send, 'sift': la.sift}[sys.argv[1]]()
