import kubernetes 

from kubecli import *
from kubecli.kube import api_manager

def url(endpoint_name, namespace='default'):

	"""Return an endpoint URL for an application.
    	:param endpoint_name: unique service_name for the pod
    	:type endpoint_name: str
	:param namespace: namespace on which service is running
	:type namespace: str
    	:return: absolute URL
    	:rtype: str
    	"""
	response = get(endpoint_name, namespace)
	ip = response.subsets[0].addresses[0].ip
	port = response.subsets[0].ports[0].port
	url = 'http://{}:{}'.format(ip, port)
	return url

def get(endpoint_name,
		namespace='default',
		**kwargs):
	api = api_manager.get_core_v1_api()
        response = api.read_namespaced_endpoints(endpoint_name,namespace,**kwargs)
	return response
