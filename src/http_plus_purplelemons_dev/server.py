

from dataclasses import dataclass


@dataclass
class Route:
    """Custom dataclass for optimizing route creation, readability, and resolution.
    Functional routes should include a `Route.func` attribute.

    Attributes:
        `request_from (str)`: The path to respond to.
        `send_to (str)`: The directory to respond with in the form of `./path/to/directory/`.
        `route_type (str)`: The type of route. Can be either `pages`, `errors`, or `func`.
    """
    request_from:str
    send_to:str
    route_type:str

class RouteExistsError(Exception):
    """Raised when a route already exists."""
    def __init__(self):
        super().__init__("Route already exists.")


class Server:

    def __init__(self, host:str, port:int, *, debug:bool=False, **kwargs):
        """Initializes the server.
        Args:
            `host (str)`: The host to listen on.
            `port (int)`: The port to listen on.
            `debug (bool)`: Whether or not to print debug messages.
        """
        self.host = host
        self.port = port
        self.debug = debug


    ### DECORATORS ###
    def all(path:str) -> function:
        """A decorator that adds a route to the server. Listens to all HTTP methods.
        Args:
            `path (str)`: The path to respond to.
        """
        def decorator(func:function):
            ...
        return decorator

    def get(path:str) -> function:
        """A decorator that adds a route to the server. Listens to GET requests.
        Args:
            `path (str)`: The path to respond to.
        """
        def decorator(func:function):
            ...
        return decorator

    def post(path:str) -> function:
        """A decorator that adds a route to the server. Listens to POST requests.
        Args:
            `path (str)`: The path to respond to.
        """
        def decorator(func:function):
            ...
        return decorator

    def put(path:str) -> function:
        """A decorator that adds a route to the server. Listens to PUT requests.
        Args:
            `path (str)`: The path to respond to.
        """
        def decorator(func:function):
            ...
        return decorator

    def delete(path:str) -> function:
        """A decorator that adds a route to the server. Listens to DELETE requests.
        Args:
            `path (str)`: The path to respond to.
        """
        def decorator(func:function):
            ...
        return decorator

    def patch(path:str) -> function:
        """A decorator that adds a route to the server. Listens to PATCH requests.
        Args:
            `path (str)`: The path to respond to.
        """
        def decorator(func:function):
            ...
        return decorator

    def options(path:str) -> function:
        """A decorator that adds a route to the server. Listens to OPTIONS requests.
        Args:
            `path (str)`: The path to respond to.
        """
        def decorator(func:function):
            ...
        return decorator
