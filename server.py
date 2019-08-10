'''
dff2obj-server.
This is a small TCP server to convert DFF to OBJ files.

Request:
[dff_size] - Header with DFF file size. Size: {config.HEADER_SIZE} bytes (Max: {config.MAX_FILE_SIZE}).
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
import config


def handle_request(client: socket.socket):
    # Generate file id.
    id = str(uuid.uuid1())
    # Path to DFF file.
    dff_path = os.path.join(config.TEMP_DIR, id + '.dff')
    # Path to OBJ file.
    obj_path = os.path.join(config.TEMP_DIR, id + '.obj')
    # Set the socket timeout.
    client.settimeout(config.SOCKET_TIMEOUT_SECONDS)

    print('Temporary file id: %s' % id)

    def clean():
        try:
            # Remove temporary files.
            for temp_file in glob.glob(os.path.join(config.TEMP_DIR, id + '*')):
                os.remove(temp_file)

            # Close the client socket.
            client.close()
            print('[%s] Cleaning complete.' % id)
        except Exception as e:
            print('[%s] Cleaning error: %s' % (id, str(e)))

    try:
        # Get header bytes.
        header = client.recv(config.HEADER_SIZE)
        # Get file size from header.
        filesize = int.from_bytes(header, config.HEADER_BYTEORDER)

        # Check file size.
        if filesize > config.MAX_FILE_SIZE:
            return clean()

        # Number of bytes read.
        bytes_read = 0

        with open(dff_path, 'wb') as dff:
            while bytes_read < filesize:
                remaining = filesize - bytes_read
                chunk = client.recv(config.BUFFER_SIZE if remaining >
                                    config.BUFFER_SIZE else remaining)

                bytes_read += len(chunk)
                dff.write(chunk)

        # Call dff2obj process.
        # Clean if the process ends with a code not 0 or the OBJ file was not created.
        if subprocess.call([config.DFF2OBJ, dff_path, obj_path]) or not os.path.isfile(obj_path):
            return clean()

        # Send OBJ file to the client.
        with open(obj_path, 'rb') as obj:
            while True:
                chunk = obj.read(config.BUFFER_SIZE)

                if not chunk:
                    break

                client.send(chunk)

        return clean()
    except socket.timeout:
        print('[%s] Socket timeout error' % id)
        return clean()


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(config.SERVER_ADDRESS)
    server.listen()
    print('dff2obj-server running on %s:%d' % config.SERVER_ADDRESS)

    while True:
        client, addr = server.accept()
        print('New client')
        threading.Thread(target=handle_request, args=(client,)).start()

    server.close()


if __name__ == '__main__':
    main()
