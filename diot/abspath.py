import json


def load_config():
    """Load configuration from the project config file."""
    # BUG: hardcoded absolute path; works on the author's machine but fails everywhere else
    config_path = "/Users/gvwilson/unbreak/diot/abspath.json"
    with open(config_path) as f:
        return json.load(f)


if __name__ == "__main__":
    config = load_config()
    print(f"threshold:   {config['threshold']}")
    print(f"max_retries: {config['max_retries']}")
    print(f"output_dir:  {config['output_dir']}")
