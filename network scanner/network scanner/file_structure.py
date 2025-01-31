import os

def create_file(path, content=None):
    """Create a file at the given path and optionally write content to it."""
    with open(path, 'w') as file:
        if content:
            file.write(content)

def create_structure(base_dir):
    """Create the directory and file structure."""
    # Define the structure as a dictionary
    structure = {
        "app": {
            "__init__.py": "",
            "config.py": "# Configuration settings\n",
            "api": {
                "__init__.py": "",
                "routes": {
                    "__init__.py": "",
                    "network_routes.py": "",
                    "sql_routes.py": "",
                    "xss_routes.py": ""
                },
                "schemas": {
                    "__init__.py": "",
                    "request_schemas.py": ""
                }
            },
            "services": {
                "__init__.py": "",
                "network_scanner.py": "",
                "sql_scanner.py": "",
                "xss_scanner.py": ""
            },
            "utils": {
                "__init__.py": "",
                "validators.py": "",
                "response_formatter.py": ""
            },
            "tools": {
                "__init__.py": "",
                "base_tool.py": "",
                "nmap_wrapper.py": "",
                "sqlmap_wrapper.py": "",
                "xsstrike_wrapper.py": ""
            }
        },
        "tests": {
            "__init__.py": "",
            "test_network_scanner.py": "",
            "test_sql_scanner.py": ""
        },
        "requirements.txt": "",
        "run.py": "",
        "README.md": "# scansphere_backend\n\nProject description here."
    }

    # Recursive function to create directories and files
    def create_recursive(base, items):
        for name, content in items.items():
            path = os.path.join(base, name)
            if isinstance(content, dict):
                os.makedirs(path, exist_ok=True)  # Create directory
                create_recursive(path, content)  # Recurse
            else:
                create_file(path, content)  # Create file

    create_recursive(base_dir, structure)

if __name__ == "__main__":
    base_directory = "scansphere_backend"
    os.makedirs(base_directory, exist_ok=True)
    create_structure(base_directory)
    print(f"Project structure created in {os.path.abspath(base_directory)}")
