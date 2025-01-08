#!/bin/bash

LOGO_DIR="/usr/share/icons"
DESKTOP_DIR="$HOME/.local/share/applications"
SCRIPT_NAME="main.py"
COMMAND_NAME="tdl"
SHARE_DIR="/usr/local/share/$COMMAND_NAME"
PIP_REQUIREMENTS="requirements.txt"

echo "Removing $COMMAND_NAME"

#!/bin/bash

# Afficher la question
read -p "Would you remove packages ? (y/n) " response

removing_packages(){
    echo "Removing packages"
    sudo pip uninstall -r "$PIP_REQUIREMENTS" --break-system-packages
}

# Vérifier la réponse
if [[ "$response" == "y" || "$response" == "Y" ]]; then
    removing_packages
elif [[ "$response" == "n" || "$response" == "N" ]]; then
    echo
else
    removing_packages
fi

echo "Deleting all tdl's directorys and files"
sudo rm -r "$SHARE_DIR"
sudo rm "$DESKTOP_DIR/$COMMAND_NAME.desktop"
sudo rm "$LOGO_DIR/$COMMAND_NAME.png"
sudo rm "/usr/local/bin/$COMMAND_NAME"
sudo rm "$HOME/.tdl_data.json"

if [[ -f "/usr/local/bin/$COMMAND_NAME" ||  -f "$LOGO_DIR" || -f "$DESKTOP_DIR" || -f "$SHARE_DIR/$SCRIPT_NAME" || -f "$HOME/.tdl_data.json" ]]; then
    echo "Failed to remove $COMMAND_NAME"
    exit 1
else
    echo "$COMMAND_NAME removed successfully"
fi