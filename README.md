# 🛤️ NestJS Route Finder

NestJS Route Finder is a simple Python script that automatically extracts API routes from NestJS controllers and outputs them in JSON and YAML formats.

This tool is useful for documenting, debugging, and generating API references for your NestJS backend.

## Features
- Extracts route information from NestJS controllers (`.controller.ts` files)
- Removes single-line (`//`) and multi-line (`/* */`) comments
- Converts method names to kebab-case if no route path is defined
- Outputs extracted routes in **JSON** and **YAML** formats
- Recursively scans the project directory, skipping `node_modules`

## Installation
Ensure you have **Python 3** installed. Then, clone the repository and install dependencies:

```sh
# Clone the repository
git clone https://github.com/BaseMax/nestjs-route-finder.git
cd nestjs-route-finder

# Install dependencies
pip install -r requirements.txt
```
