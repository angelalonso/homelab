import yaml

def loadObjectsStruct(objects_file):
    try:
        with open(objects_file) as file:
            objects = yaml.load(file, Loader=yaml.FullLoader)
    except FileNotFoundError:
        return None
    return objects


if __name__ == '__main__':
    objects_file = 'objects.yaml'
    objects_struct = loadObjectsStruct(objects_file)

