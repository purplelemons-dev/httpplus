
"""
Responsible for defining communication objects and functions.
"""

from json import dumps, loads
from dataclasses import dataclass
from http.server import BaseHTTPRequestHandler

class RouteExistsError(Exception):
    """Raised when a route already exists."""
    def __init__(self, route:str=...):
        super().__init__(f"Route {route} already exists." if route else "Route already exists.")

@dataclass
class Route:
    """Custom dataclass for optimizing route creation, readability, and resolution.

    Attributes:
        `send_to (str)`: The directory to respond with in the form of `./path/to/directory/`, `path/to/file.ext`, etc..
        `route_type (str)`: The type of route. Can be either `pages`, `errors`, or `static`.
        `content (str)`: The content to respond with. Only used for `static` routes.
        `content_type (str)`: The content type to respond with. Only used for `static` routes.
    """
    send_to:str
    route_type:str

    @property
    def full_path(self) -> str:
        """Returns the full path to the file to respond with."""
        return f"./{self.route_type}{self.send_to}"

class Request:
    """
    Request object, passed into HTTP method listeners as the first argument.
    """
    class Params:
        """
        Accessed from `Request.params`.
        
        Given the route `/example/:id`, you may use `Request.params.id`.
        However, if the route is `/example/example-id`, then you must use either
        `Request.params["example-id"]` or `Request.params.get("example-id")`.
        """
        def __init__(self, kwargs:dict[str,str]):
            for param, value in kwargs.items():
                # Fun fact, setattr is ~39% faster than __setattr__.
                setattr(self, param, value)
        
        def __getitem__(self, key:str) -> str:
            return getattr(self, key)
        def get(self, param:str) -> str:
            return getattr(self, param)
        def __repr__(self) -> str:
            return f"Request.params({self.__dict__})"
        def __str__(self) -> str:
            return self.__repr__()
        def __eq__(self, o:object) -> bool:
            if isinstance(o, Request.params):
                return self.__repr__() == o.__repr__()
            return False

    def __init__(self, request:BaseHTTPRequestHandler, /, *, params:dict[str,str]):
        self.request = request
        self.path = request.path
        self.method = request.command
        self.headers = request.headers
        self.body = request.rfile.read(int(request.headers.get("Content-Length", 0)))
        self.ip, self.port = request.client_address
        self.params = self.Params(params)

    # Dunder pog
    def __repr__(self) -> str:
        return f"Request({self.method=}, {self.path=}, {self.headers=}, {self.body=})"
    def __str__(self) -> str:
        return self.__repr__()
    def __eq__(self, o:object) -> bool:
        if isinstance(o, Request):
            return self.__repr__() == o.__repr__()
        return False
    def __ne__(self, o:object) -> bool:
        return not self.__eq__(o)
    def __hash__(self) -> int:
        return hash(self.__repr__())
    def __iter__(self) -> "Request":
        return self
    def __next__(self) -> "Request":
        raise StopIteration
    def __len__(self) -> int:
        return 0
    def __bool__(self) -> bool:
        return True

    def get_header(self, header:str) -> str:
        return self.headers[header]

    @property
    def json(self) -> dict:
        return loads(self.body)

    @property
    def text(self) -> str:
        return self.body.decode()
    
    def param(self, param:str) -> str:
        return self.params[param]


class Response:
    """
    Response object, passed into HTTP method listeners as the second argument.
    
    You *must* return this from the HTTP method listener function.
    """
    def __init__(self, response:BaseHTTPRequestHandler):
        self.response = response
        self.headers:dict[str,str] = {}
        self.body:str = ""
        self.status_code = 200
        self.isLinked = False
        self._route: Route

    def set_header(self, header:str, value:str) -> "Response":
        self.headers[header] = value
        return self

    def set_body(self, body:bytes|str|dict) -> "Response":
        """
        Automatically pareses the body into bytes, and sets the Content-Type header to application/json if the body is a dict.
        Will be overwritten if `Response

        Args:
            `body (bytes|str|dict)`: The body of the response.
        """
        if isinstance(body, dict):
            self.set_header("Content-Type", "application/json")
            self.body = dumps(body)
        elif isinstance(body, bytes):
            self.body = body.decode()
        else:
            self.body = body
        return self

    def status(self,code:int) -> "Response":
        """
        Sets the status code of the response.

        Args:
            `code (int)`: The status code to set.
        """
        self.status_code = code
        return self

    def redirect(self,to:str) -> "Response":
        """
        Will redirect client to the specified destination.

        Args:
            `to (str)`: The path to route to.
        """
        self.headers["Location"] = to
        self.status_code = 302 # Found == temporary redirect
        self.isLinked = True
        return self

    def __call__(self) -> None:
        """
        Sends the response to the client. You should not call this manually unless you are modifying `http_plus.Server`.
        """
        self.response.send_response(self.status_code)
        for header, value in self.headers.items():
            self.response.send_header(header, value)
        self.response.end_headers()
        if not self.isLinked:
            self.response.wfile.write(self.body.encode())
        return
