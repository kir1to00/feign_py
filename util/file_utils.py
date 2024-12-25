import yaml


def load_yaml(yaml_file_path):
    with open(yaml_file_path, 'r', encoding='utf-8') as file:
        data = yaml.safe_load(file)
    return data
