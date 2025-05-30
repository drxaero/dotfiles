import logging
import os
import re
import shutil
import subprocess
import time
from pathlib import Path
from typing import Generator

import pytest
from parametrization import Parametrization
from pexpect import spawn

logger = logging.getLogger(__name__)

# Path to .zshrc
ZSHRC_FILE = Path(__file__).parent.parent.parent / "apps" / "zsh" / "zshrc"

BRANCH_NAME = "test-branch"


def wait_for_prompt(cli: spawn, timeout: int = 2) -> str:
    """
    Wait for the zsh prompt to appear.

    :param timeout: The timeout for waiting for the prompt.
                    Why 2 seconds? Because it can pass GitHub Actions: pytest.
    """
    start = time.time()
    cli.expect(r"%", timeout=timeout)  # it seems zsh sends initial % at the beginning before executing the command
    init = time.time()
    logger.debug("Prompt start appeared after %s seconds", init - start)
    cli.expect(r"\[\?2004h", timeout=timeout)  # bracketed paste control
    logger.debug("Prompt end   appeared after %s seconds", time.time() - init)
    prompt = cli.before.strip()
    logger.debug("Prompt: %s", prompt)
    return prompt


@pytest.fixture(name="test_env", scope="function")
def _test_env(tmp_path: Path) -> Generator[Path, None, None]:
    """
    Set up a clean test environment with a copied .zshrc.

    :param tmp_path: The temporary directory provided by pytest.
    """
    zsh_dir = tmp_path / ".zsh"
    zsh_dir.mkdir()
    shutil.copy(ZSHRC_FILE, zsh_dir / ".zshrc")

    # Yield the zsh_dir for use in tests
    yield zsh_dir


@pytest.fixture(name="git_repo", scope="function")
def _git_repo(tmp_path: Path) -> Path:
    """
    Set up a temporary git repository.

    :param tmp_path: The temporary directory provided by pytest.
    """
    commands = [
        ["git", "init"],
        ["git", "add", "."],
        ["git", "commit", "-m", "initial commit"],
        ["git", "checkout", "-b", BRANCH_NAME],
    ]

    for command in commands:
        subprocess.run(command, cwd=tmp_path, stdout=subprocess.DEVNULL, check=True)

    return tmp_path


def run_zsh_command(zsh_dir: Path, command: str) -> str:
    """
    Run a command in a zsh session and return the prompt output.
    """
    # with (
    #     open("/tmp/send.log", "w", encoding="utf-8") as send_log,
    #     open("/tmp/read.log", "w", encoding="utf-8") as read_log,
    # ):

    cli = spawn(
        "zsh",
        ["-i"],
        env={"ZDOTDIR": str(zsh_dir)},
        encoding="utf-8",
        codec_errors="ignore",  # if you can pass the GitHub Actions test, you can remove `codec_errors="ignore"`
    )  # the dimensions should be large enough to avoid line wrapping
    # cli.logfile_send = send_log
    # cli.logfile_read = read_log

    wait_for_prompt(cli)  # wait for the cli to be spawned

    cli.sendline(command)
    prompt = wait_for_prompt(cli)
    logger.debug("Prompt after command: %s", prompt)

    cli.close()
    return prompt


def test__successful_cmd__prompt_turns_green(test_env: Path):
    """
    Test that % is green on success.
    """
    prompt = run_zsh_command(test_env, "true")
    assert re.search(r"\033\[32m%", prompt), "Green % not found on success"


def test__failed_cmd__prompt_turns_red(test_env: Path):
    """
    Test that % is red on failure.
    """
    prompt = run_zsh_command(test_env, "false")
    assert re.search(r"\033\[31m%", prompt), "Red % not found on failure"


def test__under_a_git_repo__prompt_shows_branch_name(test_env: Path, git_repo: Path):
    """
    Test that git branch appears in a git repo.
    """
    prompt = run_zsh_command(test_env, f"cd {git_repo} && true")
    assert f"[{BRANCH_NAME}]" in prompt, "Git branch not displayed"


def test__under_a_non_git_repo__prompt_shows_no_powerline(test_env: Path):
    """
    Test that no git branch appears outside a git repo.
    """
    prompt = run_zsh_command(test_env, f"cd {test_env} && true")
    assert "" not in prompt, "Git branch shown outside repo"


@Parametrization.autodetect_parameters()
@Parametrization.case(name="`$HOME/scripts` is found", folder="~/scripts", found=True)
@Parametrization.case(name="non_existent_folder is not found", folder="~/non_existent_folder", found=False)
def test__can_find_a_folder_in_path(test_env: Path, folder: str, found: bool):
    """
    Test that a folder can be found in the $PATH.
    """
    expanded_folder = os.path.expanduser(folder)

    # Use subprocess.run to fork a zsh shell, source the temp .zshrc, and echo $PATH
    temp_zshrc = test_env / ".zshrc"
    path_dirs = (
        subprocess.run(
            ["zsh", "-c", f"source {temp_zshrc} && echo $PATH"],
            capture_output=True,  # Capture stdout and stderr
            text=True,  # Return output as string, not bytes
            check=True,  # Raise an exception if the command fails
        )
        .stdout.strip()
        .split(os.pathsep)
    )
    is_in_path = expanded_folder in path_dirs
    assert (
        is_in_path == found
    ), f"Expected folder '{expanded_folder}' to be {'in' if found else 'not in'} $PATH, but it was{
        ' not' if found else ''}."
