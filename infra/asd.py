import yaml

def getSecrets(filename):
    with open(filename) as file:
        secrets = yaml.safe_load(file)
    return secrets


if __name__ == "__main__":
    SECRETS_FILE = './secrets.yaml'
    print(getSecrets(SECRETS_FILE))
