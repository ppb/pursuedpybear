class BadEventHandlerException(TypeError):

    def __init__(self, instance, method, event):
        object_type = type(instance)
        event_type = type(event)
        o_name = object_type.__name__
        e_name = event_type.__name__
        article = ['a', 'an'][int(e_name.lower()[0] in "aeiou")]

        message = f"""
{o_name}.{method}() signature incorrect, it should accept {article} {e_name} object and a signal function.

{e_name} is a dataclass that represents an event. Its attributes 
tell you about the event.

The signal function is a function you can call that accepts an event instance
as its only parameter. Call it to add an event to the queue. You don't have to
use it, but it is a mandatory argument provided by ppb.

It should look like this:

def {method}({e_name.lower()}_event: {e_name}, signal_function):
    (Your code goes here.)
"""
        super().__init__(message)


class BadChildException(Exception):
    """Raised when a type (as opposed to an instance object) is used as a child."""

    def __init__(self, child):
        type_name = child.__name__
        message = (
            f"Argument child must be an instance object"
            f" -- you passed in a type, {type_name}, instead."
            f"\nThis probably isn't what you intended."
            f"\n\nTry instantiating it, like: {type_name}()"
        )
        super().__init__(message)
