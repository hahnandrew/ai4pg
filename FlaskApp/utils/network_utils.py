def is_internet_available():
    try:
        # Attempt to create a socket connection to a well-known host (e.g., Google DNS)
        socket.create_connection(("8.8.8.8", 53), timeout=5)
        return True
    except OSError:
        return False
