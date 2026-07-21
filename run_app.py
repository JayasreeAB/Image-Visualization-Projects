#!/usr/bin/env python3
import os
import sys
import webbrowser
from threading import Timer

def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000")

if __name__ == '__main__':
    print("=" * 60)
    print("  🚀 Vision Hub - AI Face Counter & Hand Brightness Control")
    print("=" * 60)
    print("  Starting server at http://127.0.0.1:5000 ...")
    print("  Press Ctrl+C to stop the server.")
    print("=" * 60)

    # Automatically open browser after 1.5 seconds
    Timer(1.5, open_browser).start()

    from app import app
    app.run(host='0.0.0.0', port=5000, debug=False)
