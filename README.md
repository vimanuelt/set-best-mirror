# Set Best Mirror

This script ranks the performance of different GhostBSD package repository mirrors based on ping times and download speeds, then updates the configuration to use the best performing mirror.

## Overview

- **Purpose**: To automatically select and configure the best package repository mirror for GhostBSD systems.
- **Environment**: Designed for GhostBSD (FreeBSD based) with `python3`, `ping`, and `wget` installed.

## Installation

### From Source

- Clone the repository:
   ```bash
   git clone https://github.com/vimanuelt/set-best-mirror.git
   ```
   ```bash
   cd set-best-mirror
   ```

- Build and install using the Makefile:
    ```bash
    make
    ```
    ```bash
    sudo make install
   ```
    This will compile the Python script into an executable and place it in /usr/local/bin/.


Note: Running with sudo is necessary as it modifies system configuration files.

## Usage

- Run the Script: 
    ```bash
    sudo set-best-mirror
    ```
Logging: Logs are stored in /var/log/set-best-mirror.log.


## Configuration

Mirrors: Currently configured mirrors are hardcoded but can be easily modified in set-best-mirror.py.


## Troubleshooting

Permissions: Ensure you have the necessary permissions to write to /usr/local/etc/pkg/repos/ and /var/log/.

Dependencies: You need python3, ping, and wget installed on your system.


## License
This project is licensed under the BSD 3-Clause License. See the LICENSE file for details.

## Contributing
Contributions are welcome! Please fork the repository and submit pull requests for any improvements or additional features.

- Bug Reports: Log issues on the GitHub Issues page.

- Feature Requests: Similarly, use the Issues page to suggest new features.


## Acknowledgements

Thanks to the GhostBSD community for providing the resources to test and improve this utility.

