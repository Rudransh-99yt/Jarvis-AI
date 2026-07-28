#!/bin/bash

echo "🚀 Setting up Jarvis..."

mkdir -p brain config core memory skills voice utils data logs tests

touch main.py .env .gitignore README.md requirements.txt

touch brain/__init__.py
touch config/__init__.py
touch core/__init__.py
touch memory/__init__.py
touch skills/__init__.py
touch voice/__init__.py
touch utils/__init__.py

echo "✅ Project structure ready."
