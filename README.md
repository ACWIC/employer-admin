[![codecov](https://codecov.io/gh/ACWIC/employer-admin/branch/master/graph/badge.svg?token=YB6L7D2H70)](https://codecov.io/gh/ACWIC/employer-admin)

# Employer Admin API

This is a reference implementation of a proposed API
enabling Aged Care providers to interact with training providers
in a standardised way.

Specifically, it provides the endpoints for registering a proposed
enrolment and accessing information sent to the employer,
by the training provider.

Detailed technical documentation is in the docs/ folder.

DEPLOYMENT.md and DEVELOPMENT.md contain information about running
the software and making changes to it.

There is a test endpoint at this URL:

* https://izu2v5346l.execute-api.us-east-1.amazonaws.com/dev/

And it has self-documenting API specification here:

* https://izu2v5346l.execute-api.us-east-1.amazonaws.com/dev/admin/docs

These are continuously deployed from the `main` branch in this repository,
so should be considered unstable. They are also completely open
(do not require authentication), which is not a realistic simulation
of any kind of production environment.
