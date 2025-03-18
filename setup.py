#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name="lucius-agent",
    version="0.2.0",
    description="Agente de IA Lucius para Slack",
    author="Autonomos AiLab",
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        "slack-bolt>=1.18.0",
        "slack-sdk>=3.21.3",
        "langchain-groq>=0.1.0",
        "langchain-core>=0.1.18",
        "requests>=2.31.0",
        "python-dotenv>=1.0.0",
        "typing-extensions>=4.8.0",
    ],
    entry_points={
        "console_scripts": [
            "lucius=lucius_agent:main",
        ],
    },
    python_requires=">=3.8",
)
