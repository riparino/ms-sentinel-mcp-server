#!/usr/bin/env python3
"""
Setup script for MCP Server Sentinel.
This script now defers most packaging configuration to pyproject.toml.
"""

from setuptools import setup

# The majority of our configuration is now in pyproject.toml
# This setup.py file is kept minimal and mainly serves as a fallback
# for pip installation without requiring the latest pip versions.

setup()
