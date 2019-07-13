'''
dff2obj-server.
This is a small TCP server to convert DFF to OBJ files.

Request:
[dff_size] - Header with DFF file size. Size: 8 bytes (Max value: see MAX_FILE_SIZE).
[dff_data] - The contents of the DFF file. Size: [dff_size] bytes.

Response:
[obj_data] - The contents of the OBJ file.
'''

import socket
import threading
import uuid
import os
import glob
import subprocess

SERVER_HOST = os.getenv('HOST', '0.0.0.0')
SERVER_PORT = int(os.getenv('PORT', '8000'))
SERVER_ADDRESS = (SERVER_HOST, SERVER_PORT)

# Maximum size of DFF file (1 MB).
MAX_FILE_SIZE = 1024 * 1024
# Buffer size (64 KB).
BUFFER_SIZE = 1024 * 64
# Socket timeout (5 seconds).
SOCKET_TIMEOUT_SECONDS = 5

# Header size (4 bytes).
HEADER_SIZE = 4
# Header byte order (Big-Endian).
HEADER_BYTEORDER = 'big'

# Path to the temporary directory.
TEMP_DIR = os.path.join(os.path.dirname(__file__), 'temp')
# Path to executable dff2obj.
DFF2OBJ = os.path.join(os.path.dirname(__file__), 'dff2obj')


def handle_request(client: socket.socket):
    # Generate file id.
    id = str(uuid.uuid1())
    # Path to DFF file.
    dff_path = os.path.join(TEMP_DIR, id + '.dff')
    # Path to OBJ file.
    obj_path = os.path.join(TEMP_DIR, id + '.obj')
    # Set the socket timeout.
    client.settimeout(SOCKET_TIMEOUT_SECONDS)

    print('Temporary file id: %s' % id)

    def clean():
        try:
            # Remove temporary files.
            for temp_file in glob.glob(os.path.join(TEMP_DIR, id + '*')):
                os.remove(temp_file)

            # Close the client socket.
            client.close()
            print('[%s] Cleaning complete.' % id)
        except Exception as e:
            print('[%s] Cleaning error: %s' % (id, str(e)))

    try:
        # Get header bytes.
        header = client.recv(HEADER_SIZE)
        # Get file size from header.
        filesize = int.from_bytes(header, HEADER_BYTEORDER)

        # Check file size.
        if filesize > MAX_FILE_SIZE:
            return clean()

        # Number of bytes read.
        bytes_read = 0

        with open(dff_path, 'wb') as dff:
            while bytes_read < filesize:
                remaining = filesize - bytes_read
                chunk = client.recv(BUFFER_SIZE if remaining >
                                    BUFFER_SIZE else remaining)

                bytes_read += len(chunk)
                dff.write(chunk)

        # Call dff2obj process.
        # Clean if the process ends with a code not 0 or the OBJ file was not created.
        if subprocess.call([DFF2OBJ, dff_path, obj_path]) or not os.path.isfile(obj_path):
            return clean()

        # Send OBJ file to the client.
        with open(obj_path, 'rb') as obj:
            while True:
                chunk = obj.read(BUFFER_SIZE)

                if not chunk:
                    break

                client.send(chunk)

        return clean()
    except socket.timeout:
        print('[%s] Socket timeout error' % id)
        return clean()


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(SERVER_ADDRESS)
    server.listen()
    print('dff2obj-server running on %s:%d' % SERVER_ADDRESS)

    while True:
        client, addr = server.accept()
        print('New client')
        threading.Thread(target=handle_request, args=(client,)).start()

    server.close()


if __name__ == '__main__':
    main()
