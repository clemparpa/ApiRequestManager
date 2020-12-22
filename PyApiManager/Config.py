class Config:
    """Config Object For an Api

    Object that store Api configurations that will be needed
    to execute requests

    Args:

        name(String: Required):

            string to reference a Config api object
            don't call 2 api with the same name or
            an api config will be delete

        base_url(String: Required):

            url common part for all your requests with this api
            ex

                "https://api" will allow to create requests like
                    -->  "https://api/firstpath"
                    -->  "https://api/secondpath"
                    -->  "https://api/thirdpath"


        auth(Map: Optional):

            if you need an authentication for the api
            provide their the authentication header field
            (ex: Authorization) and the token
            like

                auth -> {'the auth field here': 'Your token here'}


        headers(Map: Optional):

            if you need to provide other headers to api
            do it like 'auth' argument (multiple header key/value accepted)
            ex

                header -> {
                    'first_header_field':'first_header_val',
                    'second_header_field':'second_header_val',
                    etc...
                }

    """

    name: str
    base_url: str
    auth: dict
    headers: dict

    def __init__(self, name: str, base_url: str, auth: dict = None, headers: dict = None):
        self.name = name
        self.base_url = base_url
        self.auth = auth
        self.headers = headers


    def __eq__(self, other):
        """ '==' operator implemented: same 'name' attribut -> equality """
        return self.name == other.name


    def __repr__(self):
        return "Config(name=%r, base_url=%r, auth=%r, headers=%r)" % (self.name, self.base_url, self.auth, self.headers)


    def __hash__(self):
        """
        hash implemented like: same 'name' attribut -> same hash
        ApiConfig delete dupplicates names for Config objects
        so Config objects in ApiConfigs.configs have unique hash
        """
        return hash(self.name)
