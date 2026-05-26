# Import the necessary libraries
import zenoh, random, time

# Initialize the random number generator.
# Calling it without arguments uses the current system time, which is the default.
random.seed()

# This function simulates reading a temperature value from a physical sensor.
def read_temp():
    # Returns a random integer between 15 and 30.
    return random.randint(15, 30)

# The main entry point of the script.
if __name__ == "__main__":
    # Open a Zenoh session.
    # The configuration is loaded from 'client_mtls.json5', which sets up the
    # secure mTLS connection, including the client's certificates and keys.
    # The 'with' statement ensures the session is properly closed when exiting.
    with zenoh.open(zenoh.Config.from_file("client_mtls.json5")) as session:
        # Define the key expression where the data will be published.
        key = 'myhome/kitchen/temp'
        # Declare a publisher for the specified key.
        pub = session.declare_publisher(key)
        # Start an infinite loop to continuously publish data.
        while True:
            # Read a new temperature value.
            t = read_temp()
            # Format the temperature as a string to be sent.
            buf = f"{t}"
            # Print to the console what is being sent.
            print(f"Putting Data ('{key}': '{buf}')...")
            # Publish the data to the Zenoh network on the declared key.
            pub.put(buf)
            # Wait for 1 second before the next iteration.
            time.sleep(1)