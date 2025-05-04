#!/usr/bin/env python3
"""Post-installation script to download DLLs."""

import subprocess
import sys


def main():
    try:
        # Try importing the function directly
        # pylint: disable=import-outside-toplevel
        from download_dll import (
            download_kusto_dll,
        )

        download_kusto_dll()
    except ImportError:
        # Fall back to using the entry point
        try:
            subprocess.check_call([sys.executable, "-m", "download_dll"])
        except subprocess.SubprocessError:
            print("Warning: Failed to download Kusto DLL after installation")
            print("You may need to run 'download-kusto-dll' manually")


if __name__ == "__main__":
    main()
