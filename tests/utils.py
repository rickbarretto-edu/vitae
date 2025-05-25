from functools import wraps
from typing import Callable


def should(description: str) -> Callable:
    """
    Decorator to label a test function with a descriptive expectation.

    Useful for BDD and readable tests. This also adds the description
    to the documentation of the wrapped function as "Should {description}".

    Parameters
    ----------
    description : str
        describes the bahavior of the test.

    Returns
    -------
    Callable

    Examples
    --------
    >>> @should("be instance of Err")
    ... def test_err_result():
    ...     result = Err("fail")
    ...     assert isinstance(result, Err)
    ...     assert not isinstance(result, Ok)
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        wrapper.__doc__ = f"Should {description}"
        return wrapper

    return decorator
