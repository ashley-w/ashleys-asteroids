# Ashley's Asteroids 🔺
*A Triangle Simulator*

A synthwave-themed asteroids game built with Python and pygame, featuring triangle-based collision detection, lumpy procedural asteroids, and explosive gameplay.

## 🎮 Play Online
[Play the game on Netlify](https://your-netlify-url.netlify.app) *(coming soon)*

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

# Run the game
python main.py
```

### Web Build
```bash
# Build for web deployment
python build.py

# Or manually:
python -m pygbag main.py --width 1280 --height 720 --name "Ashley's Asteroids"
```

## 🌐 Deployment to Netlify

1. **Connect to Netlify:**
   - Push your code to GitHub
   - Connect your GitHub repo to Netlify
   - Netlify will automatically detect the `netlify.toml` configuration

2. **Build Settings:**
   - Build command: `python -m pygbag main.py --width 1280 --height 720 --name "Ashley's Asteroids"`
   - Publish directory: `dist`
   - Python version: 3.11 (set in `runtime.txt`)

3. **Deploy:**
   - Netlify will automatically build and deploy on every push to main branch

## 📁 Project Structure
```
ashleys-asteroids/
├── src/
│   ├── core/           # Core game systems
│   ├── entities/       # Game objects (player, asteroids, etc.)
│   └── systems/        # Game systems (explosions, notifications, etc.)
├── main.py            # Main game entry point
├── netlify.toml       # Netlify configuration
├── requirements.txt   # Python dependencies
├── build.py          # Build script for web deployment
└── README.md         # This file
```

## 🎨 Tech Stack
- **Python 3.11+**
- **pygame-ce** for game engine
- **pygbag** for WebAssembly compilation
- **Netlify** for web hosting

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
