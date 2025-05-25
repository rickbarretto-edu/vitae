from typing import Any, Callable


def also(*actions: Callable[[Any], None]) -> Callable[[Any], Any]:
    """Merge independent functions into a single one.

    Example:
    -------
        Buffer(
            on_flush=then(process_data, also(print, log)),
            max=64
        )

    """

    def function(data: Any) -> Any:
        for action in actions:
            action(data)
        return data

    return function


def then(*actions: Callable[[Any], Any]) -> Callable[[Any], Any]:
    """Pipe dependent functions into a single one.

    Note:
    ----
    The output of the latest function must be the same type
    of the input of the next one.

    Example:
    -------
        Buffer(
            on_flush=then(process_data, also(print, log)),
            max=64
        )

    """

    def function(data: Any) -> Any:
        for action in actions:
            data = action(data)
        return data

    return function
