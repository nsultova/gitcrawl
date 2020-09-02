# TODOs

How to implement my various manual tests in an automated way?

### Thoughts:

* how to test the code-flow as it heavily relies on interaction?
* * test --leave-me alone flag on basic example
* * test custom functions
* some of the functions deal with network access, thus testing might be cumbersome
* * one might be able to test the logic on a local custom-made conda repository
* * ..or mirroring the side and routing the traffic towards the local copy
* Is there a more resource friendly way to test the behavior without shipping the whole test environment?