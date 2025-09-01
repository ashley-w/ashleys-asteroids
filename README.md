# Ashley's Asteroids 🔺
*A Triangle Simulator*

A synthwave-themed asteroids game built with Python and pygame, featuring triangle-based collision detection, lumpy procedural asteroids, and explosive gameplay.

## 🎮 Play Online
**[🕹️ Play Now on itch.io](https://just-ashley.itch.io/ashleys-asteroids-a-triangle-simulator)**

No downloads needed - runs directly in your browser!

## 🚀 Features
- **Triangle collision detection** for precise gameplay
- **Procedural lumpy asteroids** for visual variety
- **Power-up system** with shields, speed boosts, rapid fire, spread shots, and bombs
- **Progressive difficulty** that scales over time
- **Synthwave aesthetic** with neon colors and retro styling
- **Web deployment ready** using WebAssembly

## 🎯 Controls
- **A/D** - Turn left/right
- **W/S** - Thrust forward/backward
- **SPACE** - Shoot
- **SHIFT** - Drop bomb (when available)
- **ESC** - Pause game

## 🛠️ Development

### Local Development
```bash
# Clone the repository
git clone https://github.com/ashley-w/ashleys-asteroids.git
cd ashleys-asteroids

# Install dependencies
pip install -r requirements.txt

# Run the game locally
python main.py
```

### Web Build & Deploy
```bash
# Install pygbag for web builds
pip install pygbag

# Build for web
pygbag main.py

# Web files are created in build/web/
# Upload to itch.io or other hosting service
```

## 📁 Project Structure
```
ashleys-asteroids/
├── src/
│   ├── core/           # Core game systems
│   ├── entities/       # Game objects (player, asteroids, etc.)
│   └── systems/        # Game systems (explosions, notifications, etc.)
├── main.py                    # Main game entry point
├── requirements.txt           # Python dependencies
├── pyproject.toml            # Project configuration
├── build/web/                # Web build output (pygbag)
└── README.md                 # This file
```

## 🎨 Tech Stack
- **Python 3.10+**
- **pygame 2.6+** for game engine
- **pygbag** for WebAssembly compilation  
- **itch.io** for web hosting

## 🔧 Game Architecture
- **Entity-Component System** with pygame sprite groups
- **Triangle collision detection** using barycentric coordinates
- **Procedural asteroid generation** with random vertex placement
- **Async game loop** for web compatibility
- **Progressive difficulty scaling** based on time elapsed

## 📝 License
MIT License - feel free to fork and modify!

---
*Built with ❤️ and lots of triangles*
