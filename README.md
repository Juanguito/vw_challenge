# Tic Tac Toe Challenge
 
Author: Juan Gabriel Sánchez Martí


The purpose of this project is to validate my skills creating an easy to understand, scalable and maintainable app.

This `README` file consists of two distinct parts:
1. Web Service implementation
2. User management service design

## 1. Web Service implementation

### Overview
For this project I spent slightly more than half the time writing code, what has been fun, and almost half of the time researching and setting up the infrastructure of the project as I had never dealt with some topics as the DDBB creation, or the containerization of the services, as they had been previously defined by others at the companies where I worked.

### Installation
Download or clone this project in a local directory.

The project contains a `Makefile` with the commands that you can use. Run `$ make help` to get a list of them:

```bash
$  Tic-Tac-Toe-game > make help 
Commands:
  local_setup: Creates a virtual environment and installs the dependencies.
  local_clean: Removes the virtual environment.
  local_run: Starts the application locally.
  up: Starts application containers.
  down: Stops application containers.
  check: Formats the code using black, verifies types with mypy and linting with flake8.
  logs: Shows the logs of the application.
  test: Runs unit tests.
```
### Used Technologies
For this project, in order to keep it standard, scalable and not too much complex, I decided to use:
- Docker -> Containerizing the services
- Docker Compose -> Ability to build several containers and connect them
- Python Virtual Environments -> To not polute local computer environment
- PostgreSQL -> A widely used database
- SQLAlchemy -> Extended Python SQL toolkit and Object Relational Mapper
- Alembic -> Database migration tool for usage with the SQLAlchemy
- Black -> For formatting
- Flake8 -> For linting
- Mypy -> For type verification
- Makefile -> Eases the use of the available app commands
- setup.cfg -> For tuning the formatter and the linter

### How to run
Running the app is very simple. Execute:
```bash
$ make up
```
It will start 2 containers (`postgres_db` for the app, `tic_tac_toe_app` for the ddbb) and the app endpoints will be available at `http://127.0.0.1:8000/`

To run the app locally, stop or remove the `tic_tac_toe_app` container and then:
- Create a virtual environment, activate it and install project dependencies:
```bash
$ make local_setup
```
- Run the FastAPI server:
```bash
$ make local_run
```


### Project Architecture
I decided to implement the project with my personal view of an `Hexagonal Architecture`, as it helps to isolate the components of the app. Allowing it to scale and adapt easily to changes by decoupling the business logic of the external dependencies decisions. This facilitates testing by replacing external dependencies by Mocks or InMemory repositories.

I decided to use `Docker `containers as they allow to be independent the services of the machine where they  run on, ensuring consistent behavior across environments. For those reasons, I configured 2 services: one for the PostGreSQL database and another for the application, in this case a FastAPI server.

The use of a `PostgreSQL` database, `SQLAlchemy` and `Alembic`, is due to they were the tools I used in my last company and they seem to be very extended in the industry.

Same for `Flake8`, `Black` and `Mypy`, as they are very extended Python tools.

I did'nt implemented any CI/CD pipeline as I don't have time enough. Anyway, it would be interesting to run it through, i.e. using Github Actions.

### Implementation details
I started the project creating a hexagonal directory structure and a `main.py` file with the minimum code to start a FastAPI app:
```
- vw_challenge
 |- src
   |- application
   |- domain
     |- models
     |- repositories
     |- services
   |- infra
     |- repositories
 |- tests
 |- main.py
```
Then I continued creating some domain entities (`Match`, `Status`, `Movement`) with some basic fields.

I created the interface (`ABC` class with `abstract methods`) at `domain -> repositories -> match_database_repository` that must implement the repositories for dealing with `Match`. Methods are `create`, `retrieve` and `update`.

As it will be needed to add loggin to the app, I created a new Interface `domain -> services -> logger_interface` which will force loggers to use typical `info`, `warning`, `debug` and `error` methods.

Additionally, I implemented a `InMemoryRepository`at `domain -> infra -> repositories -> in_memory_repository` in order to be able to start to implement and test some code.

Next, create app Use Cases. I decided that, for the moment, there are only needed 3 use cases:
- Create Match
- Make Movement
- Get Match Status

I implemented them in a very simple way as they will receive, via dependency injection, instances of `Logger` and `MatchDatabase` implementations, and the call the match service to perform the required operations.

I then began implementing the MatchService, as I had all the necessary components to define the business logic:
- Instead of returning `None` when something is wrong, I raise `Custom Exceptions`.
    - I decided to create CustomExceptions at `domain -> errors` to handle specific error scenarios. I implemented a `to_http_exception()` method to convert these custom exceptions into `HTTPException` instances that FastAPI can handle.
- `Match Service` receives injected instancies of classes that implement the needed functionality.
    - Only the `create_match()`, `move()` and `get_match_status()` methods are public. The others are `private`.
- Tests were written.

After completing this code, I continued defining the required endpoints at `infra -> routers`.The code for each endpoint is very simple where:
- The url is defined
- Parameters are received and mapped using `Pydantic` capabilities
- `Use cases` are instantiated and executed using `dependency injection`
- Exceptions are caught and converted to `HTTPException` instances.
- Required values are returned
- Tests were written. (One test is currently commented out due to an issue that I will address later)
- The `logger` is initialized with standard values.

Then, I implemented `infra -> logging_service` using the stardard `logging` library.

I then began working on the database implementation:
- I configured a `PostgreSQL` container using docker-compose. A .env file is included for ease of setup, but this should not be included in a production repository. 
    - I used example values for the user, password, and database name (fastapi_user, fastapi_pass, and fastapi_db) as I did not deem it necessary to change them for this exercise.
- I implemented `infra -> entities` to define a `matches` table and its columns.
    - I added methods `to_match()` and `from_match()` to map from the domain model to this infra entity, and viceversa.
- I implemented `infra -> repositories -> postgresql_repository` with the required operations by the `match_database_repository`.
- I used Alembic to create an `Initial migration`


The app is almost complete, so it's time to run the service:
- I created a `Dockerfile` to run it in a container.
- For it, I created `requirements` folder where I defined dependencies for `prod` and `dev` in split files as I don't want to polute the system with debugging libraries.
- I added the options to `docker-compose` file. I included a command to run pending migrations if they exist.

In order to ease run the app, I wrote a `Makefile` with some useful commands. I added a `setup.cfg` with some common formatting and linting options.

## 2. User management service design
The objective of this part is to design the next functionality evolution by adding the "User" concept.
There is no implementation required on this step, only a new set of documented features, API, service functionality and Database structure related to the "Users" concept and their management.

### Users features detail
This addition will enhance the multiplayer experience by associating players with their matches and enable future improvements like user statistics, leaderboards, and authentication security.

#### User Registration & Authentication
Users will be able to create an account by providing a username and password.
Passwords will be securely hashed and stored ensuring that no plain-text credentials are exposed.
A basic login system will validate user credentials and return a session token.
Users will only able to view and update their own information (it could change in the future if an `admin` role is implemented).

#### Match Participation & User Association
Matches will no longer exist in isolation; each match will have associated users who participate in it.
We must ensure that only authenticated players can interact with ongoing games.

#### Profile Management
Users will have a minimal profile that includes their username and password.

#### Security Considerations
- Authentication: Ensures only logged-in users can interact with the games. Endpoints must receive a user_token param to validate their identities.
- Secure Password Storage: Passwords will be hashed using industry-standard encryption (e.g., `hashlib` or `bcrypt`).


## API

### New endpoints for users management
| Method    | Endpoint            | Description                                       | Payload                                                            | Response
|-----------|---------------------|---------------------------------------------------|--------------------------------------------------------------------|-----------------------------------------------------------|
| POST      | /users/create       | Register a new user (returns user ID).            |{"username": "The name/nick of the user", "password": "Password"}  | `Status=200`<br>{"user_id": "The user identifier"}
| POST      | /users/login        | Authenticate a user and return a session token.   |{"username": "The name/nick of the user", "password": "Password"}  | `Status=200`<br>{"token": "Token string", "user_id": "The user identifier"}
| POST      | /users/logout/{user_id}      | Logouts the user and removes the session token.   |{"token": "Token}  | `Status=200`
| POST       | /users/{user_id}    | Retrieve user own details.                        |{"token": "Token string"}                                           | `Status=200`<br>{"username": "The name/nick of the user, "password": "Password", "created_at": "Creation date", "updated_at": "Latest update date"}
| PUT       | /users/{user_id}    | Update user own profile information.              |{"token": "Token string", "password": "New password"}              | `Status=200`<br>{"username": "The name/nick of the user, "password": "Password", "created_at": "Creation date", "updated_at": "Latest update date"}

### Existing endpoints must be updated
The existing endpoints must be moved to `/match` in order to avoid conflicts and not clear urls, despite other updates as adding `token` as `POST` parameter:
| Method    | Endpoint            | Description                                       | Payload                                                            | Response
|-----------|---------------------|---------------------------------------------------|--------------------------------------------------------------------|-----------------------------------------------------------|
| POST       | /match/create       | Creates a new match.            | {"token": "Token string", "user_id1": "User identifier for player 1", "user_id2": "User identifier for player 2"}  | `Status=200`<br>{"matchId": "The new match's ID"}
| POST      | /match/move        | Movement of a user.   |{"token": "Token string", "matchId": "The match's ID" "playerId": "'X' or 'O'", "square": { "x": <x>,"y": <y>}}  | `Status=200`
| POST      | /match/status/{matchId}      | Current status of a given match.   |{"token": "Token}  | `Status=200`<br>{"matchId": "The new match's ID"}
- NOTE: `/match/create` endpoint has changed from `GET` to `POST` as it now requires a `token` parameter


### Database updates
A new table `users` must be implemented. This table should contain:
- id (UUID)
- username (str)
- password (str)
- token (str | None)
- created_at (datetime)
- updated_at (datetime | None)

A new `match_participants` table must be implemented. As a match, currently, can only be played by 2 people, fields should be:
- match_id (UUID)
- player1_id (UUID) references to table `matches` field `id`
- player2_id (UUID) references to table `matches` field `id`
- created_at (datetime)
- updated_at (datetime | None)

But, in case we want to to admit more than 2 players in the future, then fields could be:
- match_id (UUID)
- player_id (UUID) references to table `matches` field `id`
- created_at (datetime)
- updated_at (datetime | None)

In both cases, a match can have multiple players and player can play multiple matches, and this last implementation is valid for 2 players too.

All theese changes will be implemented in `infra -> entities -> user_db.py`.

Finally, we must create a new migration to keep changes updated.

## Architectural design changes

As current Architecture was choosen in order to be easily updated, only few changes would be needed:
### Application
New uses cases must be added:
- CreateNewUserUseCase
- LoginUserUseCase
- LogoutUserUseCase
- GetUserUseCase
- UpdateUserUseCase
- CreateNewUserUseCase

### Domain
**Models** - Create a new file `user.py` where implement the class `User` that represent the User must be created with fields `id` (UUID), `username` (str), `password` (str), `token` (str | None), `created_at` (datetime) and `updated_at` (datetime | None).

**Repositories** - Create new file `user_database_repository.py` which will implement the class `UserDatabaseRepository` that will act as an interface with methods `get_user()`, `save_user()` and `update_user()`

**Services** - Create a new file `user_service.py` that will implement the class `UserService` with the methods `create_user()`, `update_user()`, `get_user()`. Additionally, I would add 3 more methods:
- `is_authorized()` - This method will check that the received token matches the stored one.
- `do_login()` - This method will check that the given user and password exists and will generate a token and return it.
- `do_logot()` - This method will remove the user token.

### Infra
**Entities** - Create a new file `user_db.py` where define the table name and the required columns. Add `from_user()` and `to_user()` methods to be able to map its contents to the User domain model.

**Repositories** - 2 approaches could be implemented:
- Keep using `PostgreSQLRepository` adding the methods required to accomplish with the new `UserDatabaseRepository` interface, inheriting from it.
- Rename `PostgreSQLRepository` to `MatchPostgreSQLRepository` and create a new `UserPostgreSQLRepository` that implements the requirements of `UserDatabaseRepository` interface.

### Tests
- Add tests for new User routes.
- Update old routes adding `/match`.
- Add new `test_user_services.py` where test the methods implemented at `user_service_py`.
