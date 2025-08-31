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

# Run the game locally
python main.py
```

### Web Build & Deploy
```bash
# Build for web
python build-local.py

# This creates a 'main' folder with web files
# Upload the contents of the 'main' folder to Netlify manually
```

## 🌐 Manual Deployment to Netlify

1. **Build locally:** Run `python build-local.py`
2. **Find the output:** Look for a `main` folder with your web files
3. **Deploy:** Drag & drop the `main` folder contents to Netlify
4. **Your game goes live!** 🔺

## 📁 Project Structure
```
ashleys-asteroids/
├── src/
│   ├── core/           # Core game systems
│   ├── entities/       # Game objects (player, asteroids, etc.)
│   └── systems/        # Game systems (explosions, notifications, etc.)
├── main.py            # Main game entry point
├── requirements.txt   # Python dependencies
├── build-local.py     # Simple build script
└── README.md         # This file
```

## 🎨 Tech Stack
- **Python 3.10+**
- **pygame-ce** for game engine
- **pygbag** for WebAssembly compilation
- **Netlify** for web hosting (manual deploy)

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
