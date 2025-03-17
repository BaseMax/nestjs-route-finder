import os
import re
import json
import yaml

def camel_to_kebab(name):
    """Convert a camelCase or PascalCase string to kebab-case."""
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1-\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1-\2', s1).lower()

def remove_comments(lines):
    """Remove single-line and multi-line comments from the code."""
    cleaned_lines = []
    in_multiline_comment = False

    for line in lines:
        if in_multiline_comment:
            if '*/' in line:
                in_multiline_comment = False
                line = line.split('*/', 1)[1]
            else:
                continue

        if '/*' in line:
            in_multiline_comment = True
            line = line.split('/*', 1)[0]

        line = line.split('//', 1)[0]

        if line.strip():
            cleaned_lines.append(line)

    return ''.join(cleaned_lines)

def remove_comments_and_extract_routes(file_path, base_path):
    """Remove comments and extract route info, including controller prefix."""
    routes = []
    
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        cleaned_code = remove_comments(lines)
    
    controller_pattern = re.compile(
        r'@Controller\s*\(\s*[\'"](?P<controller>[^\'"]+)[\'"]\s*\)'
    )
    controller_match = controller_pattern.search(cleaned_code)
    controller_prefix = controller_match.group('controller') if controller_match else ''

    route_pattern = re.compile(
        r'@(?P<method>Get|Post|Put|Delete|Patch)\s*\(\s*(?:[\'"](?P<path>[^\'"]*)[\'"])?\s*\).*?(?:async\s+)?(?P<function_name>\w+)\s*\(',
        re.DOTALL
    )
    
    for match in route_pattern.finditer(cleaned_code):
        method = match.group('method').lower()
        path = match.group('path')
        function_name = match.group('function_name')
        
        if not path:
            path = camel_to_kebab(function_name)
        
        full_path = f"/{controller_prefix.strip('/')}/{path.strip('/')}"
        full_path = re.sub(r'/+', '/', full_path)

        relative_file_path = file_path.replace(base_path + os.sep, '').replace(base_path, '')

        routes.append({
            'method': method.upper(),
            'path': full_path,
            'file': relative_file_path
        })

    return routes

def process_directory(directory):
    """Recursively process the directory to extract routes from TypeScript/JavaScript files."""
    all_routes = []
    
    for root, dirs, files in os.walk(directory):
        if 'node_modules' in dirs:
            dirs.remove('node_modules')

        for file in files:
            if file.endswith('.controller.ts'):
                file_path = os.path.join(root, file)
                routes = remove_comments_and_extract_routes(file_path, directory)
                all_routes.extend(routes)

    return all_routes

def save_output(routes, output_directory):
    """Save the extracted routes to JSON and YAML files."""
    json_file = os.path.join(output_directory, "routes.json")
    yaml_file = os.path.join(output_directory, "routes.yaml")

    with open(json_file, "w", encoding="utf-8") as jf:
        json.dump(routes, jf, indent=4, ensure_ascii=False)

    with open(yaml_file, "w", encoding="utf-8") as yf:
        yaml.dump(routes, yf, default_flow_style=False, allow_unicode=True)

    print(f"\n✅ JSON and YAML output saved in: {output_directory}")

if __name__ == "__main__":
    project_path = input("Enter the path to the project: ").strip()
    routes = process_directory(project_path)

    for route in routes:
        print(f"Method: {route['method']}, Path: {route['path']}, File: {route['file']}") 

    save_output(routes, project_path)
