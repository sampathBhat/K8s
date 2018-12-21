import kubernetes 

from kubecli import *
from kubecli.kube import api_manager
from kubecli.kube import node

def url(service_name, port_name, namespace='default'):
	"""Return an endpoint URL for an application.
    	:param service_name: unique service_name for the pod
    	:type service_name: str
	:param port_name: name of the port to fetch from list of available ports
	:type port_name: str
        :param namespace: namespace on which service is running
	:type namespace: str
    	:return: absolute URL
    	:rtype: str
    	"""
	response = get(service_name, namespace)
	type = response.spec.type 
	if type == 'ClusterIP':
		ip = response.spec.external_i_ps[0]
		port = find(type, port_name, response.spec.ports)
		url = 'http://{}:{}'.format(ip, port)
	elif type == 'NodePort':
		ip = node.listIPs()['edge'][0]
		port = find(type, port_name, response.spec.ports)
		url = 'http://{}:{}'.format(ip, port)
	return url

def find(type, port_name, response):
        for item  in  response:
           if type == 'ClusterIP' and item.name == port_name:
                return item.target_port
           elif type == 'NodePort' and item.name == port_name:
                return item.node_port
        return None


def create(
        service_manifest,
		namespace='default',
        **kwargs
):
	api = api_manager.get_core_v1_api()
	print('\nCreating service with manifest={} namespace={} options={}'.format(
        service_manifest, namespace, kwargs))
	api.create_namespaced_service(namespace,service_manifest, **kwargs)
	return True

def created(service_name, namespace='default'):
        try:
                response= get(service_name)
        except kubernetes.client.rest.ApiException as e:
                print('Service {} doesnot exist \nThe error response is {}'.format(service_name,e.body))
                return False
        return True

def get(service_name,
		namespace='default',
		**kwargs):
	api = api_manager.get_core_v1_api()
        response = api.read_namespaced_service(service_name,namespace,**kwargs)
	return response

def delete(
		service_name,
		namespace='default',
		**kwargs
):
	api = api_manager.get_core_v1_api()
	print('\nDeleting service with namespace={} servicename={}'.format(
        namespace, service_name))
	api.delete_namespaced_service(service_name,namespace,**kwargs)
	return True
