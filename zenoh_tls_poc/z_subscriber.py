import zenoh, time

def listener(sample):
    print(f"Received {sample.kind} ('{sample.key_expr}': '{sample.payload.to_string()}')")

if __name__ == "__main__":
    with zenoh.open(zenoh.Config.from_file("client_mtls.json5")) as session:
        sub = session.declare_subscriber('myhome/kitchen/temp', listener)
        print("Subscriber running, press Ctrl+C to quit.")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            pass