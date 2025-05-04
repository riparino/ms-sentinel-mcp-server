#!/usr/bin/env python3
"""
Script to download the Kusto.Language DLL from NuGet.
Can be run directly or imported.
"""

import os
import urllib.request
import zipfile
import tempfile
import shutil
import json


def download_kusto_dll(
    package_id="Microsoft.Azure.Kusto.Language", version=None, output_dir="lib"
):
    """Download Kusto Language DLL from NuGet."""
    print("====== Starting Kusto Language DLL Download ======")

    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    print(f"Created output directory: {output_dir}")

    # Get latest version if needed
    if not version:
        version = get_latest_version(package_id)
        print(f"Latest version is {version}")

    # Download and extract
    try:
        dlls = download_package(package_id, version, output_dir)
        if dlls:
            print(f"Successfully downloaded {len(dlls)} DLLs:")
            for dll in dlls:
                print(f"  - {os.path.basename(dll)}")
        else:
            print("No DLLs were found in the package.")
    except Exception as e:
        print(f"Error downloading Kusto Language DLL: {e}")
        print("Installation will continue, but KQL validation might not work.")
        return []

    print("====== Completed Kusto Language DLL Download ======")
    return dlls


def get_latest_version(package_id):
    """Get the latest version of the package from NuGet."""
    index_url = (
        f"https://api.nuget.org/v3-flatcontainer/{package_id.lower()}/index.json"
    )

    try:
        with urllib.request.urlopen(index_url) as response:
            data = response.read()
            versions = json.loads(data)["versions"]
            return versions[-1]  # Last one is the latest
    except Exception as e:
        print(f"Error getting latest version: {e}")
        return "9.0.0"  # Fallback to a known version


def download_package(package_id, version, output_dir):
    """Download and extract the NuGet package."""
    nuget_api_base = "https://api.nuget.org/v3-flatcontainer"
    nupkg_url = (
        f"{nuget_api_base}/{package_id.lower()}/{version}/"
        f"{package_id.lower()}.{version}.nupkg"
    )
    print(f"Downloading from {nupkg_url}")

    # Create a temporary directory for the download
    with tempfile.TemporaryDirectory() as temp_dir:
        # Download the package
        nupkg_path = os.path.join(temp_dir, f"{package_id}.{version}.nupkg")
        urllib.request.urlretrieve(nupkg_url, nupkg_path)

        # Extract the .nupkg file (it's just a zip)
        extract_dir = os.path.join(temp_dir, "extracted")
        os.makedirs(extract_dir, exist_ok=True)

        with zipfile.ZipFile(nupkg_path, "r") as zip_ref:
            zip_ref.extractall(extract_dir)

        # Find DLLs in the lib directory (most common location)
        dll_paths = []
        lib_dir = os.path.join(extract_dir, "lib")
        if os.path.exists(lib_dir):
            # Find framework-specific directories
            framework_dirs = [
                d
                for d in os.listdir(lib_dir)
                if os.path.isdir(os.path.join(lib_dir, d))
            ]

            # Prioritize .NET Standard 2.0 if available (compatible with Python.NET)
            target_dir = None
            for preferred in [
                "netstandard2.0",
                "netstandard2.1",
                "net6.0",
                "net5.0",
                "net472",
                "net462",
            ]:
                if preferred in framework_dirs:
                    target_dir = preferred
                    break

            # If no preferred framework found, use the first one
            if not target_dir and framework_dirs:
                target_dir = framework_dirs[0]

            if target_dir:
                dll_dir = os.path.join(lib_dir, target_dir)
                dlls = [f for f in os.listdir(dll_dir) if f.endswith(".dll")]

                # Copy DLLs to output directory
                for dll in dlls:
                    src_path = os.path.join(dll_dir, dll)
                    dst_path = os.path.join(output_dir, dll)
                    shutil.copy2(src_path, dst_path)
                    dll_paths.append(dst_path)
                    print(f"Extracted: {dst_path}")

        # Look for DLLs in the root if none found in lib
        if not dll_paths:
            for root, _, files in os.walk(extract_dir):
                for file in files:
                    if file.endswith(".dll"):
                        src_path = os.path.join(root, file)
                        dst_path = os.path.join(output_dir, file)
                        shutil.copy2(src_path, dst_path)
                        dll_paths.append(dst_path)
                        print(f"Extracted: {dst_path}")

        return dll_paths


if __name__ == "__main__":
    download_kusto_dll()
