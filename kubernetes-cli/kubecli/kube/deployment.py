import time,kubernetes

from kubecli import *
from kubecli.kube import api_manager
from kubecli.kube import pod
from kubernetes.client.models import v1_delete_options

def create(
        deployment_manifest,
        namespace='default',
        wait_for_completion=False,
        timeout_sec=120,
		**kwargs
):
	api = api_manager.get_apps_v1_api()
	print('\nCreating Deployment with manifest={} namespace={} options={}'.format(
        deployment_manifest, namespace, kwargs))
	api.create_namespaced_deployment(namespace, deployment_manifest, **kwargs)
	if wait_for_completion:
		deployment_name = deployment_manifest['metadata']['name']
		print("\nWaiting for {} deployment to complete...".format(
                deployment_name))
		_deployment_wait(deployment_name,namespace,timeout_sec)
		time.sleep(10)
		pod_name=get_pod_name(deployment_name)
		pod_deployment_wait(pod_name,namespace,timeout_sec)
	return True

def pod_deployment_wait(
                                pod_name,
                namespace,
                timeout_sec
):
        end_time = time.time() + timeout_sec
        while time.time() < end_time:
                if pod.created(pod_name,namespace):
                        break

                time.sleep(1)


def _deployment_wait(
				deployment_name,
                namespace,
                timeout_sec
):
	end_time = time.time() + timeout_sec
	while time.time() < end_time:
		if created(deployment_name,namespace):
			break
		time.sleep(1)

def _teardown_wait(
                deployment_name,
				namespace,
                timeout_sec
):
	end_time = time.time() + timeout_sec
	while time.time() < end_time:
		if not created(deployment_name,namespace):
			break
		time.sleep(1)


def create_and_wait(
        deployment_manifest,
        namespace='default',
        wait_for_completion=True,
        timeout_sec=120,
		**kwargs
):
    return create(
        deployment_manifest,
        namespace,
        wait_for_completion,
        timeout_sec,
		**kwargs
        )

def created(deployment_name, namespace='default'):
        try:
                response= get(deployment_name)
        except kubernetes.client.rest.ApiException as e:
                print('Deployment {} doesnot exist \nThe error response is {}'.format(deployment_name,e.body))
                return False
        return True


def get(deployment_name, namespace='default'):
    api= api_manager.get_apps_v1_api()
    response = api.read_namespaced_deployment(deployment_name,namespace)
    return response

#def execute(namespace='default', deployment_name, cmd):

def delete(
        deployment_name,
        namespace = 'default',
        propagation_policy='Foreground',
        wait_for_completion=False,
        timeout_sec=120
):
        api = api_manager.get_apps_v1_api()
        print('\nDeleting Deployment with namespace={} deploymentname={}'.format(
        namespace, deployment_name))
        options = v1_delete_options.V1DeleteOptions(propagation_policy="Foreground" , grace_period_seconds=5)
        api.delete_namespaced_deployment(deployment_name,namespace,body=options)
        if wait_for_completion:
                _teardown_wait(deployment_name,namespace,timeout_sec)

        return True


def delete_and_wait(
        deployment_name,
		namespace = 'default',
        wait_for_completion=True,
        timeout_sec=120
):
    return delete(
        deployment_name,
		namespace,
        wait_for_completion,
        timeout_sec
        )
def get_pod_name(deployment_name,namespace='default'):
	response= list_all_pod(namespace)
	items=response.items
	pod_name=None
	for item in items:
		pod_name=item.metadata.name
		if pod_name.startswith(deployment_name):
			print("The pod name {} for given deployment name is {}".format(pod_name,deployment_name))
			return pod_name
	return None
			
def list_all_pod(namespace='default'):
	api = api_manager.get_core_v1_api()
	response=api.list_namespaced_pod(namespace)
	return response
