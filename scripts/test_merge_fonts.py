#!/usr/bin/env python3
"""
Test script for merge_fonts.py
Validates the script structure and simulates API calls
"""

import sys
import json
from pathlib import Path

def test_imports():
    """Test that all required modules can be imported"""
    print("Testing imports...")
    try:
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
        print("✓ All standard library imports successful")
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False
    
    try:
        import fontforge
        print(f"✓ FontForge module available (version {fontforge.version()})")
    except ImportError:
        print("✗ FontForge module not available")
        return False
    
    return True

def test_script_syntax():
    """Test that merge_fonts.py has valid syntax"""
    print("\nTesting script syntax...")
    import py_compile
    try:
        # Use relative path from script directory
        script_path = Path(__file__).parent / 'merge_fonts.py'
        py_compile.compile(str(script_path), doraise=True)
        print("✓ Script has valid Python syntax")
        return True
    except py_compile.PyCompileError as e:
        print(f"✗ Syntax error: {e}")
        return False

def test_function_definitions():
    """Test that all expected functions are defined"""
    print("\nTesting function definitions...")
    # Add scripts directory to path using relative import
    scripts_dir = Path(__file__).parent
    sys.path.insert(0, str(scripts_dir))
    try:
        import merge_fonts
        
        expected_functions = [
            'get_latest_release',
            'download_file',
            'extract_archive',
            'find_fonts',
            'merge_fonts',
            'patch_with_nerd_fonts',
            'main'
        ]
        
        for func_name in expected_functions:
            if hasattr(merge_fonts, func_name):
                print(f"✓ Function '{func_name}' is defined")
            else:
                print(f"✗ Function '{func_name}' is not defined")
                return False
        
        return True
    except Exception as e:
        print(f"✗ Error loading module: {e}")
        return False

def test_directory_structure():
    """Test that expected directories can be created"""
    print("\nTesting directory creation...")
    test_dir = Path("/tmp/test_lxgw_jb_nerd")
    try:
        test_dir.mkdir(exist_ok=True)
        (test_dir / "work").mkdir(exist_ok=True)
        (test_dir / "output").mkdir(exist_ok=True)
        print("✓ Directories can be created successfully")
        
        # Cleanup
        import shutil
        shutil.rmtree(test_dir)
        return True
    except Exception as e:
        print(f"✗ Directory creation error: {e}")
        return False

def test_fontforge_basic():
    """Test basic fontforge operations"""
    print("\nTesting FontForge basic operations...")
    try:
        import fontforge
        
        # Test creating a simple font
        font = fontforge.font()
        font.familyname = "Test"
        font.fontname = "Test"
        font.fullname = "Test Font"
        
        # Test adding a glyph
        glyph = font.createChar(65, 'A')  # Unicode 65 = 'A'
        
        print("✓ FontForge can create and manipulate fonts")
        
        font.close()
        return True
    except Exception as e:
        print(f"✗ FontForge operation error: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("Testing LXGW-JB-nerd Font Merge Script")
    print("=" * 60)
    
    tests = [
        ("Module Imports", test_imports),
        ("Script Syntax", test_script_syntax),
        ("Function Definitions", test_function_definitions),
        ("Directory Structure", test_directory_structure),
        ("FontForge Operations", test_fontforge_basic),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"✗ Test '{test_name}' failed with exception: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 60)
    print("Test Results Summary")
    print("=" * 60)
    
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        symbol = "✓" if result else "✗"
        print(f"{symbol} {test_name}: {status}")
    
    total = len(results)
    passed = sum(1 for _, result in results if result)
    
    print("\n" + "=" * 60)
    print(f"Total: {passed}/{total} tests passed")
    print("=" * 60)
    
    return 0 if passed == total else 1

if __name__ == "__main__":
    sys.exit(main())
