from fastapi.templating import Jinja2Templates
import jinjax

__all__ = ["templates"]


# =~=~=~=~=~=~= Filters =~=~=~=~=~=~=

def words(text: str) -> list[str]:
    return text.split(" ")


# =~=~=~=~=~=~= Jinja Setup =~=~=~=~=~=~=

templates = Jinja2Templates("vitae/features/researchers/templates")
templates.env.filters["words"] = words

templates.env.add_extension(jinjax.JinjaX)
catalog = jinjax.Catalog(jinja_env=templates.env)
catalog.add_folder("vitae/features/researchers/templates")
