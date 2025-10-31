# LXGW-JB-nerd

[![Build and Release Fonts](https://github.com/xihale/LXGW-JB-nerd/actions/workflows/build-fonts.yml/badge.svg)](https://github.com/xihale/LXGW-JB-nerd/actions/workflows/build-fonts.yml)

A merged font combining the best of three worlds:
- **LXGW WenKai (霞鹜文楷)** - Beautiful Chinese characters
- **JetBrains Mono** - Clean and modern Latin characters optimized for coding
- **Nerd Fonts** - Complete icon glyph collection for developers

## Features

- ✨ **Chinese Support**: Excellent Chinese character coverage from LXGW WenKai
- 💻 **Coding Optimized**: JetBrains Mono's carefully designed Latin characters
- 🎨 **Rich Icons**: Full Nerd Fonts icon set (Font Awesome, Devicons, Octicons, etc.)
- 📐 **Monospace**: Consistent character width perfect for terminals and code editors
- 🔄 **Auto-Updated**: Automatically tracks latest versions of all three fonts

## Installation

### Download

Download the latest release from the [Releases](https://github.com/xihale/LXGW-JB-nerd/releases) page.

### Install

**Linux**
```bash
mkdir -p ~/.local/share/fonts
tar -xzf lxgw-jb-nerd-fonts.tar.gz -C ~/.local/share/fonts/
fc-cache -fv
```

**macOS**
```bash
# Extract and open the fonts, then click "Install Font"
unzip lxgw-jb-nerd-fonts.zip
open *.ttf
```

**Windows**
1. Extract the zip file
2. Select all `.ttf` files
3. Right-click and select "Install" or "Install for all users"

## Usage

After installation, the font will be available as **LXGWJB Nerd Font Mono** in your applications.

### Terminal Emulators
- **VS Code**: Set `"editor.fontFamily": "LXGWJB Nerd Font Mono"`
- **Alacritty**: Set `font.normal.family = "LXGWJB Nerd Font Mono"`
- **iTerm2**: Preferences → Profiles → Text → Font → LXGWJB Nerd Font Mono
- **Windows Terminal**: Settings → Profiles → Appearance → Font face → LXGWJB Nerd Font Mono

## Building from Source

### Prerequisites

- Python 3.11+
- FontForge with Python bindings
- Internet connection

### Build

```bash
# Install dependencies
sudo apt-get install fontforge python3-fontforge  # Ubuntu/Debian
# or
brew install fontforge  # macOS

# Run the build script
python scripts/merge_fonts.py
```

The merged fonts will be available in the `output/` directory.

## How It Works

1. **Download**: Automatically fetches the latest releases of LXGW WenKai, JetBrains Mono, and Nerd Fonts patcher
2. **Merge**: Uses FontForge to combine Chinese characters from LXGW WenKai with Latin characters from JetBrains Mono
3. **Patch**: Applies Nerd Fonts patcher to add icon glyphs
4. **Package**: Creates distribution archives and publishes to GitHub Releases

## Credits

- **LXGW WenKai** by [lxgw](https://github.com/lxgw/LxgwWenKai) - Base Chinese font
- **JetBrains Mono** by [JetBrains](https://github.com/JetBrains/JetBrainsMono) - Base Latin font
- **Nerd Fonts** by [ryanoasis](https://github.com/ryanoasis/nerd-fonts) - Icon glyphs and patcher

## License

This project follows the licenses of its components:
- LXGW WenKai: [SIL Open Font License 1.1](https://github.com/lxgw/LxgwWenKai/blob/main/LICENSE)
- JetBrains Mono: [Apache License 2.0](https://github.com/JetBrains/JetBrainsMono/blob/master/LICENSE)
- Nerd Fonts: [MIT License](https://github.com/ryanoasis/nerd-fonts/blob/master/LICENSE)

The merge scripts in this repository are released under the MIT License.