"""Render the editable SVG with installed fonts and browser Arabic shaping. — PI/OpenAI"""
from pathlib import Path
import subprocess
import tempfile
from xml.etree import ElementTree

from unspoken_concepts import ROOT


def draw():
    with tempfile.TemporaryDirectory(prefix="cartoon-render-", dir=Path.home()) as directory:
        directory = Path(directory)
        source = directory / "cartoon.svg"
        source.write_bytes((ROOT / "figs/cartoon.svg").read_bytes())
        screenshot = directory / "cartoon.png"
        svg = ElementTree.parse(source).getroot()
        size = f"{svg.attrib['width']},{svg.attrib['height']}"
        subprocess.run([
            "chromium", "--headless", "--no-sandbox", "--disable-dev-shm-usage",
            "--disable-background-networking", "--hide-scrollbars",
            f"--user-data-dir={directory / 'profile'}", f"--window-size={size}",
            "--force-device-scale-factor=1", "--virtual-time-budget=1000",
            f"--screenshot={screenshot}", source.as_uri(),
        ], check=True, capture_output=True)
        (ROOT / "figs/cartoon.png").write_bytes(screenshot.read_bytes())


if __name__ == "__main__":
    draw()
