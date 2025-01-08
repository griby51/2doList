#!/bin/bash

SCRIPT_NAME="main.py"
COMMAND_NAME="tdl"
TARGET_DIR="/usr/local/bin"
SHARE_DIR="/usr/local/share/$COMMAND_NAME"
PIP_REQUIREMENTS="requirements.txt"
LOGO_DIR="/usr/share/icons"
DESKTOP_DIR="$HOME/.local/share/applications"

insall_pip(){
    echo "Installing pip"
    if command -v apt > /dev/null; then
        sudo apt install -y python3-pip
    elif command -v dnf > /dev/null; then
        sudo dnf install -y python3-pip
    elif command -v yum > /dev/null; then
        sudo yum install -y python3-pip
    elif command -v pacman > /dev/null; then
        sudo pacman -S --noconfirm python-pip
    elif command -v zypper > /dev/null; then
        sudo zypper install -y python3-pip
    else
        echo "Unsupported package manager. Install pip manually."
        exit 1
    fi
}

if [ ! -f "$SCRIPT_NAME" ] || [ ! -f "$PIP_REQUIREMENTS" ]; then
    echo "$SCRIPT_NAME or $DATA_FILE or $PIP_REQUIREMENTS not found"
    exit 1
fi

echo "Installing $COMMAND_NAME"

echo "Creating directory"
sudo mkdir -p "$SHARE_DIR"

echo "Copying file"
sudo cp "$SCRIPT_NAME" "$SHARE_DIR"
sudo cp "logo.png" "$LOGO_DIR/$COMMAND_NAME.png"
sudo cp "tdl.desktop" "$DESKTOP_DIR/$COMMAND_NAME.desktop"

sudo chmod +x "$SHARE_DIR/$SCRIPT_NAME"

echo "Installing requirements"

if ! command -v pip > /dev/null; then
    insall_pip
fi 

pip install -r "$PIP_REQUIREMENTS" --break-system-packages
if [ $? -ne 0 ]; then
    echo "Failed to install requirements"
    exit 1
fi

sudo bash -c "cat > $TARGET_DIR/$COMMAND_NAME" <<EOL
#!/bin/bash
python3 $SHARE_DIR/$SCRIPT_NAME \"\$@\"
EOL

sudo chmod +x $TARGET_DIR/$COMMAND_NAME

if [[ -f "$TARGET_DIR/$COMMAND_NAME" ||  -f "$LOGO_DIR" || -f "$DESKTOP_DIR" || -f "$SHARE_DIR/$SCRIPT_NAME" ]]; then
    echo "$COMMAND_NAME installed successfully"
else
    echo "Failed to install $COMMAND_NAME"
    exit 1
fi
