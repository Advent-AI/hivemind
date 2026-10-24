No remaining serious finding in the amended tables within this isolated experiment.

For example, if `e2` merges into `e1`, an association citing `e2` must follow `e2 → e1 → persistent evidence ID`; merging alone no longer makes the association fail.

The tables now distinguish merging from rejection, require accepted evidence to have actually been saved, preserve candidate-to-final viewpoint mapping, and cover rollback and replay. The added test explicitly covers an association referencing the evidence ID removed by merging.

This is a design-only conclusion; implementation and test results remain unverified.