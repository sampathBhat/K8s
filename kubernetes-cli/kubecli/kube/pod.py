import time,kubernetes

from kubecli import *
from kubecli.kube import api_manager
from kubernetes.stream import stream

def create(
        pod_manifest,
        namespace='default',
        wait_for_completion=False,
        timeout_sec=120,
		**kwargs
):
	api = api_manager.get_core_v1_api()
	print('\nCreating Pod with manifest={} namespace={} options={}'.format(
        pod_manifest, namespace, kwargs))
	api.create_namespaced_pod(namespace, pod_manifest, **kwargs)
	if wait_for_completion:
		pod_name = pod_manifest['metadata']['name']
		print("\nWaiting for {} deployment to complete...".format(
                pod_name))
		_deployment_wait(pod_name,namespace,timeout_sec)
	return True

def _deployment_wait(
				pod_name,
                namespace,
                timeout_sec
):
	end_time = time.time() + timeout_sec
	while time.time() < end_time:
		if created(pod_name,namespace):
			break
		
		time.sleep(1)

def _teardown_wait(
                pod_name,
				namespace,
                timeout_sec
):
	end_time = time.time() + timeout_sec
	while time.time() < end_time:
		if not created(pod_name,namespace):
			break
		time.sleep(1)


def create_and_wait(
        pod_manifest,
        namespace='default',
        wait_for_completion=True,
        timeout_sec=120,
		**kwargs
):
    return create(
        pod_manifest,
        namespace,
        wait_for_completion,
        timeout_sec,
		**kwargs
        )

def created(pod_name, namespace='default'):
        try:
		response= get(pod_name)
        except kubernetes.client.rest.ApiException as e:
		print('Pod {} doesnot exist \nError response is {}'.format(pod_name,e.body))
		return False
	print("The Status of pod {} is {} ".format(pod_name,response.status.phase))
	return response.status.phase == 'Running'

def get(pod_name, namespace='default'):
	api= api_manager.get_core_v1_api()
	response = api.read_namespaced_pod(pod_name,namespace)
	return response

# command is optional .If command is not specified then 'hostname' command will be executed
def execute(pod_name, namespace='default', command='hostname', stdout=True, stdin=False, stderr =True, tty = False):
        api= api_manager.get_core_v1_api()	
	response = stream(api.connect_get_namespaced_pod_exec, pod_name, namespace, command=command, stderr=stderr, stdin=stdin, stdout=stdout, tty=tty)
	return response


def delete(
        pod_name,
		namespace = 'default',
        wait_for_completion=False,
        timeout_sec=120
):
	api = api_manager.get_core_v1_api()
	print('\nDeleting Pod with namespace={} podname={}'.format(
       	namespace, pod_name))
	api.delete_namespaced_pod(pod_name,namespace,body={})
	if wait_for_completion:
		_teardown_wait(pod_name,namespace,timeout_sec)
	return True

def delete_and_wait(
        pod_name,
		namespace = 'default',
        wait_for_completion=True,
        timeout_sec=120
):
    return delete(
        pod_name,
		namespace,
        wait_for_completion,
        timeout_sec
        )
