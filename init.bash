#!/bin/bash

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

echo "Starting Raspberry Pi Pico SDK setup on macOS..."

# Step 1: Install Homebrew if not present
if ! command_exists brew; then
    echo "Homebrew not found. Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    # Add Homebrew to PATH immediately (for Apple Silicon or Intel)
    if [ -f /opt/homebrew/bin/brew ]; then
        eval "$(/opt/homebrew/bin/brew shellenv)"
    else
        eval "$(/usr/local/bin/brew shellenv)"
    fi
else
    echo "Homebrew already installed."
fi

# Step 2: Install Xcode Command Line Tools (for git, compilers, etc.)
if ! xcode-select -p >/dev/null 2>&1; then
    echo "Installing Xcode Command Line Tools..."
    xcode-select --install
fi

# Step 3: Install required Homebrew packages
echo "Installing required packages: cmake, libusb, pkg-config..."
brew install cmake libusb pkg-config

# Step 4: Install ARM GCC toolchain via Cask
echo "Installing gcc-arm-embedded via Cask..."
brew install --cask gcc-arm-embedded

# Step 5: Clone Pico SDK and examples if not present
PICO_DIR="$HOME/pico"
if [ ! -d "$PICO_DIR/pico-sdk" ]; then
    echo "Cloning Pico SDK and examples to $PICO_DIR..."
    mkdir -p "$PICO_DIR"
    cd "$PICO_DIR"
    git clone https://github.com/raspberrypi/pico-sdk.git --branch master
    cd pico-sdk
    git submodule update --init
    cd ..
    git clone https://github.com/raspberrypi/pico-examples.git --branch master
else
    echo "Pico SDK already cloned in $PICO_DIR."
fi

# Step 6: Reset environment variables (backup .zshrc and remove old Pico/ARM entries)
ZSHRC="$HOME/.zshrc"
if [ -f "$ZSHRC" ]; then
    echo "Backing up $ZSHRC to $ZSHRC.bak..."
    cp "$ZSHRC" "$ZSHRC.bak"
    echo "Removing old Pico SDK and ARM GCC path entries from $ZSHRC..."
    sed -i '' '/PICO_SDK_PATH/d' "$ZSHRC"
    sed -i '' '/ARM\/bin/d' "$ZSHRC"  # Remove old ARM path if present
else
    echo "Creating new $ZSHRC..."
    touch "$ZSHRC"
fi

# Step 7: Set new environment variables
echo "Adding new environment variables to $ZSHRC..."
echo 'export PICO_SDK_PATH="$HOME/pico/pico-sdk"' >> "$ZSHRC"
echo 'export PATH="/Applications/ARM/bin:$PATH"' >> "$ZSHRC"

# Step 8: Source the updated .zshrc to apply changes
echo "Sourcing $ZSHRC to apply changes..."
source "$ZSHRC"

# Verification
echo "Setup complete! Verifying installations..."
arm-none-eabi-gcc --version || echo "Error: arm-none-eabi-gcc not found. Check PATH."
echo "PICO_SDK_PATH: $PICO_SDK_PATH"
echo "You can now build examples: cd $PICO_DIR/pico-examples/build; cmake ..; make"
echo "If issues persist, check the backup $ZSHRC.bak or run 'source $ZSHRC' in new terminals."
