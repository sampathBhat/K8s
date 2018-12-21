import json,yaml

from kubernetes.client.apis import core_v1_api
from kubernetes.client.apis import extensions_v1beta1_api

from kubecli import *
from kubecli.kube.base import Config 

config = Config.getInstance()
corev1_api = None
appsv1_api=None
def get_core_v1_api():
	global corev1_api
	if corev1_api is None:
		client = config.client()
		corev1_api = core_v1_api.CoreV1Api(client)
	return corev1_api


def get_apps_v1_api():
        global appsv1_api
        if appsv1_api is None:
                client = config.client()
                appsv1_api = extensions_v1beta1_api.ExtensionsV1beta1Api(client)
        return appsv1_api


def reset():
	global corev1_api
	corev1_api = None
