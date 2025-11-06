import yaml

def read_yaml_file(file_path: str) -> dict:
    with open(file_path, 'rb') as yaml_file:
        return yaml.safe_load(yaml_file)
