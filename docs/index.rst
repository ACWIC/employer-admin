ACWIC employer-admin API service
================================

.. _Aged Care Workforce Industry Council: https://acwic.com.au
.. _GitHub: https://github.com/ACWIC/employer-admin
.. _how to run the services together: https://acwic-employer-coordinator.readthedocs.io

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
(ACWIC) and published at `GitHub`_.
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


System Requirements
-------------------

The Aged Care Provider uses this service
for one administrative task
(create new enrolment authorisation)
and to access data provided by Training Providers.

.. uml:: requirements.uml

The above diagram shows Training Providers
dispatching training events
to the callback service for context.
This is where the callback data comes from,
such that the admin service can access it.


Create new enrolment authorisation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The "enrolment authorisation" is a bridging identifier
that links student identity in the Training Provider system
with the employee identity in the Aged Care Provider system.

It also contains a unique "shared secret"
used by the Training Provider for authentication
when communicating with the Aged Care Provider
about this enrolment.


View enrolment status and summary
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When the Aged Care provider first creates an enrolment,
the service generates some unique identifiers
but these have not yet been shared with anyone.

Over time, as data is accumulated
about the enrolment authorisation,
(because Training Providers are sending
data to the callback service)
the status of the enrolment may change.
For example:

* **transactional messages**
  inform the employer that an enrolment was successful,
  or a course has been completed, etc
* **credential messages**
  inform the employer when students demonstrate competance
  as assessed by criteria that are part of an agreed standard
* **training insight messages**
  provide the employer with additional information
  that the training provider thinks may provide
  useful insights to the employer

The enrolment status is derived from
the transactional messages.
The enrolment summary adds an aggregated summary
of messages received to the status.


View event summary
^^^^^^^^^^^^^^^^^^

The event summary provides a summary of all the
transactional, credential and training insight messages
sent to the employer
by the training provider
in relation to a particular enrolment.

This provides a complete history of the enrolment,
containing enough information to calculate the current state
and also what the state would have been at any point in the past.

The event summary is also an index of event details,
that can be used to access what the training provider sent.


View event detail
^^^^^^^^^^^^^^^^^

This endpoint allows the employer to access
exactly what the training provider sent them.
