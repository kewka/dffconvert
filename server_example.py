import os
import socket
import config

EXAMPLE_FILE = os.path.join(os.path.dirname(__file__), 'example/ballas3.dff')
EXAMPLE_OBJ = os.path.join(os.path.dirname(
    __file__), 'example/server_ballas3.obj')


def server_example():
    # Get dff size.
    dff_size = os.path.getsize(EXAMPLE_FILE)
    connection = socket.create_connection(config.SERVER_ADDRESS)
    # Send dff size.
    connection.send(dff_size.to_bytes(config.HEADER_SIZE,
                                      config.HEADER_BYTEORDER))

    # Send dff data.
    with open(EXAMPLE_FILE, 'rb') as dff:
        while True:
            chunk = dff.read()

            if not chunk:
                break

            connection.send(chunk)

    # Read obj_size.
    obj_size = int.from_bytes(connection.recv(
        config.HEADER_SIZE), config.HEADER_BYTEORDER)
    print('OBJ size: %d' % obj_size)
    # Read obj data.
    obj_data = connection.recv(obj_size)

    # Write obj data to file.
    bytes_written = 0

    with open(EXAMPLE_OBJ, 'wb') as obj:
        while bytes_written < obj_size:
            bytes_written += obj.write(obj_data)

    connection.close()


if __name__ == '__main__':
    server_example()
