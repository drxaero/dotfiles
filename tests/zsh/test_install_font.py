import os
import platform
import subprocess
from pathlib import Path
from typing import Generator

import pytest

# Path to the bash script
SCRIPT_PATH = Path(__file__).parent.parent.parent / "apps" / "zsh" / "install_font"


def get_user_font_dir(home_dir: Path) -> Path:
    """
    Return the MacOS user font directory.
    """
    assert platform.system() == "Darwin", "This function only supports MacOS."
    assert home_dir.is_dir(), f"Home directory {home_dir} does not exist."

    return home_dir / "Library" / "Fonts"


@pytest.fixture(name="mock_home_dir")
def _mock_home_dir(tmp_path: Path) -> Generator[Path, None, None]:
    """
    Fixture to mock the home directory.
    """
    assert tmp_path.is_dir(), f"Temporary path {tmp_path} does not exist."

    font_path = get_user_font_dir(tmp_path)
    os.makedirs(font_path, exist_ok=True)
    yield tmp_path


def test_downloaded_font_is_a_ttf_file(mock_home_dir: Path):
    """
    Test if the font is downloaded as a .ttf file.
    """

    downloaded_font_path = get_user_font_dir(mock_home_dir) / "JetBrainsMono-Regular.ttf"

    # Environment check
    assert SCRIPT_PATH.is_file(), f"Script not found at {SCRIPT_PATH}"
    assert not os.path.exists(downloaded_font_path), "Font file should not exist."

    # Run
    result = subprocess.run(["sh", str(SCRIPT_PATH)], capture_output=True, check=True, env={"HOME": str(mock_home_dir)})
    assert result.returncode == 0, f"Script failed with {result.stderr}"

    # Check if the font file exists
    assert os.path.isfile(downloaded_font_path), "Font file was not downloaded."
