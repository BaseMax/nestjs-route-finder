import os
import re

def remove_comments_and_extract_routes(file_path):
    routes = []
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

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

    cleaned_code = ''.join(cleaned_lines)

    route_pattern = re.compile(
        r'@(?P<method>Get|Post|Put|Delete|Patch)\s*$?\'?(?P<path>[^\')]*?)\'?$?\s*(?:async\s+)?(?P<function_name>\w+)\s*\('
    )
    matches = route_pattern.finditer(cleaned_code)

    for match in matches:
        method = match.group('method').lower()
        path = match.group('path') if match.group('path') else ''
        function_name = match.group('function_name')

        if not path:
            path = function_name

        full_route = f"{path}"
        routes.append({
            'method': method,
            'path': full_route,
            'file': file_path
        })

    return routes

def process_directory(directory):
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
