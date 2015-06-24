# Test suite for SELECT, GET, FIND command
This test suite attempts to stress test how well the service behaves in
long running, repeated SELECT, GET, FIND command.

## Parameters

- BIGOBJECT\_HOST: hostname for the service
- BIGOBJECT\_PORT: port number for the service
- WORKER: number of workers

## Assumptions

The test dataset is from our sales demo data.  The object breakdown is

- Product
- Customer
- sales

There is a 25% chance that worker (this test) will break off connection before
result set completes transmission.

In the other 75% the worker expects the result set to be available in 1 second.

Tests run indefinately, until any which worker failed in anyway.
