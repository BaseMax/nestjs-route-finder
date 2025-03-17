# NestJS Route Finder

NestJS Route Finder is a Python script that scans a NestJS project to extract route information from controller files. It identifies HTTP methods and paths and outputs them in JSON and YAML formats.

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
