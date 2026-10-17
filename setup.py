
from setuptools import setup, find_packages

setup(
    name="autopilot-ai",
    version="0.1.0",
    description="AutoPilot AI model and inference utilities",
    packages=find_packages(include=["autopilot_ai", "autopilot_ai.*", "src", "src.*"]),
    python_requires=">=3.10",
)
