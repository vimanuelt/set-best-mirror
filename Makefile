# Define variables
PYTHON := python3
PYINSTALLER := $(PYTHON) -m PyInstaller
SCRIPT := set-best-mirror.py
BINARY_NAME := set-best-mirror
SPEC_FILE := $(BINARY_NAME).spec
DIST_DIR := dist
BUILD_DIR := build
LOG_DIR := /var/log

# Default target
all: install

# Create a spec file if it doesn't exist
spec:
	$(PYINSTALLER) --name $(BINARY_NAME) --onefile $(SCRIPT)

# Build the binary using the spec file
build: spec
	$(PYINSTALLER) $(SPEC_FILE)
	@echo "Build completed. Binary is located in $(DIST_DIR)/$(BINARY_NAME)"

# Install the binary to /usr/local/bin/
install: build
	@if [ ! -d $(LOG_DIR) ]; then \
	    sudo mkdir -p $(LOG_DIR); \
	    sudo chown root:root $(LOG_DIR); \
	    sudo chmod 755 $(LOG_DIR); \
	fi
	sudo cp $(DIST_DIR)/$(BINARY_NAME) /usr/local/bin/
	@echo "$(BINARY_NAME) has been installed to /usr/local/bin/"

# Clean up build artifacts
clean:
	rm -rf $(BUILD_DIR) $(DIST_DIR) $(SPEC_FILE)

# Run the script directly for testing
run:
	$(PYTHON) $(SCRIPT)

# Help target to show available commands
help:
	@echo "Available targets:"
	@echo "  make all      - Build and install the binary (default)"
	@echo "  make spec     - Generate spec file for PyInstaller"
	@echo "  make build    - Build the binary"
	@echo "  make install  - Install the binary to /usr/local/bin/"
	@echo "  make clean    - Remove build artifacts"
	@echo "  make run      - Run the Python script directly for testing"

.PHONY: all spec build install clean run help
