The existing assertions retain their intended meaning. The fixture additions supply fields required by the adopted schema, and the two parsing changes read the same JSON payload before the appended closing check.

The new test separately checks the default system message, closing check, and parsed schema against c8. The reported control and two mutant results support that it catches a missing closing check and a dropped final newline; I did not rerun them.

APPROVE