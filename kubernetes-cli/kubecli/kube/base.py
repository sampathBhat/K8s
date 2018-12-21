import os
import urllib3

from kubernetes.client.configuration import Configuration
from kubernetes.config import kube_config
from kubernetes.client import api_client

#from kubecli.kube import api_manager

class Config:
    __instance = None
    DEFAULT_HOST = '127.0.0.1'

    @staticmethod
    def getInstance():
        """ Static access method. """
        if Config.__instance == None:
            Config()
        return Config.__instance

    def __init__(self):
        self.config = None
        self.clnt = None
        """ Virtually private constructor. """
        if Config.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            Config.__instance = self

    def url(self):
        if self.config is None:
            return None
        return self.config.host

    def client(self):
        if self.clnt is None:
            self.clnt = api_client.ApiClient(configuration=self.config)
        return self.clnt

    def build(self, url=None):
        config = Configuration()
        config.host = None

        if os.path.exists(
            os.path.expanduser(kube_config.KUBE_CONFIG_DEFAULT_LOCATION)):
            kube_config.load_kube_config(client_configuration=config)
        else:
            print('Unable to load config from %s' %kube_config.KUBE_CONFIG_DEFAULT_LOCATION)
        if url is None:
            url = 'http://%s:8085' % Config.DEFAULT_HOST
        try:
            urllib3.PoolManager().request('GET', url)
            config.host = url
            config.verify_ssl = False
            urllib3.disable_warnings()
        except urllib3.exceptions.HTTPError:
            raise urllib3.exceptions.HTTPError('Unable to find a running Kubernetes instance')

        self.config = config
        #Resetting old Client & Related API's
        self.clnt = None
#       api_manager.reset()

        print('Running test against : %s' % config.host)
        return config

