import yaml

with open(r'./config.yaml') as file:
  config_data = yaml.safe_load(file)

  for key, value in config_data.items():
      print(config_data[key])
