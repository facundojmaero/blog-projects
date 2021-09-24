import os

pytest_plugins = [
    "tests.fixtures",
]


def pytest_addoption(parser):
    """Add custom command line arguments to pytest."""
    parser.addoption(
        "--strategy",
        action="store",
        help="Test strategy: drop, clear, subtransaction (default: drop)",
        default="drop",
    )

    parser.addoption(
        "--meeseks",
        action="store",
        help="How many meeseks to spawn (default: 5)",
        default="5",
    )


def pytest_configure(config):
    """Setup pytest before running tests."""
    # Store the meeseks argument as an env var to use in `parametrize`
    os.environ["meeseks"] = config.getoption("--meeseks")
