import json
import yaml
	
def read_json(file=None, text=None):
	if file is not None:
		with open(file) as json_file:
			json_content = json.load(json_file)
	elif text is not None:
		json_content = json.loads(text)
	else:
	    json_content = None
	return json_content
	
def read_yaml(file=None, text=None):
	if file is not None:
		with open(file) as yaml_file:
			yaml_content = yaml.load(yaml_file)
	elif text is not None:
		yaml_content = yaml.load(text)
	else:
	    yaml_content = None
	return yaml_content
	

def read_and_update_json(file, dictionary=None):
	if dictionary is None:
		return read_json(file)
	
	json = None
	return json

def read_and_update_yaml(file, dictionary=None):
	if dictionary is None:
		return read_yaml(file)
	
	yaml = None
	return yaml
