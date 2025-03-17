import os
import re

def remove_comments_and_extract_routes(file_path):
    """Remove comments from the file and extract route information."""
    routes = []
    
    with open(file_path, 'r', encoding='utf-8') as file:
        cleaned_code = remove_comments(file.readlines())

    route_pattern = re.compile(
        r'@(?P<method>Get|Post|Put|Delete|Patch)\s*$?\'?(?P<path>[^\')]*?)\'?$?\s*(?:async\s+)?(?P<function_name>\w+)\s*\('
    )
    
    for match in route_pattern.finditer(cleaned_code):
        method = match.group('method').lower()
        path = match.group('path') or match.group('function_name')
        routes.append({
            'method': method,
            'path': path,
            'file': file_path
        })

    return routes

def remove_comments(lines):
    """Remove single-line and multi-line comments from the code."""
    cleaned_lines = []
    in_multiline_comment = False

    for line in lines:
        if '/*' in line:
            in_multiline_comment = True
            line = line.split('/*')[0]
        if '*/' in line:
            in_multiline_comment = False
            line = line.split('*/')[-1]
        
        if not in_multiline_comment and not line.strip().startswith('//'):
            cleaned_lines.append(line)

    return ''.join(cleaned_lines)

def process_directory(directory):
    """Recursively process the directory to extract routes from TypeScript files."""
    all_routes = []
    
    for root, dirs, files in os.walk(directory):
        if 'node_modules' in dirs:
            dirs.remove('node_modules')

        for file in files:
            if file.endswith('.ts'):
                file_path = os.path.join(root, file)
                routes = remove_comments_and_extract_routes(file_path)
                all_routes.extend(routes)

    return all_routes

if __name__ == "__main__":
    project_path = input("Enter the path to your NestJS project: ")
    routes = process_directory(project_path)

    for route in routes:
        print(f"Method: {route['method'].upper()}, Path: {route['path']}, File: {route['file']}")
