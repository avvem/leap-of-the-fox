# 🎮 Pygame CE Platformer

A platformer game built using [Pygame Community Edition (pygame-ce)](https://pyga.me/docs/).  
Tested and developed on macOS M1, should also run on Linux and Windows with Python 3.11+.

---

## 📁 Project Structure

PYGAME/
├── assets/                     # Game assets (images, sounds)
│   ├── bg.png
│   ├── bullet.png
│   ├── dying.mp3
│   ├── fox_breathing.mp3
│   ├── fox_eating.mp3
│   ├── fox_hit.mp3
│   ├── fox_jumping.mp3
│   ├── fox.png
│   ├── hunter_shooting.mp3
│   ├── hunter_spawning.mp3
│   ├── hunter.png
│   └── squirrel.png
│
├── pygame-env/                 # Python virtual environment (ignored by Git)
│
├── sound_files/               # FL Studio files (ignored by Git)
│
├── src/                        # All source code
│   ├── explosion.py
│   ├── fox.py
│   ├── hunter.py
│   ├── main.py
│   ├── muzzle_flash.py
│   ├── projectile.py
│   └── squirrel.py
│
├── .gitignore                  # Git ignore rules
├── game_icon.icns              # Optional icon file
├── high_scores.txt             # Game score persistence
├── requirements.txt            # Python dependencies


---

## 🚀 Getting Started

These steps assume you're using **macOS** or **Linux**. For Windows, use Git Bash or WSL.

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/pygame-ce-platformer.git
cd pygame-ce-platformer

2. Create Virtual Environment
bash
Copy
Edit
python3 -m venv pygame-env
source pygame-env/bin/activate
3. Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt
4. Run the Game
bash
Copy
Edit
cd src
python main.py
