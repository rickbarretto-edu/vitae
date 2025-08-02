# Researcher/model

This directory contains all Researcher Feature's domain models.

Some models have the ability to be converted from database schemas by using `from_table` classmethod. Some may argue that this is not a Clean Architecture's good practice, but since this classmethods behaves the same way a `converter.py` module would do, I prefered to attatch them to my models.

This is not a behavioral approach, but organizational one. I think it's more readable to have `Researcher.from_table(schema)` than `researcher_from_table(schema)` and also makes auto-complete easier.

If my database or my model changes, I would need to change them anyway. Tests and linters should warn you when you have a misbehavior or typing issues, the same way. So one, is not more safer than the other.

## Primitive Obsession

I also have created small value objects that validates its own state in order to avoid Primitive Obsession. If you're interested to contribute to this project, follow this principle.

## Hungarian Notation

Please, don't! First, don't describe the type of something on its name, use type-hints for it. Second, this also applies to patterns.

Never write `Factory`, `Builder`, `Singleton` or whatever. This is a bad practice, documentation exists if needed. Don't use fancy approaches, worse is better, make the code simpler not complex.

### Repositories

If you're creating a `Repository`, don't write `UsersRepository`, or even worse, `IUserRepository`. Just write `Users` or `AllUsers`, simple like that. By definition, I should know that `Users(Protocol/ABC)` is a Repository of `User`s and their concrete classes are `UsersInDatabase`, `UsersInMemory`, `UsersInCatalog`...

### Factory

Do you actually need them? Use `@classmethod`s or initialize your object with keywords and default values.

### Singleton

Please, don't! Never use singleton.

### Builder

If you need to have a builder, make sure you've made its class private, I wouldn't like to call a `UserBuilder` class. What is a `UserBuilder` in real life?

Instead, follow [Fluent Interface](https://martinfowler.com/bliki/FluentInterface.html) principles, as described by Martin Fowler.

**Example:**

```py
fowler = (
    Author.use
        .name("Martin Fowler")
        .article(
            title="Fluent Interface", 
            date=Date(20, Month.December, 2005),
            tags=["API Design", "DSL"]
            href="https://martinfowler.com/bliki/FluentInterface.html"
        )
        .new()
)
```

And this should build something like:

```py
Author(
    name=AuthorName("Martin Fowler"),
    owns=Articles(articles=[
        Article(
            title=ArticleTitle("Fluent Interface"),
            date=Date(day=20, month=12, year=2005),
            tags=ArticleTags(tags=[
                Tag("API Design"), Tag("DSL"),
            ]),
            href=URL("https://martinfowler.com/bliki/FluentInterface.html"),
        )
    ])
)
```
