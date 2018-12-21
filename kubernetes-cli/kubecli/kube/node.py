import kubernetes

from kubecli import *
from kubecli.kube import api_manager

def list():
	api = api_manager.get_core_v1_api()
        response = api.list_node()
	return response

def listIPs():
	response = list()
	nodes = {'control':[],'edge':[], 'worker':[]}

	for item in response.items:
		labels = item.metadata.labels
		ip = item.status.addresses[0].address
		if 'is_control' in labels:
			nodes['control'].append(ip)
		elif 'is_edge' in labels:
			nodes['edge'].append(ip)
		else:
			nodes['worker'].append(ip)
	return nodes
