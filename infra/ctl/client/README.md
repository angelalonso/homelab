# How to use this

## Add an object
### Using a file
''' client.py add host filename '''  
, where filename has to be proper yaml-formatted.  
Note:  the filename will be taken as the name of the object  
  
### Using a folder
''' client.py add host path '''  
, where all files within path will be read and they all have to be proper yaml-formatted
Remember:  the filename will be taken as the name of the object  

### Using a YAML string
''' client.py add host "'hostname': {'mac_address': 'aa:bb:cc:dd:ee:ff'}" '''  
, where all files within path will be read and they all have to be proper yaml-formatted
