# Contributing to tuxmake

## Development dependencies

The packages needed to develop tuxmake are listed in both `requirements-dev.txt`
and `.gitlab-ci.yml`

## Running the tests

To run the tests, just run `make`: it will run the unit tests first, then the
coding style checks, then the integration tests. Please make sure all the tests
pass before submitting patches.

To run the integration tests, you need to have tuxmake available in your $PATH.
Here are two ways in which you can do that:

- Install tuxmake from sources for development `flit install --symlink` and
  ensure that ~/.local/bin is in your $PATH.
- Create a symlink named `tuxmake` in any directory that is in your $PATH,
  pointing to /path/to/tuxmake-sources/run
