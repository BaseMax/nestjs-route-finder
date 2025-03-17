# 🛤️ NestJS Route Finder

**NestJS Route Finder** is a simple Python script that automatically extracts API routes from NestJS controllers and outputs them in **JSON** and **YAML** formats. 

This tool is useful for **documenting**, **debugging**, and **generating API references** for your NestJS backend.

## 🚀 Features

✅ Automatically extracts routes from `.controller.ts` files  
✅ Supports `@Get`, `@Post`, `@Put`, `@Delete`, and `@Patch` decorators  
✅ Handles controller prefixes for accurate paths  
✅ Converts camelCase method names into kebab-case routes (if no explicit path is provided)  
✅ Removes both **single-line** and **multi-line** comments  
✅ Saves output as **JSON** (`routes.json`) and **YAML** (`routes.yaml`)  

## 📌 Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/BaseMax/nestjs-route-finder.git
   cd nestjs-route-finder
   ```

2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

## 🔧 Usage

Run the script and provide the path to your NestJS project:

```sh
python script.py
```

Then enter the absolute path to your NestJS project when prompted.  
Example:
```
Enter the path to the project: /path/to/your/nestjs-project
```

The extracted routes will be saved in:

- `routes.json`
- `routes.yaml`

## 📄 Example Output

### **routes.json**
```json
[
    {
        "method": "GET",
        "path": "/users/all",
        "file": "src/controllers/user.controller.ts"
    },
    {
        "method": "POST",
        "path": "/users/create",
        "file": "src/controllers/user.controller.ts"
    }
]
```

### **routes.yaml**
```yaml
- method: GET
  path: /users/all
  file: src/controllers/user.controller.ts
- method: POST
  path: /users/create
  file: src/controllers/user.controller.ts
```

## 🛠 How It Works

1. **Scans your NestJS project** and finds `.controller.ts` files  
2. **Extracts** the controller prefix and route methods (`@Get`, `@Post`, etc.)  
3. **Removes comments** to avoid false matches  
4. **Outputs JSON and YAML** for easy integration with documentation tools  

This project is licensed under the MIT License.

Copyright 2025, Max Base (Seyyed Ali Mohammadiyeh)
