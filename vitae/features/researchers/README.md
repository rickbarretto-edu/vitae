# Researchers

This is the **core domain** of the project and the most complex feature implemented so far.

Its main responsibility is to provide a **Web UI for non-technical users** to search, filter, and explore researchers, and then **export their connections to the Lucy Lattes** platform.

## Backend

The backend is built using **FastAPI**, chosen for its:

- Great development experience
- Clean and good defaults
- Fast iteration for building new features
- Lightweight, micro-framework design (as opposed to the heavier Django stack)

FastAPI allows us to focus on feature delivery without unnecessary overhead. It integrates well with Python’s ecosystem and fits the Vertical Slice model well.

The feature uses the **shared SQLModel-based database**, with no separate data store.

## Frontend

The frontend uses **Server-Side Rendering (SSR)** to eliminate the need for a JavaScript bundler or runtime like NPM, Node, or Deno. Since one of the project's constraints is to be easy to ship, and I think this wouldn't be as I want if multiple runtimes are required.

- The initial implementation used **Jinja2 templates**, but as complexity increased, maintenance became difficult.
- Templates were replaced with **JinjaX components**, which offer:
    - Isolated and reusable components
    - A cleaner, React-inspired syntax
    - Easier readability and maintainability

This architectural decision drastically improved development speed and UI consistency.

## Highlights

### Web

- `routes.py`: Defines all FastAPI HTTP endpoints for this feature.
- `templates.py`: Sets up and configures Jinja2/JinjaX environments.
- `templates/`: Contains all JinjaX components and page layouts shown to users.
- `schemas/`: Defines Pydantic schemas used for data transfer between backend, frontend, and domain layers.

### Domain

- `usecases/`: Contains the main application logic for querying and processing researcher data.
- `models/`: Holds the rich domain models that encapsulate the core business rules.
- `repository/`: 
    - Defines and implements repository interfaces for database operations.
    - Uses `database.session` directly for fine-grained transaction control.
    - Responsible for mapping database schemas to domain models.
