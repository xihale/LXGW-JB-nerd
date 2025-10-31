#!/usr/bin/env python3
"""
Font Merger Script
Merges LXGW WenKai (Chinese) with JetBrains Mono (Latin) and patches with Nerd Fonts
"""

import os
import sys
import subprocess
import json
import urllib.request
import zipfile
import tarfile
import shutil
from pathlib import Path
from typing import Dict, List, Optional

def get_latest_release(repo: str) -> Dict:
    """Get the latest release information from GitHub"""
    url = f"https://api.github.com/repos/{repo}/releases/latest"
    print(f"Fetching latest release from {repo}...")
    
    # Add User-Agent to avoid rate limiting
    req = urllib.request.Request(url, headers={'User-Agent': 'LXGW-JB-nerd/1.0'})
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode())
    return data

def download_file(url: str, dest: Path) -> None:
    """Download a file from URL to destination"""
    print(f"Downloading {url}...")
    dest.parent.mkdir(parents=True, exist_ok=True)
    urllib.request.urlretrieve(url, dest)
    print(f"Downloaded to {dest}")

def extract_archive(archive_path: Path, dest_dir: Path) -> None:
    """Extract tar.gz or zip archive"""
    print(f"Extracting {archive_path}...")
    dest_dir.mkdir(parents=True, exist_ok=True)
    
    if archive_path.suffix == '.zip' or archive_path.name.endswith('.zip'):
        with zipfile.ZipFile(archive_path, 'r') as zip_ref:
            zip_ref.extractall(dest_dir)
    elif archive_path.name.endswith('.tar.gz') or archive_path.name.endswith('.tgz'):
        with tarfile.open(archive_path, 'r:gz') as tar_ref:
            tar_ref.extractall(dest_dir)
    else:
        raise ValueError(f"Unsupported archive format: {archive_path}")
    
    print(f"Extracted to {dest_dir}")

def find_fonts(directory: Path, pattern: str = "*.ttf") -> List[Path]:
    """Find all font files in directory"""
    fonts = list(directory.rglob(pattern))
    print(f"Found {len(fonts)} font files matching {pattern} in {directory}")
    return fonts

def merge_fonts(lxgw_font: Path, jb_font: Path, output_font: Path) -> None:
    """Merge LXGW (Chinese) and JetBrains Mono (Latin) fonts using fontforge"""
    print(f"Merging {lxgw_font.name} with {jb_font.name}...")
    
    merge_script = f'''
import fontforge
import sys

# Open the JetBrains Mono font as base (for Latin characters)
base = fontforge.open("{jb_font}")
print(f"Opened base font: {base.fontname}")

# Open LXGW font to copy Chinese characters
chinese = fontforge.open("{lxgw_font}")
print(f"Opened Chinese font: {chinese.fontname}")

# Copy Chinese characters (CJK Unified Ideographs and related ranges)
# Basic CJK: U+4E00 to U+9FFF
# CJK Extension A: U+3400 to U+4DBF
# CJK Symbols: U+3000 to U+303F
for encoding in range(0x3000, 0x303F + 1):
    if encoding in chinese:
        base.selection.select(encoding)
        chinese.selection.select(encoding)
        chinese.copy()
        base.paste()

for encoding in range(0x3400, 0x4DBF + 1):
    if encoding in chinese:
        base.selection.select(encoding)
        chinese.selection.select(encoding)
        chinese.copy()
        base.paste()

for encoding in range(0x4E00, 0x9FFF + 1):
    if encoding in chinese:
        base.selection.select(encoding)
        chinese.selection.select(encoding)
        chinese.copy()
        base.paste()

# Update font metadata
base.familyname = "LXGW JB"
base.fullname = "LXGW JB Mono"
base.fontname = "LXGWJB-Mono"

# Generate the merged font
output_path = "{output_font}"
base.generate(output_path)
print(f"Generated merged font: {output_path}")

base.close()
chinese.close()
'''
    
    # Write and execute the merge script
    merge_script_path = output_font.parent / "merge_temp.py"
    merge_script_path.write_text(merge_script)
    
    try:
        result = subprocess.run(
            ["fontforge", "-script", str(merge_script_path)],
            check=True,
            capture_output=True,
            text=True
        )
        print(result.stdout)
        if result.stderr:
            print("Warnings:", result.stderr)
    finally:
        merge_script_path.unlink()
    
    print(f"Merged font created: {output_font}")

def patch_with_nerd_fonts(font_path: Path, patcher_dir: Path, output_dir: Path) -> Path:
    """Patch font with Nerd Fonts glyphs"""
    print(f"Patching {font_path.name} with Nerd Fonts...")
    
    patcher_script = patcher_dir / "font-patcher"
    if not patcher_script.exists():
        raise FileNotFoundError(f"Nerd Font patcher not found at {patcher_script}")
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    cmd = [
        str(patcher_script),
        "--complete",  # Add all glyphs
        "--careful",   # Don't overwrite existing glyphs
        "--quiet",     # Reduce output
        "-out", str(output_dir),
        str(font_path)
    ]
    
    subprocess.run(cmd, check=True)
    
    # Find the patched font
    patched_fonts = list(output_dir.glob("*Nerd*.ttf"))
    if not patched_fonts:
        raise RuntimeError(f"No patched font found in {output_dir}")
    
    patched_font = patched_fonts[0]
    print(f"Patched font created: {patched_font}")
    return patched_font

def main():
    """Main function to orchestrate the font merging process"""
    print("=" * 60)
    print("LXGW + JetBrains Mono + Nerd Font Merger")
    print("=" * 60)
    
    # Setup directories
    work_dir = Path("work")
    work_dir.mkdir(exist_ok=True)
    
    downloads_dir = work_dir / "downloads"
    extracts_dir = work_dir / "extracts"
    merged_dir = work_dir / "merged"
    patched_dir = work_dir / "patched"
    output_dir = Path("output")
    
    for d in [downloads_dir, extracts_dir, merged_dir, patched_dir, output_dir]:
        d.mkdir(exist_ok=True)
    
    # Step 1: Download LXGW WenKai
    print("\n" + "=" * 60)
    print("Step 1: Downloading LXGW WenKai")
    print("=" * 60)
    lxgw_release = get_latest_release("lxgw/LxgwWenKai")
    lxgw_version = lxgw_release['tag_name']
    print(f"Latest LXGW WenKai version: {lxgw_version}")
    
    # Find the appropriate asset
    lxgw_asset = None
    for asset in lxgw_release['assets']:
        if 'lxgw-wenkai-' in asset['name'] and asset['name'].endswith('.tar.gz'):
            lxgw_asset = asset
            break
    
    if not lxgw_asset:
        raise RuntimeError("Could not find LXGW WenKai font asset")
    
    lxgw_archive = downloads_dir / lxgw_asset['name']
    download_file(lxgw_asset['browser_download_url'], lxgw_archive)
    extract_archive(lxgw_archive, extracts_dir / "lxgw")
    
    # Step 2: Download JetBrains Mono
    print("\n" + "=" * 60)
    print("Step 2: Downloading JetBrains Mono")
    print("=" * 60)
    jb_release = get_latest_release("JetBrains/JetBrainsMono")
    jb_version = jb_release['tag_name']
    print(f"Latest JetBrains Mono version: {jb_version}")
    
    # Find the appropriate asset
    jb_asset = None
    for asset in jb_release['assets']:
        if 'JetBrainsMono-' in asset['name'] and asset['name'].endswith('.zip'):
            jb_asset = asset
            break
    
    if not jb_asset:
        raise RuntimeError("Could not find JetBrains Mono font asset")
    
    jb_archive = downloads_dir / jb_asset['name']
    download_file(jb_asset['browser_download_url'], jb_archive)
    extract_archive(jb_archive, extracts_dir / "jetbrains")
    
    # Step 3: Download Nerd Font Patcher
    print("\n" + "=" * 60)
    print("Step 3: Downloading Nerd Font Patcher")
    print("=" * 60)
    nerd_release = get_latest_release("ryanoasis/nerd-fonts")
    nerd_version = nerd_release['tag_name']
    print(f"Latest Nerd Fonts version: {nerd_version}")
    
    patcher_asset = None
    for asset in nerd_release['assets']:
        if asset['name'] == 'FontPatcher.zip':
            patcher_asset = asset
            break
    
    if not patcher_asset:
        raise RuntimeError("Could not find Nerd Font patcher asset")
    
    patcher_archive = downloads_dir / "FontPatcher.zip"
    download_file(patcher_asset['browser_download_url'], patcher_archive)
    patcher_dir = work_dir / "FontPatcher"
    extract_archive(patcher_archive, patcher_dir)
    
    # Make patcher executable
    patcher_script = patcher_dir / "font-patcher"
    if patcher_script.exists():
        patcher_script.chmod(0o755)
    
    # Step 4: Find fonts to merge
    print("\n" + "=" * 60)
    print("Step 4: Finding fonts to merge")
    print("=" * 60)
    lxgw_fonts = find_fonts(extracts_dir / "lxgw")
    jb_fonts = find_fonts(extracts_dir / "jetbrains")
    
    print(f"Found {len(lxgw_fonts)} LXGW fonts")
    print(f"Found {len(jb_fonts)} JetBrains Mono fonts")
    
    # Step 5: Merge fonts and patch with Nerd Fonts
    print("\n" + "=" * 60)
    print("Step 5: Merging and patching fonts")
    print("=" * 60)
    
    # For simplicity, merge Regular variants
    lxgw_regular = None
    for font in lxgw_fonts:
        if 'Regular' in font.name and 'Mono' in font.name:
            lxgw_regular = font
            break
    
    jb_regular = None
    for font in jb_fonts:
        if 'Regular' in font.name and 'Mono' not in font.parent.name:
            # Get TTF version from fonts/ttf directory
            if font.parent.name == 'ttf':
                jb_regular = font
                break
    
    if not lxgw_regular:
        print("Warning: Could not find LXGW Regular font, using first available")
        lxgw_regular = lxgw_fonts[0] if lxgw_fonts else None
    
    if not jb_regular:
        print("Warning: Could not find JetBrains Mono Regular font, using first available")
        jb_regular = jb_fonts[0] if jb_fonts else None
    
    if not lxgw_regular or not jb_regular:
        raise RuntimeError("Could not find required fonts for merging")
    
    print(f"Using LXGW font: {lxgw_regular}")
    print(f"Using JetBrains Mono font: {jb_regular}")
    
    # Merge the fonts
    merged_font = merged_dir / "LXGWJB-Mono-Regular.ttf"
    merge_fonts(lxgw_regular, jb_regular, merged_font)
    
    # Patch with Nerd Fonts
    final_font = patch_with_nerd_fonts(merged_font, patcher_dir, patched_dir)
    
    # Copy to output directory
    final_output = output_dir / final_font.name
    shutil.copy2(final_font, final_output)
    
    print("\n" + "=" * 60)
    print("SUCCESS!")
    print("=" * 60)
    print(f"Final font available at: {final_output}")
    print(f"\nVersions used:")
    print(f"  LXGW WenKai: {lxgw_version}")
    print(f"  JetBrains Mono: {jb_version}")
    print(f"  Nerd Fonts: {nerd_version}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\nError: {e}", file=sys.stderr)
        sys.exit(1)
