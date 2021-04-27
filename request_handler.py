import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from users import (get_all_users,
                    get_single_user,
                    create_user)

class HandleRequests(BaseHTTPRequestHandler):

    def parse_url(self, path):
       
        path_params = path.split("/")
        resource    = path_params[1]
        id          = None

        if "?" in resource:

            param       = resource.split("?")[1]  
            resource    = resource.split("?")[0]
            pair        = param.split("=")
            key         = pair[0]
            value       = pair[1]

            return ( resource, key, value )

        else:
            try:
                id = int(path_params[2])
            except IndexError:
                pass
            except ValueError:
                pass
            return (resource, id)

    def _set_headers(self, status):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers', 'X-Requested-With, Content-Type, Accept')
        self.end_headers()

    def do_GET(self):

        self._set_headers(200)
        response = {}
        parsed = self.parse_url(self.path)

        if len(parsed) == 2:
            (resource, id) = parsed

            if resource == "users":
                if id is not None:
                    response = f"{get_single_user(id)}"
                else:
                    response = f"{get_all_users()}"

        print(self.path)

        self.wfile.write(f"{response}".encode())
    
    def do_POST(self):
        self._set_headers(201)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)

        post_body = json.loads(post_body)

        (resource, id) = self.parse_url(self.path)

        new_resource_row = None

        # Add a new animal to the list. Don't worry about
        # the orange squiggle, you'll define the create_animal
        # function next.
        if resource == "users":
            new_resource_row = create_user(post_body)

        # Encode the new animal and send in response
        self.wfile.write(f"{new_resource_row}".encode())

def main():
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()

if __name__ == "__main__":
    main()