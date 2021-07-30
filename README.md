# Control framework reports

This script generates reports for the control framework

## Installation

Make a copy of `example.env` file with the name `.env`. Fill missed credentials and settings there.

From the root of the project run
```
make install
```
It will create a virtual environment and install all the dependencies.

## How to run
Switch to the virtual environment
```
. venv/bin/activate
```
Then run 
```
python main.py <args>
```

## For developers
To setup a dev environment run
```
make dev_install
```
Run unittests
```
make test
```
Check linters
```
make lint
```
Try to fix linter and sort errors automatically
```
make format
```

Check `Makefile` for other possible commands

## PR Submission Policy

All commits are mandatory to start with the prefix NEW, FIX or OPT :

> NEW - all new features, can brake backward compatibility.
> FIX - fixing an issue in existing functionality.
> OPT - optional improvements, refactoring etc. Must be backward compatible.

## Related Documentation

* [Pulling Data Out of Oracle database with Python using SQLAlchemy](https://confluence.aws.abnamro.org/pages/viewpage.action?spaceKey=MPSR&title=Pulling+Data+Out+of+Oracle+database+with+Python+using+SQLAlchemy)

