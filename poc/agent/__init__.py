"""Stack-side harness for the POC (not Hivemind): a sentence lands on a view, an exit condition is kept, an event
is emitted with the evidence when a judgement crosses it, a bet card is rendered. Reads the views database
(read-only); writes only its own database."""
