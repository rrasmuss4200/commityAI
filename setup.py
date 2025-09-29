from setuptools import setup, find_packages

setup(
    name="commityai",
    version="0.2.0",
    description="AI-powered git commit message generator using OpenAI",
    py_modules=find_packages(),
    install_requires=["openai>=1.0.0"],
    entry_points={
        "console_scripts": [
            "commityai=src.main:main",
        ],
    },
    python_requires=">=3.7",
)