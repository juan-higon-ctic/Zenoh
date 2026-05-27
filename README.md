# Zenoh Secure Communication (mTLS) Proof of Concept

This project demonstrates a secure publish-subscribe (Pub/Sub) system using Zenoh, protected with Mutual TLS (mTLS) for robust, bidirectional authentication.

## Overview

The system consists of three main components:

1.  **Zenoh Router (`zenohd.exe`)**: Acts as the central message broker. It is configured to enforce mTLS, meaning it will only communicate with clients that present a valid and trusted certificate.
2.  **Sensor (`z_sensor.py`)**: A Python script that simulates a temperature sensor. It acts as a Zenoh **publisher**, sending data to a specific key. It must authenticate itself to the router using its own certificate.
3.  **Subscriber (`z_subscriber.py`)**: A Python script that acts as a Zenoh **subscriber**. It listens for data on the temperature key. It must also authenticate itself to the router to receive messages.

The communication flow is as follows: `Sensor -> Router -> Subscriber`, with all links secured by mTLS.

## Security

This project implements **Mutual TLS (mTLS)**. Unlike standard TLS where only the client verifies the server, mTLS ensures that:

*   The **client** (sensor/subscriber) verifies the **router's** identity.
*   The **router** verifies the **client's** identity.

This prevents unauthorized devices from either publishing or subscribing to data on the network. Certificates are generated using `minica`, a simple CA tool.

## How to Run

Follow these steps to run the mTLS-secured system.

### Prerequisites

*   Python 3.x
*   Zenoh Python library: `pip install eclipse-zenoh`
*   The Zenoh router executable (`zenohd.exe`) placed in this directory.
*   The `minica` executable available in your system's PATH or in this directory.

### 1. Generate Certificates

If you haven't already, generate the required certificates for the server (router) and the client (apps).

```powershell
# Create the main directory for mTLS certificates
mkdir mtls_certs
cd mtls_certs

# Create and generate certificates for the server (router)
mkdir server
cd server
minica --domains localhost
cd ..

# Create and generate certificates for the client (sensor/subscriber)
mkdir client
cd client
minica --domains localhost
cd ..

# Return to the project root
cd ..
```

### 2. Run the System

Open three separate terminals in this project's root directory (`C:\Codigos\5-Concepto Zenoh\zenoh_tls_poc`).

**Terminal 1: Start the Router**
```powershell
# This command runs the Zenoh router executable and tells it to use your JSON5 file for configuration.
.\zenohd.exe -c router_mtls.json5
```

**Terminal 2: Start the Subscriber**
```powershell
# Note: Use 'python' and not 'python3', especially when inside a virtual environment on Windows.
python z_subscriber.py
```

**Terminal 3: Start the Sensor**
```powershell
python z_sensor.py
```

### 3. Verify

Observe the output in the subscriber's terminal (Terminal 2). You should see it receiving temperature data from the sensor, confirming that the secure mTLS communication is working correctly.