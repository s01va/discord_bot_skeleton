import sys
import yaml


def read_yaml(yaml_file: str):
    try:
        with open(yaml_file, 'r') as f:
            loaded_yaml = yaml.safe_load(f.read())
            if loaded_yaml is None:
                print(f"Could not parse {yaml_file}")
                sys.exit(3)
            return loaded_yaml
    except:
        print(f"Could not parse {yaml_file}")
        sys.exit(3)
