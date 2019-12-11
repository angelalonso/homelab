import argparse
import yaml
import sys

def main() -> int:
    return 0

if __name__ == 	'__main__':
    with open(r'./config.yaml') as file:
        config_data = yaml.safe_load(file)

        for key, value in config_data.items():
            print(config_data[key])

    sys.exit(main())
