# Moody

## About

A conceptual RESTful API service for mood data.

## Goal

Demonstrate my ability to write skeleton code for a backend API.

Specifically, the design of the API should allow us to collect mood data so that it can provide useful insights.

* Frequency distribution of a user’s mood
* Proximity to which type of locations (home, office, shopping center, park) make the user happy

## Implementation Details

> Define API

`POST /mood_events` is defined to create a `MoodEvent` record. Along with an authorization token (implemented using JWT), the client is required to provide the following data to fulfill the request:

* sentiment
* latitude
* longitude

`GET /mood_events` is defined to get `MoodEvent` records of the user. The end goal is to allow multiple query parameters for this route to filter a user's collection of mood events.
e.g. Get all "happy" mood events since Dec. 11th, 2017.

```
GET /mood_events?sentiment=happy&created-after=12-11-17
```

> Create dev project

I chose Flask to implement the application. It's the framework I'm most comfortable with.

> Layout code structure

I decided to keep the code layout simple and semantic as possible. As the application and its required logic grows, it will probably be a good idea to subdivide some of the modules into their respective domains (e.g. separate blueprints for handling mood events and user authentication/authorization).

> Design data model and key data structures

`MoodEvent` defines the data captured from a single mood event. It will store the sentiment that was determined by the mood-sensing application, the location of the event, datetime of when this event was created.

`User` defines the user of the application. This will help us identify which `MoodEvent` belongs to whom.

`Place` defines a distinct place/area that will be meaningful to a user. We want to use this model to associate `Place`s with particular `MoodEvent`s.

> Define data persistence using any datastore of your choice.

Relational SQL database. Specifically, PostgreSQL since that's what I'm most comfortable with but it's not enforced/defined within my current implementation since I'm not using any Postgres-specific features with the ORM.


> Define Implementation of operations

See [routes.py](./moody/routes.py)

> Input validation

Request validation and object serialization is handled by Marshmallow.
See [schemas.py](./moody/.schemas.py)

> Authentication

Require email to fetch user from database. Require password to verify that user is in fact who he/she claims to be.

> Authorization

Issue an authorization token to user. JWT implementation allows verifying tokens to be stateless. Payload in the token can describe specific authorization permissions if necessary since the data is signed.

> Unit test

Use `pytest` as test runner and use `unittest.mock` for mocks and monkeypatching.

> Instrumentation for performance management

Not very experienced with measuring backend API performance. My initial thinking is to define a script that tests the amount of load the application can handle by keeping track of average response times based on amount of load. I'll need to do further research, testing, and evaluation of 3rd party libraries/services to get a better idea how this should be implemented.

> Provide insights such as:
>
> • Frequency distribution of a user’s mood
>
> • Proximity to which type of locations (home, office, shopping center, park) make the user happy

The initial implementation doesn't explicitly provide this information. However, I think the design of the API should allow a client or a backend worker to calculate this kind of information with its current implementation.

for frequency distribution of a user's mood:

* Use the `GET /mood_events` endpoint with `created-before` + `created-after` query parameters.
* Sum the counts of each `sentiment` across the collection of mood events returned from the API

for proximity to which type of locations make the user happy:

* Use the `GET /mood_events` endpoint with `sentiment=happy` query parameter.
* Sum the counts of each `Place` associated with each happy `MoodEvent` and sort by count

I did a rough implementation for these to examples in [insights.py](./moody/insights.py)

## TODO

* implement remaining functions/modules
* write queries for insights.py
* provide routes for insights?
* write tests
* add more documentation
* support db schema migrations?
* add dockerfile, docker-compose
* investigate other resources other than Google Places API
