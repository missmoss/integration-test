# integration-test
Integration test suite for BigObject service

## Composition
Each directory represent a test suite, having its own Dockerfile for
controlling the environment in which the test is run.

## How to run
Each directory has a runner that can be run simply by executing `python run.py`

Consult README in each test suite for a number of available parameters to tune

Tests will be scheduled on a recurring basis on a Jenkins build slave.
