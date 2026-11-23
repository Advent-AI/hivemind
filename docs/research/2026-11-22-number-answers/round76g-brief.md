# Council round 76g: the slice-2 design, revision 6 (read-only)

You are an independent reviewer. Do not edit any file. The repository is /Users/lchingen/hivemind. Cite file:line.

`docs/research/2026-11-22-number-answers/RELEASE-PAGE.md` is at revision 6. Rounds 76 to 76f each found no leak and no request path.
Their remaining findings were ways the screen check could certify a page the reader cannot fully read: clipping, an extra line,
transparency, a clipping wrapper, the same colour on the same background. Revision 6 answers 76f with three general rules instead of
one patch per trick (AGENTS §1):
- no clipping ancestor;
- a WCAG AA contrast floor for every read text;
- a pinned template, so the screen run certifies one exact template and any change must be re-certified.

The governing documents are the same as in `round76-brief.md`.

## Questions

1. Are the two 76f findings closed, as classes, by the general rules? Name any still open, with its line.
2. Is there any remaining way, within the pinned template (`page == render_page(data)`, byte for byte, with the template's style
   and script hashes fixed in the tests), for the shipped page to leak, make a request, or show the reader something other than the
   frozen screen?
3. **Convergence (AGENTS §1 and §5).** The template is fixed and pinned. An adversarial CSS change can enter only through a template
   change, which fails the pinned hashes. If what remains is a further possible tightening of the screen check against templates
   that cannot ship, list it as optional and give the verdict accordingly.
4. Verdict: ready to build, or not ready with each serious finding.

**Out of scope:**
- the frozen pieces;
- the closed v13s line;
- slice 1's accepted internals;
- the idea path;
- the evidence-summary disagreement;
- wording.
