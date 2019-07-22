# Contributing

We would love for you to contribute to LambdaPool and help make it even better than it is today! As a contributor, here are the guidelines we would like you to follow:

 - [Code of Conduct](#coc)
 - [Question or Problem?](#question)
 - [Issues and Bugs](#issue)
 - [Feature Requests](#feature)
 - [Submission Guidelines](#submit)
 - [Development Setup](#setup)
 - [Coding Rules](#rules)
 - [Commit Message Guidelines](#commit)

## <a name="coc"></a> Code of Conduct
Help us keep the project open and inclusive. Please read and follow our [Code of Conduct][coc].

## <a name="question"></a> Got a Question or Problem?

Do not open issues for general support questions as we want to keep GitHub issues for bug reports and feature requests. You've got much better chances of getting your question answered on Stack Overflow.

Stack Overflow is a much better place to ask questions since:

- there are thousands of people willing to help on Stack Overflow
- questions and answers stay available for public viewing so your question / answer might help someone else
- Stack Overflow's voting system assures that the best answers are prominently visible.

To save your and our time, we will systematically close all issues that are requests for general support and redirect people to Stack Overflow.

If you would like to chat about the question in real-time, you can reach out via [our slack channel][slack].

## <a name="issue"></a> Found a Bug?
If you find a bug in the source code, you can help us by
[submitting an issue](#submit-issue) to our [GitHub Repository][github]. Even better, you can
[submit a Pull Request](#submit-pr) with a fix.

## <a name="feature"></a> Missing a Feature?
You can *request* a new feature by [submitting an issue](#submit-issue) to our GitHub
Repository. If you would like to *implement* a new feature, please submit an issue with
a proposal for your work first, to be sure that we can use it.
Please consider what kind of change it is:

* For a **Major Feature**, first open an issue and outline your proposal so that it can be
discussed. This will also allow us to better coordinate our efforts, prevent duplication of work,
and help you to craft the change so that it is successfully accepted into the project.
* **Small Features** can be crafted and directly [submitted as a Pull Request](#submit-pr).

## <a name="submit"></a> Submission Guidelines

### <a name="submit-issue"></a> Submitting an Issue

Before you submit an issue, please search the issue tracker, maybe an issue for your problem already exists and the discussion might inform you of workarounds readily available.

We want to fix all the issues as soon as possible, but before fixing a bug we need to reproduce and confirm it. In order to reproduce bugs, we will systematically ask you to provide a minimal reproduction. Having a minimal reproducible scenario gives us a wealth of important information without going back & forth to you with additional questions.

A minimal reproduction allows us to quickly confirm a bug (or point out a coding problem) as well as confirm that we are fixing the right problem.

We will be insisting on a minimal reproduction scenario in order to save maintainers time and ultimately be able to fix more bugs. Interestingly, from our experience users often find coding problems themselves while preparing a minimal reproduction. We understand that sometimes it might be hard to extract essential bits of code from a larger code-base but we really need to isolate the problem before we can fix it.

Unfortunately, we are not able to investigate / fix bugs without a minimal reproduction, so if we don't hear back from you we are going to close an issue that doesn't have enough info to be reproduced.

### <a name="submit-pr"></a> Submitting a Pull Request (PR)
Before you submit your Pull Request (PR) consider the following guidelines:

1. Search [GitHub][github] for an open or closed PR that relates to your submission. You don't want to duplicate effort.
1. Be sure that an issue describes the problem you're fixing, or documents the design for the feature you'd like to add. Discussing the design up front helps to ensure that we're ready to accept your work.
1. Fork the [rorodata/lambdapool][github] repo.
1. Make your changes in a new git branch:

     ```shell
     git checkout -b fixes-issue-id master
     ```

1. Create your patch, **including appropriate test cases**.
1. Follow our [Coding Rules](#rules).
1. Ensure that all tests pass.
1. Commit your changes using a descriptive commit message that follows our
  [commit message conventions](#commit).

     ```shell
     git commit -p
     ```

1. Push your branch to GitHub:

    ```shell
    git push origin fixes-issue-id
    ```

1. In GitHub, send a pull request to `lambdapool:master`.
- If we suggest changes then:
  - Make the required updates.
  - Re-run the test suite ensure tests are still passing.
  - Rebase your branch and force push to your GitHub repository (this will update your Pull Request):

    ```shell
    git rebase master -i
    git push -f
    ```

That's it! Thank you for your contribution!

#### After your pull request is merged

After your pull request is merged, you can safely delete your branch and pull the changes
from the main (upstream) repository:

- Delete the remote branch on GitHub either through the GitHub web UI or your local shell as follows:

    ```shell
    git push origin --delete fixes-issue-id
    ```

- Check out the master branch:

    ```shell
    git checkout master -f
    ```

- Delete the local branch:

    ```shell
    git branch -D myfixes-issue-id
    ```

- Update your master with the latest upstream version:

    ```shell
    git pull --ff upstream master
    ```

## <a name="dev-setup"></a> Development Setup

The development machine should have Python 3.6 installed. It is recommended to setup the development using [virtualenv](https://virtualenv.pypa.io/en/latest/) with/without [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/). Setting them up is out of the scope of this document and can be referred from above linked project websites.

The project dependencies can be installed using:

```bash
(venv) lambdapool $ pip install -r requirements.txt
...
```

In order to develop `lambdapool`, it must be installed in editable mode so as to keep on testing the modifications as they are developed:

```bash
(venv) lambdapool $ pip install -e .
...
```

We prefer using [pytest](https://pytest.org) as our testing suite, [pytest-flakes](https://pypi.org/project/pytest-flakes/) as our linting tool and [pytest-cov](https://pypi.org/project/pytest-cov/) as our code coverage tool.

```bash
(venv) lambdapool $ pip install -r dev-requirements.txt
...
```

It is recommended to always run the tests before filing any Pull Request. A [bash script](runtests.sh) exists in the project for the convenience of the developers which runs the tests along with flakes checks and calculates code coverage.

```bash
(venv) lambdapool $ ./runtests.sh
...
```

## <a name="rules"></a> Coding Rules
To ensure consistency throughout the source code, keep these rules in mind as you are working:

- All features or bug fixes **must be tested**.
- All public API methods **must be documented**.
- The functionality implemented **must have proper type annotations**.
- We follow [Google's Python Style Guide][python-style-guide] to an extent. The focus should always be on code readability and future extensibility rather than on rules.
- The code **must not fail flake checks**.
- Code coverage must maintained well, although this may not mean that the tests are appropriately written.
- Add the appropriate change to the the topmost subheading in the [CHANGELOG][changelog]

## <a name="commit"></a> Commit Message Guidelines

The seven rules of a great Git commit message

> Keep in mind: This has all been said before.

1. Separate subject from body with a blank line
1. Limit the subject line to 50 characters
1. Capitalize the subject line
1. Do not end the subject line with a period
1. Use the imperative mood in the subject line
1. Wrap the body at 72 characters
1. Use the body to explain what and why vs. how
1. Present tense or imperative tense both are okay in subject lines

For example:

```
Summarize changes in around 50 characters or less

More detailed explanatory text, if necessary. Wrap it to about 72
characters or so. In some contexts, the first line is treated as the
subject of the commit and the rest of the text as the body. The
blank line separating the summary from the body is critical (unless
you omit the body entirely); various tools like `log`, `shortlog`
and `rebase` can get confused if you run the two together.

Explain the problem that this commit is solving. Focus on why you
are making this change as opposed to how (the code explains that).
Are there side effects or other unintuitive consequences of this
change? Here's the place to explain them.

Further paragraphs come after blank lines.

 - Bullet points are okay, too

 - Typically a hyphen or asterisk is used for the bullet, preceded
   by a single space, with blank lines in between, but conventions
   vary here

If you use an issue tracker, put references to them at the bottom,
like this:

Resolves: #123
See also: #456, #789
```

Reference: https://chris.beams.io/posts/git-commit/

[coc]: CODE_OF_CONDUCT.md
[slack]: https://slack.rorocloud.io
[github]: https://github.com/rorodata/lambdapool
[python-style-guide]: http://google.github.io/styleguide/pyguide.html
[changelog]: CHANGELOG.md