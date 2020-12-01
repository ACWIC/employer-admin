# Employer Admin API
[![codecov](https://codecov.io/gh/ACWIC/employer-admin/branch/master/graph/badge.svg?token=YB6L7D2H70)](undefined)
[![CircleCI](https://circleci.com/gh/ACWIC/employer-admin.svg?style=svg&circle-token=495a27fbb86a1f46740ec1b21726a181a04c1cb8)](https://circleci.com/gh/circleci/circleci-docs)

This is a reference implementation of a proposed API enabling Aged Care
providers to interact with training providers in a standardised way.
Specifically, it provides the endpoints for registering a proposed
enrolment and accessing information sent to the employer, by the
training provider.

See the Swagger API documentation:

* [Development version](https://ngkkz39vx8.execute-api.us-east-1.amazonaws.com/dev/admin/docs)
* [Preview version](https://prekb2sflh.execute-api.us-east-1.amazonaws.com/prod/admin/docs)

This is a companion service to
- [Employer Callback](https://github.com/ACWIC/employer-callback)

See these files:

* [DEPLOYMENT.md](DEPLOYMENT.md) how to run the software
* [DEVELOPMENT.md](DEVELOPMENT.md) how to make changes to the software

The Development version is continuously deployed from the `main` branch in this
repository, so should be considered unstable.
It is also completely open (do not require authentication),
which is not a realistic simulation of any kind of production environment.

For more information about running this service, see the
[Aged Care Provider Integration Guide](https://acwic-employer-coordinator.readthedocs.io).