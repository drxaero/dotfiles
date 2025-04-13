import os
import subprocess
from pathlib import Path

import pytest

# Path to the bash script
SCRIPT_PATH = Path(__file__).parent.parent.parent / "apps" / "zsh" / "install_font"


@pytest.fixture(name="mock_home_dir")
def _mock_home_dir(tmp_path: Path):
    """Fixture to mock the home directory."""
    font_path = tmp_path / "Library" / "Fonts"
    os.makedirs(font_path, exist_ok=True)
    yield tmp_path


def test_downloaded_font_is_a_ttf_file(mock_home_dir: Path):
    """Test if the font is downloaded as a .ttf file."""

    # Arrange
    assert SCRIPT_PATH.is_file(), f"Script not found at {SCRIPT_PATH}"

    # Run
    result = subprocess.run(["sh", str(SCRIPT_PATH)], capture_output=True, check=True, env={"HOME": str(mock_home_dir)})
    assert result.returncode == 0, f"Script failed with {result.stderr}"

    # Check if the font file exists
    downloaded_font_path = mock_home_dir / "Library" / "Fonts" / "JetBrainsMono-Regular.ttf"
    assert os.path.isfile(downloaded_font_path), "Font file was not downloaded."
