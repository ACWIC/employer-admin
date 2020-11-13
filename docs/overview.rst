.. _Aged Care Workforce Industry Council: https://acwic.com.au
.. _GitHub ACWIC Site: https://github.com/ACWIC/employer-admin
.. _how to run the services together: https://acwic-employer-coordinator.readthedocs.io

Overview
========

This is a software component (microservice)
that is designed to be operated by Aged Care Providers
to facilitate machine-to-machine interaction
with Training Providers.

This technical documentation is aimed at
software developers and systems integrators
who need to operate or interface this software.

It is an open-source reference implementation
provided by the

`Aged Care Workforce Industry Council`_
(ACWIC) and published at the
`GitHub ACWIC Site`_.
This particular component is designed to work
as part of a suite of microservices.
There is documentation about
`how to run the services together`_ 
on ReadTheDocs.

This component is called "Employer Admin Service"
because it's shorter name than
"Aged Care Provider Admin Service"
(more compact, easier to type).
But when we say "Employer"
we mean "Aged Care Provider".

This service provides administrative features
that support Aged Care Providers
to consume training services from partner organisations
(Training Providers).
Employers would operate this service
(or do something equivalent)
so that they can transact with Training Providers
and consume the data they provide
about the provision of training services.
