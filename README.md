# 🎮 Pygame CE Platformer

A platformer game built using [Pygame Community Edition (pygame-ce)](https://pyga.me/docs/).  
Tested and developed on macOS M1, should also run on Linux and Windows with Python 3.11+.

---

## 🚀 Getting Started

These steps assume you're using **macOS** or **Linux**. For Windows, use Git Bash or WSL.

If these instructions fail, please see pygame-ce git repo, pygame-ce website or instructions on specific problem for solution.

### 1. Clone the Repository

```bash
git clone https://github.com/avvem/leap-of-the-fox.git
cd leap-of-the-fox
```

### 2. Create Virtual Environment
```bash
python3 -m venv pygame-env
source pygame-env/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```
Also install pygame-ce here (see below).

### 4. Run the Game
```bash
cd src
python main.py
```

---

## 🧰 Requirements
Python 3.11+

Pygame Community Edition (pygame-ce)

### 🔧 Installing pygame-ce
Use pip to install Pygame CE:

```bash
pip install pygame-ce
```
Make sure your virtual environment is activated before running the above command.

### 🛠 SDL2 Libraries (macOS/Linux only)
On macOS (via Homebrew):

```bash
brew install sdl2 sdl2_image sdl2_mixer sdl2_ttf
```
Linux users should install the SDL2 development libraries using their package manager, e.g.:

```bash
sudo apt install libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev
```
Windows users do not need to install SDL2 separately — it comes bundled with pygame-ce.
