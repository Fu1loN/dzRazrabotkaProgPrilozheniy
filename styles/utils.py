from pathlib import Path

def load_stylesheet():
    style_file = Path(__file__).parent / 'main.qss'
    with open(style_file, 'r') as f:
        return f.read() 