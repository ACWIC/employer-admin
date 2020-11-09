Overview
========

This is a software component (microservice)
that is designed to be operated by Aged Care Providers
to facilitate machine-to-machine interaction
with Training Providers.

It is an open-source reference implementation
provided by the
[Aged Care Workforce Industry Council](https://acwic.com.au)
(ACWIC) and published at
https://github.com/ACWIC/employer-admin

This particular component is designed to work
as part of a suite of microservices.
Reference implementations of all necessary components
are provided at the ACWIC GitHub site.
The suite of microservices aims to
enable Aged Care Providers and Training Providers
to integrate their systems
using industry-standard APIs
and with negligible aditional
operating cost.

For example, an Aged Care provider running this service
and it's companion, the
[employer-callback](https://github.com/ACWIC/employer-callback),
who has a modest level of traffic (e.g. ~100 employees)
could operate these services in the Amazon Web Services
cloud environment for approximately
the cost of one cup of coffee per year.

Of course, the cost of systems-integration
and adaptation to business processes
would be significantly higher.
Complex and/or high volume businesses
may need to modify this software to meet their needs,
or may prefer to provide equivalent APIs
using their existing platforms.
This software is offered as the starting point
to industry colaboration aimed at developing
best practices in a cost effective manner.
Future changes to this software will be driven
by a desire to balance a number of values such as
minimising the total cost of ownership
and lowering barriers to best-practice adoption
within industry.

This technical documentation is aimed at
software developers and systems integrators
who need to operate or interface this software.

For general information about ACWIC,
please visit the
[ACWIC web site](https://acwic.com.au)
