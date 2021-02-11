import pathlib
import yaml


BASE_DIR = pathlib.Path(__file__).parent.parent
config_path = BASE_DIR / 'settings' / 'config.yaml'


def get_config():
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)

    return config
