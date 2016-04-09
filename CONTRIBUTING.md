# Get Involved

The goal of PPB is to be a learning tool. Building games can be complex, and
PPB should make that complexity approachable for new developers. It is also 
open to developers of all skill levels for contribution and improvement.

This guide will include steps experienced developers may not need explanation 
for, it's target audience is new developers not used to contribution.

## Before You Begin

* Read the [README](https://github.com/pathunstrom/pursuedpybear/blob/master/README.md).
* Read the [Code of Conduct](https://github.com/pathunstrom/pursuedpybear/blob/master/CodeofConduct.md).
    * All contributors must abide by the current code of conduct.
    * The current code of conduct is the [Contributor Covenant](http://contributor-covenant.org/)
* Familiarize yourself with this guide!
* [Fork](https://help.github.com/articles/fork-a-repo/) ppb.

## Tasks

If you'd like to work on the engine itself, you can contribute to tasks.

### Task Contribution Steps Summary

1. Choose a task.
2. Comment on the Github issue.
3. OPTIONAL: A maintainer can assign the issue to one team member.
4. Make a new branch.
5. Code
6. Merge
7. Pull request
8. Review
9. Issue is closed

### Choose a Task

Items will be kept in two places:

* [Github Issue Tracker](https://github.com/pathunstrom/pursuedpybear/issues)
* [Project TODO file](https://github.com/pathunstrom/pursuedpybear/blob/master/TODO.md)

Any task in the TODO file should have a related item in the issue tracker. 
Items in the issue tracker may not have a related item in the TODO file. When 
you have picked a task, comment on the Issue that you're working on it. The 
intent is to let other developers know who to communicate with while working on 
a task and which remotes to track.

### Task Assignment

In some cases, a maintainer will choose a contributor to assign the task to.
The assignee will come from people working on the task, and that person will
be the arbiter of work on the task. If a person is assigned, only pull requests
from that user will be accepted into master.

### Make a Branch

Make a working branch off of ppb/master. ppb/dev is [pathunstrom](https://github.com/pathunstrom)'s 
working branch. Do not base work off of this branch.

### Do the Work

Now it's time to code.

Feel free to work however is best for you.

Python's PEP 8 is strongly encouraged.

### CONTRIBUTORS.md

Before you finish, add your information to CONTRIBUTORS.md.

Form: \[NAME](github profile) | email | Twitter

Name does not have to be your legal name. It can be any identifier you are 
comfortable with as long as it does not break the code of conduct.

Both email and Twitter are optional field. You may also make them hyperlinks.

### Merge into Local Master

Make sure to [update your local master to match](https://help.github.com/articles/fork-a-repo/#keep-your-fork-synced) ppb/master. Then merge your 
working branch into local master. Resolve conflicts and make sure all the 
examples and available tests still work. Then push to your fork.

### Pull request

Make a Pull Request through github to ppb/master. Please make sure the request 
has a meaningful title and references the issue number you're working on.

*Example*

> Ref #8: Contributing Guide

### Review

At least one maintainer and anyone else working on the task will review your 
code using the issue tracker. When a consensus is reached, the code will be 
merged into master and the task closed.

## Documentation

Due to PPB's aim as a learning library, documentation standard will be higher 
than most projects. All modules, classes, functions and methods should include 
[docstrings](https://en.wikipedia.org/wiki/Docstring#Python). 

Currently we are using [reStructuredText](https://en.wikipedia.org/wiki/ReStructuredText#Examples_of_reST_markup) style.

All examples will include section by section explanation of the code.

If you see any code without docstrings or explanatory in line comments, feel 
free to add them. The process is similar to tasks, but should include ONLY 
documentation in the changes.

In the pull request, make sure the title includes the word Documentation and 
the body of the comment includes what was documented.

## Examples

Examples using various parts of the engine in different ways is highly 
encouraged. An example must run with the current HEAD when it is added. Please 
document the example well. The pull request should include the word Example in 
the title.

In addition, when there is a major shift in the API, some examples might break.
Contributors are encouraged to update examples to current standards.

## Requests, Bug Reports, Enhancements, and Other

If you're not comfortable working on the code, join the discussion on the issue 
tracker. 

If you need a specific interface for your project, add an issue with a detailed 
summary of what you need, why you need it, and a link to an example of how you 
expect it to work. Use the feature label.

If you find a bug in the engine add an issue and mark it as a bug. Please include
the events that create the bug and a minimal example that recreates the bug. 
This will be examined by contributors and determined where the task belongs.

If you have an idea to improve the code in any way (better algorithms, improved 
organization, better naming), add an issue and mark it as an enhancement. 
Optimizations and improvements that do not break the current API 
(Or can be integrated with the current API) are more likely to get moved to a 
task.

Feel free to join any discussion on any issue. Community feedback will be 
critical to making the goal of PPB a reality.