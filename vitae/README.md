# Vitae

## Architecture

Vitae is structured using **Vertical Sliced Clean Architecture**, which gives emphasis on feature-based organization (or domain-based) rather than function-based or layered-based approach. So, you won't see Repositories, Services, Controllers, layers globally. Instead you may or not may see them into each individual domain, sometimes they are not required, and this will be covered by each domain's documentation.

The reason of this choice is to promote encapsulation, reduce code coupling between unrelated parts and also be context-bound. Content matters, and matters a lot.

> **Note**: Vertical Slice is not an architecture itself but a **design pattern for organizing code**.

This approach requires some familiarity with Clean Architecture and DDD principles, especially the importance of *context*. The same term can have different meanings depending on its context, and this design acknowledges and embraces that.

### Benefits

What I've noticed when using this approach is that each domain has its own needs. i.e. Bootstrap feature does not have Repositories, Domain Models, only a CLI and a Use Case.

There is no need to have such things for simpler features. So I can use whatever approach I want or need for each case individually.

## Shared Components

While features are self-contained, some shared components are used across the application for practical reasons, especially when there's no meaningful value in duplicating them.

### Settings

The `settings` module defines a global `Vitae` configuration object that holds project-wide settings. Configuration values are provided through a `.toml` file instead of `.env`, for the following reasons:

- **Avoids environment pollution** with too many runtime variables.
- **TOML has wide adoption**, is used natively by Python via `pyproject.toml`, and has strong parsing support across languages.
- It’s **declarative and clean**, making it suitable for storing structured configuration.

Refer to the main `README.md` for instructions on how to configure this file and initialize the system.

### Database

The database layer is implemented using **SQLModel** (which integrates Pydantic and SQLAlchemy) to define models and schemas, while SQLAlchemy is used for transaction management and ORM capabilities.

- **Schemas** are located in `infra/database/tables/`.
- **Transactions**, including batched and performance-intensive operations, are in `infra/database/transactions/`.

This separation of concerns ensures that:
- Schema definitions remain isolated and reusable.
- Transaction logic can be optimized independently, as demonstrated in `feature/ingest`, where bulk ingestion needed high throughput and efficient querying.

## RSpec tests

Pytest is the choosen test runner, and with some configuration I've setted it up to use RSpec-ish syntax, which I think is more descriptive and helps a lot to understand the desired behavior.

See the internal test documentation to understand how to use it.
