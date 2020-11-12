# Development

This is a python FastAPI app
built in the "clean architecture" style
(using functionally pure domain entities,
repository objects that encapsulate IO,
use-case classes that encapsulate business logic, etc).

See [DEPLOYMENT.md](DEPLOYMENT.md) for instructions on how to deploy this service

---

## Collaboration
We work in GitHub with a [github flow](https://guides.github.com/introduction/flow/),
and require all PRs to be reviewed before merging.

There is some guard-rails preventing merges
that violate test coverage or code style policies,
or failing tests as well.


## Coding Style guide
We use pre-commit hooks, including black, isort, flake8.

The suggested way to install these hooks it is by installing [pre-commit](https://pre-commit.com/),

then running `pre-commit install`

Note that on the first time you run `git commit`,
it's going to  take some time to install all the hooks,
but after that it will be fast.


## Configuration
Your personal secrets and configuration should be stored in a `.env` file.
This file is not tracked in git.

To start, create the file with the following contents
```
CALLBACK_BUCKET=put-callbacks-here
ENROLMENT_BUCKET=put-enrolments-here
```


## Local development
Everything is managed with `docker-compose`. The configuration for this is stored in
`local.yml`, so it can be convenient to set this in your shell first:
```
export COMPOSE_FILE=local.yml
```

1. `docker-compose build` - build everything
2. `docker-compose up -d` - run everything in daemon mode

There are two components:

1. API documentation (via uvicorn/FastAPI directly)

2. minio (mimics AWS lambda)

**A note about local resources:**

**docker-compose** will not auto-create S3 buckets in minio,
so this must be done manually first.
see your app/config.py file to know which files to create.

you can access the minio service on `http://localhost:9001` after you run `docker-compose up`.

We've already defined the bucket names in the `.env` file. use those names to create the buckets in `minio`.


## Tests
Tests are managed by pytest, which can be executed with the shortcut make command:
```
make test
```
