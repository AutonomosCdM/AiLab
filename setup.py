from setuptools import setup, find_packages

setup(
    name="lucius",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        'langchain',
        'langchain-community',
        'langchain-groq',
        'groq',
        'slack_bolt',
        'slack_sdk',
        'python-dotenv',
        'pytest',
        'pytest-asyncio',
        'requests'
    ],
    author="Autonomos AiLab",
    description="AI Assistant for Executive Teams",
    python_requires='>=3.8',
)
