import os

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