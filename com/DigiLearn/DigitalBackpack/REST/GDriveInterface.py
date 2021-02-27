import socket

# this might have to be a non-static class cause there might need to have different sockets/ports/etc
# for different stuff
# this also might just be a general "interface" class, not just for the gdrive inter so ya well see

_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
_socket_out_port = None
_socket_in_port = None
# this might be the same as _SCOPES but im not sure yet
# might also be googleapis.com/drive/v3, still need to figure that out
_socket_host = None

def getrequest(request: str):
    # before anything...

    # psure i need to _socket.connect((target_host, target_port)) here
    #   there might be an issue here with requests getting responses from other requests... hmmmm....
    #   probably gonna need a parameter for this instead of a global variable
    #   possibly for all the socket stuff

    _socket.connect((_socket_host, _socket_out_port))

    _socket.send(request.encode())

    # receive response
    response = _socket.recv(_socket_in_port)  # needs a port number, idk where imma get that
    http_response = repr(response)
    if "HTTP/1.1 200 OK" in http_response:
        return response
    else:
        # need to throw an error here
        return None
