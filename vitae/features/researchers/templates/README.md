# Researchers/Templates

Templates related stuff goes here. From configuration of templates to templating itself.

The choosen Templating engine was Jinja with the JinjaX extension.
See [Jinja's Documentation](https://jinja.palletsprojects.com/en/stable/) and [JinjaX's Documentation](https://jinjax.scaletti.dev/) to get more details about how to work with them.

The reason why I choose the JinjaX extension can be found here: [JinjaX - Motivation](https://jinjax.scaletti.dev/motivation/), but not only, see their homepage to see the difference between using templates and components. If you want to see the benefits of this, see this Pull Request, it talks by itself: [Use JinjaX components instead of pure Jinja Templates #46](https://github.com/lasicuefs/curricFilter/pull/46).

## Organization

- **Functional**
    - `ui`: Basic UI components.
    - `form`: Basic Form components that updates its state from URL.
    - `layout`: Page's Layouts, including `Page`, which is the base for any of our pages.
- **Contextual**
    - `researcher`: Any researcher related component.
    - `search`: Specific components for searching feature.
