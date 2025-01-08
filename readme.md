# A simple CLI to do list app for linux

## Installation

⚠️ Before installing these, you may have python and pip installed on your machine even if install.sh will install it for you

To install as a terminal command type this in your terminal
```bash
git clone https://github.com/griby51/2doList
cd 2doList
chmod +x install.sh
sudo ./install.sh
```
Or you can use it as python file by executing `main.py` with these commands :
```bash
pip install prompt-toolkit
python main.py
```

You can remove it by go to 2dolist directory or if you delete it cloning like installing command and type this in your terminal
```bash
chmod +x uninstall.sh
sudo ./uninstall.sh
```

## Usage

To use my simple 2doList app, simply type `tdl` in your terminal, the shortcut are those or now you can start it with your application launcher like rofi or dmenu :

| Why is it for                                | Shortcut |
|----------------------------------------------|----------|
| Quit                                         | `Ctrl-q` |
| Modify list or task                          | `,`      |
| Add list or task                             | `+`      |
| Remove list or task                          | `-`      |
| Set as done, confirm name or enter task area | `Enter`  |
| Quit task area                               | `Escape` |
