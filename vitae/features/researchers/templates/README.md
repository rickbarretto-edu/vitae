# Researchers/Templates

This directory is related to Templating. From configuration to template files.

The choosen Templating engine was Jinja with the JinjaX extension. See [Jinja's Documentation](https://jinja.palletsprojects.com/en/stable/) and [JinjaX's Documentation](https://jinjax.scaletti.dev/) to get more details about how to work with them.

The reason why I choose the JinjaX extension can be found here in their website [JinjaX - Motivation](https://jinjax.scaletti.dev/motivation/), since I had the same motivation. But not only, see their homepage to see the difference between using templates and components. 

If you want to see real benefits of this approach, see this Pull Request that talks by itself: [Use JinjaX components instead of pure Jinja Templates #46](https://github.com/lasicuefs/curricFilter/pull/46).

## Organization

- **Functional**
    - `ui`: Reusable UI components.
    - `form`: Form components that bind state from URL.
    - `layout`: Page's layouts structure.
        - Includes `Page` layout, to be used across many pages.
- **Contextual**
    - `researcher`: Researcher domain related.
    - `search`: Components focused on search/filtering functionality.
