# Import the necessary libraries
import zenoh, time

# This is the callback function that will be executed every time a message is received.
# Zenoh calls this function automatically with the received data.
def listener(sample):
    # 'sample' is an object containing the received data and its metadata.
    # We print the kind of sample (e.g., PUT), the key expression it was sent to,
    # and the actual data (payload), converted to a string.
    print(f"Received {sample.kind} ('{sample.key_expr}': '{sample.payload.to_string()}')")

# The main entry point of the script.
if __name__ == "__main__":
    # Open a Zenoh session.
    # The configuration is loaded from 'client_mtls.json5', which sets up the
    # secure mTLS connection, including the client's certificates and keys.
    # The 'with' statement ensures the session is properly closed when exiting.
    with zenoh.open(zenoh.Config.from_file("client_mtls.json5")) as session:
        # Declare a subscriber for a specific key expression.
        # This tells Zenoh: "I am interested in any data published on 'myhome/kitchen/temp'".
        # The 'listener' function is passed as the callback to handle incoming data.
        sub = session.declare_subscriber('myhome/kitchen/temp', listener)
        # Inform the user that the subscriber is active and how to stop it.
        print("Subscriber running, press Ctrl+C to quit.")
        # This loop keeps the script alive indefinitely to continue receiving messages.
        try:
            while True:
                time.sleep(1)
        # When the user presses Ctrl+C, the KeyboardInterrupt is caught,
        # allowing the 'with' block to exit gracefully and close the session.
        except KeyboardInterrupt:
            pass