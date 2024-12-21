#!/bin/bash

SCRIPT_NAME="main.py"
COMMAND_NAME="tdl"
TARGET_DIR="/usr/local/bin"
SHARE_DIR="/usr/local/share/$COMMAND_NAME"
PIP_REQUIREMENTS="requirements.txt"

if [ ! -f "$SCRIPT_NAME" ] || [ ! -f "$PIP_REQUIREMENTS" ]; then
    echo "$SCRIPT_NAME or $DATA_FILE or $PIP_REQUIREMENTS not found"
    exit 1
fi

echo "Installing $COMMAND_NAME"

sudo mkdir -p "$SHARE_DIR"

sudo cp "$SCRIPT_NAME" "$SHARE_DIR"

sudo chmod +x "$SHARE_DIR/$SCRIPT_NAME"

echo "Installing requirements"

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

if [ -f "$TARGET_DIR/$COMMAND_NAME" ]; then
    echo "$COMMAND_NAME installed successfully"
else
    echo "Failed to install $COMMAND_NAME"
    exit 1
fi
