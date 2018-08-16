"""
Tensorflow wheel files builds and jobs trigger application.
"""

# Packages
import os
import time
import json
import urllib3
import requests


class TensorflowBuildTrigger:
    def __init__(self):
        self.namespace = os.getenv('OCP_NAMESPACE', '')  # set default inplace default quotes
        self.url = os.getenv('OCP_URL', '')  # set default inplace default quotes
        self.access_token = os.getenv('OCP_TOKEN', '')  # set default inplace default quotes
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(self.access_token),
            'Accept': 'application/json',
            'Connection': 'close'
        }
        # Application Variables
        self.BUILD_MAP = os.getenv('BUILD_MAP', "{}")

        # Resource Quota Variable
        self.RESOURCE_QUOTA = os.getenv('RESOURCE_QUOTA', "1")
        self.QUOTA_NAME = os.getenv('QUOTA_NAME')
        self.RESOURCE_LIMITS_CPU = os.getenv('RESOURCE_LIMITS_CPU')
        self.RESOURCE_LIMITS_MEMORY = os.getenv('RESOURCE_LIMITS_MEMORY')

        # Buildconfig and Imagestream Variables
        self.GENERIC_WEBHOOK_SECRET = os.getenv('GENERIC_WEBHOOK_SECRET', 'tf-build-secret')
        self.SOURCE_REPOSITORY = os.getenv('SOURCE_REPOSITORY',
                                           'https://github.com/thoth-station/tensorflow-build-s2i.git')
        self.BAZEL_VERSION = os.getenv('BAZEL_VERSION', '0.11.0')
        self.VERSION = os.getenv('VERSION', '1')
        self.S2I_IMAGE = os.getenv('S2I_IMAGE')

        # Job Variables
        self.CUSTOM_BUILD = os.getenv('CUSTOM_BUILD', "bazel build --copt=-mavx --copt=-mavx2 --copt=-mfma "
                                                      "--copt=-mfpmath=both --copt=-msse4.2  "
                                                      "--cxxopt='-D_GLIBCXX_USE_CXX11_ABI=0' "
                                                      "--verbose_failures "
                                                      "//tensorflow/tools/pip_package:build_pip_package")
        self.BUILD_OPTS = os.getenv('BUILD_OPTS', "")
        self.TF_CUDA_VERSION = os.getenv('TF_CUDA_VERSION', "9.2")
        self.TF_CUDA_COMPUTE_CAPABILITIES = os.getenv('TF_CUDA_COMPUTE_CAPABILITIES', '3.0,3.5,5.2,6.0,6.1,7.0')
        self.TF_CUDNN_VERSION = os.getenv('TF_CUDNN_VERSION', "7")
        self.CUDA_TOOLKIT_PATH = os.getenv('CUDA_TOOLKIT_PATH', "/usr/local/cuda")
        self.CUDNN_INSTALL_PATH = os.getenv('CUDNN_INSTALL_PATH', "/usr/local/cuda")
        self.GCC_HOST_COMPILER_PATH = os.getenv('GCC_HOST_COMPILER_PATH', "/usr/bin/gcc")
        self.TF_NEED_OPENCL_SYCL = os.getenv('TF_NEED_OPENCL_SYCL', "0")
        self.TF_CUDA_CLANG = os.getenv('TF_CUDA_CLANG', "0")
        self.TF_NEED_JEMALLOC = os.getenv('TF_NEED_JEMALLOC', "1")
        self.TF_NEED_GCP = os.getenv('TF_NEED_GCP', "0")
        self.TF_NEED_VERBS = os.getenv('TF_NEED_VERBS', "0")
        self.TF_NEED_HDFS = os.getenv('TF_NEED_HDFS', "0")
        self.TF_ENABLE_XLA = os.getenv('TF_ENABLE_XLA', "0")
        self.TF_NEED_OPENCL = os.getenv('TF_NEED_OPENCL', "0")
        self.TF_NEED_CUDA = os.getenv('TF_NEED_CUDA', "0")
        self.TF_NEED_MPI = os.getenv('TF_NEED_MPI', "0")
        self.TF_NEED_GDR = os.getenv('TF_NEED_GDR', "0")
        self.TF_NEED_S3 = os.getenv('TF_NEED_S3', "0")
        self.TF_NEED_KAFKA = os.getenv('TF_NEED_KAFKA', "0")
        self.TF_NEED_OPENCL_SYCL = os.getenv('TF_NEED_OPENCL_SYCL', "0")
        self.TF_DOWNLOAD_CLANG = os.getenv('TF_DOWNLOAD_CLANG', "0")
        self.TF_SET_ANDROID_WORKSPACE = os.getenv('TF_SET_ANDROID_WORKSPACE', "0")
        self.TF_NEED_TENSORRT = os.getenv('TF_NEED_TENSORRT', "0")
        self.NCCL_INSTALL_PATH = os.getenv('NCCL_INSTALL_PATH', "/usr/local/nccl-2.2")
        self.TEST_WHEEL_FILE = os.getenv('TEST_WHEEL_FILE', "y")
        self.TF_GIT_BRANCH = os.getenv('TF_GIT_BRANCH', "r1.9")
        self.SESHETA_GITHUB_ACCESS_TOKEN = os.getenv('GIT_TOKEN', "")
        self.GIT_RELEASE_REPO = os.getenv('GIT_RELEASE_REPO', "https://github.com/AICoE/tensorflow-wheels.git")

    def get_imagestream(self, application_build_name):
        imagestream_get_endpoint = '{}/apis/image.openshift.io/v1/namespaces/{}/imagestreams/{}'.format(self.url,
                                                                                                        self.namespace,
                                                                                                        application_build_name)
        imagestream_get_response = requests.get(imagestream_get_endpoint, headers=self.headers, verify=False)
        print("Status code for imagestream GET request: ", imagestream_get_response.status_code)
        if imagestream_get_response.status_code == 200:
            return True
        else:
            print("Error for imagestream GET request: ", imagestream_get_response.text)
            return False

    def imagestream_template(self, application_build_name):
        imagestream = {
            "kind": "ImageStream",
            "apiVersion": "image.openshift.io/v1",
            "metadata": {
                "name": application_build_name,
                "labels": {
                    "appTypes": "tensorflow-build-image",
                    "appName": application_build_name
                }
            },
            "spec": {
                "lookupPolicy": {
                    "local": True
                }
            }
        }
        return imagestream

    def create_imagestream(self, imagestream):
        imagestream_endpoint = '{}/apis/image.openshift.io/v1/namespaces/{}/imagestreams'.format(self.url,
                                                                                                 self.namespace)
        imagestream_response = requests.post(imagestream_endpoint, json=imagestream, headers=self.headers, verify=False)
        print("Status code for imagestream POST request: ", imagestream_response.status_code)
        if imagestream_response.status_code == 201:
            return True
        else:
            print("Error for imagestream POST request: ", imagestream_response.text)
            return False

    def get_buildconfig(self, application_build_name):
        buildconfig_get_endpoint = '{}/apis/build.openshift.io/v1/namespaces/{}/buildconfigs/{}'.format(self.url,
                                                                                                        self.namespace,
                                                                                                        application_build_name)
        buildconfig_get_response = requests.get(buildconfig_get_endpoint, headers=self.headers, verify=False)
        print("Status code for BuildConfig GET request: ", buildconfig_get_response.status_code)
        if buildconfig_get_response.status_code == 200:
            return True
        else:
            print("Error for Buildconfig GET request: ", buildconfig_get_response.text)
            return False

    def builconfig_template(self, application_build_name, docker_file_path, nb_python_ver):
        buildconfig = {
            "kind": "BuildConfig",
            "apiVersion": "build.openshift.io/v1",
            "metadata": {
                "name": application_build_name,
                "labels": {
                    "appTypes": "tensorflow-build-image",
                    "appName": application_build_name
                }
            },
            "spec": {
                "triggers": [
                    {
                        "type": "ConfigChange"
                    },
                    {
                        "type": "ImageChange"
                    },
                    {
                        "type": "Generic",
                        "generic": {
                            "secret": self.GENERIC_WEBHOOK_SECRET,
                            "allowEnv": True
                        }
                    }
                ],
                "source": {
                    "type": "Git",
                    "git": {
                        "uri": self.SOURCE_REPOSITORY,
                        "ref": "master"
                    }
                },
                "strategy": {
                    "type": "Docker",
                    "dockerStrategy": {
                        "noCache": True,
                        "dockerfilePath": docker_file_path,
                        "from": {
                            "kind": "DockerImage",
                            "name": self.S2I_IMAGE
                        },
                        "env": [
                            {
                                "name": "NB_PYTHON_VER",
                                "value": nb_python_ver
                            },
                            {
                                "name": "BAZEL_VERSION",
                                "value": self.BAZEL_VERSION
                            }
                        ]
                    }
                },
                "output": {
                    "to": {
                        "kind": "ImageStreamTag",
                        "name": application_build_name + ":" + self.VERSION
                    }
                },
                "resources": {
                    "limits": {
                        "cpu": self.RESOURCE_LIMITS_CPU,
                        "memory": self.RESOURCE_LIMITS_MEMORY
                    },
                    "requests": {
                        "cpu": self.RESOURCE_LIMITS_CPU,
                        "memory": self.RESOURCE_LIMITS_MEMORY
                    }
                }
            }
        }
        return buildconfig

    def create_buildconfig(self, buildconfig):
        buildconfig_endpoint = '{}/apis/build.openshift.io/v1/namespaces/{}/buildconfigs'.format(self.url,
                                                                                                 self.namespace)
        buildconfig_response = requests.post(buildconfig_endpoint, json=buildconfig, headers=self.headers, verify=False)
        print("Status code for Buildconfig POST request: ", buildconfig_response.status_code)
        if buildconfig_response.status_code == 201:
            return True
        else:
            print("Error for Buildconfig POST request: ", buildconfig_response.text)
            return False

    def trigger_build(self, application_build_name, nb_python_ver):
        trigger_payload = {
            "git": {
                "uri": self.SOURCE_REPOSITORY,
                "ref": "master"
            },
            "env": [
                {
                    "name": "NB_PYTHON_VER",
                    "value": nb_python_ver
                },
                {
                    "name": "BAZEL_VERSION",
                    "value": self.BAZEL_VERSION
                }
            ]
        }
        build_trigger_api = '{}/apis/build.openshift.io/v1/namespaces/{}/buildconfigs/{}/webhooks/{}/generic'.format(
            self.url,
            self.namespace,
            application_build_name,
            self.GENERIC_WEBHOOK_SECRET)
        build_trigger_response = requests.post(build_trigger_api, json=trigger_payload, headers=self.headers,
                                               verify=False)
        print("Status code for Build Webhook Trigger request: ", build_trigger_response.status_code)
        if build_trigger_response.status_code == 200:
            return True
        else:
            print("Error for Build Webhook Trigger request: ", build_trigger_response.text)
            return False

    def get_latest_build(self, application_build_name):
        latest_build_endpoint = '{}/apis/build.openshift.io/v1/namespaces/{}/buildconfigs/{}'.format(self.url,
                                                                                                     self.namespace,
                                                                                                     application_build_name)
        latest_build_response = requests.get(latest_build_endpoint, headers=self.headers, verify=False)
        print("Status code for latest Buildconfig GET request: ", latest_build_response.status_code)
        if 'status' in latest_build_response.json():
            latest_build_status = latest_build_response.json().get('status')
            if isinstance(latest_build_status, dict):
                return latest_build_status.get('lastVersion')
            else:
                raise Exception('Error in fetching the lastVersion from the latest Buildconfig status: {}'.format(
                    latest_build_response.json().get('status')))
        else:
            raise Exception('Error in latest Buildconfig GET response: {}'.format(latest_build_response.text))

    def get_status_build(self, build_name):
        build_status_endpoint = '{}/apis/build.openshift.io/v1/namespaces/{}/builds/{}'.format(self.url,
                                                                                               self.namespace,
                                                                                               build_name)
        build_status_response = requests.get(build_status_endpoint, headers=self.headers, verify=False)
        print("Status code for latest Build's GET request: ", build_status_response.status_code)
        if 'status' in build_status_response.json():
            build_status = build_status_response.json().get('status')
            if isinstance(build_status, dict):
                return build_status
            else:
                raise Exception('Error in fetching the status of the latest Build: {}'.format(
                    build_status_response.json().get('status')))
        else:
            raise Exception('Error in latest Builds GET response: {}'.format(build_status_response.text))

    def get_job(self, application_name):
        job_get_endpoint = '{}/apis/batch/v1/namespaces/{}/jobs/{}'.format(self.url, self.namespace,
                                                                           application_name)
        job_get_response = requests.get(job_get_endpoint, headers=self.headers, verify=False)
        print("Status code for job GET request: ", job_get_response.status_code)
        if job_get_response.status_code == 200:
            return True
        else:
            print("Error for job GET request: ", job_get_response.text)
            return False

    def get_logs(self, build_pod):
        build_pod_endpoint = '{}/api/v1/namespaces/{}/pods/{}/log'.format(self.url, self.namespace, build_pod)
        build_pod_logs = requests.get(build_pod_endpoint, headers=self.headers, verify=False)
        print("Status code for build pod log GET request: ", build_pod_logs.status_code)
        if build_pod_logs.status_code == 200:
            with open('{}.txt'.format(build_pod), 'w') as f:
                f.write(build_pod_logs.text)
            print("Log of:", build_pod)
            return True
        else:
            print("Error for build pod log GET request: ", build_pod_logs.text)
            return False

    def job_template(self, application_name, builder_imagesream, nb_python_ver):
        job = {
            "kind": "Job",
            "apiVersion": "batch/v1",
            "metadata": {
                "name": application_name,
                "labels": {
                    "appTypes": "tensorflow-build-job",
                    "appName": application_name
                }
            },
            "spec": {
                "template": {
                    "metadata": {
                        "labels": {
                            "appTypes": "tensorflow-build-job",
                            "deploymentconfig": application_name,
                            "appName": application_name
                        }
                    },
                    "spec": {
                        "containers": [
                            {
                                "env": [
                                    {
                                        "name": "CUSTOM_BUILD",
                                        "value": self.CUSTOM_BUILD
                                    },
                                    {
                                        "name": "BUILD_OPTS",
                                        "value": self.BUILD_OPTS
                                    },
                                    {
                                        "name": "TF_CUDA_VERSION",
                                        "value": self.TF_CUDA_VERSION
                                    },
                                    {
                                        "name": "TF_CUDA_COMPUTE_CAPABILITIES",
                                        "value": self.TF_CUDA_COMPUTE_CAPABILITIES
                                    },
                                    {
                                        "name": "TF_CUDNN_VERSION",
                                        "value": self.TF_CUDNN_VERSION
                                    },
                                    {
                                        "name": "TF_NEED_OPENCL_SYCL",
                                        "value": self.TF_NEED_OPENCL_SYCL
                                    },
                                    {
                                        "name": "TF_CUDA_CLANG",
                                        "value": self.TF_CUDA_CLANG
                                    },
                                    {
                                        "name": "GCC_HOST_COMPILER_PATH",
                                        "value": self.GCC_HOST_COMPILER_PATH
                                    },
                                    {
                                        "name": "CUDA_TOOLKIT_PATH",
                                        "value": self.CUDA_TOOLKIT_PATH
                                    },
                                    {
                                        "name": "CUDNN_INSTALL_PATH",
                                        "value": self.CUDNN_INSTALL_PATH
                                    },
                                    {
                                        "name": "TF_NEED_JEMALLOC",
                                        "value": self.TF_NEED_JEMALLOC
                                    },
                                    {
                                        "name": "TF_NEED_GCP",
                                        "value": self.TF_NEED_GCP
                                    },
                                    {
                                        "name": "TF_NEED_VERBS",
                                        "value": self.TF_NEED_VERBS
                                    },
                                    {
                                        "name": "TF_NEED_HDFS",
                                        "value": self.TF_NEED_HDFS
                                    },
                                    {
                                        "name": "TF_ENABLE_XLA",
                                        "value": self.TF_ENABLE_XLA
                                    },
                                    {
                                        "name": "TF_NEED_OPENCL",
                                        "value": self.TF_NEED_OPENCL
                                    },
                                    {
                                        "name": "TF_NEED_CUDA",
                                        "value": self.TF_NEED_CUDA
                                    },
                                    {
                                        "name": "TF_NEED_MPI",
                                        "value": self.TF_NEED_MPI
                                    },
                                    {
                                        "name": "TF_NEED_GDR",
                                        "value": self.TF_NEED_GDR
                                    },
                                    {
                                        "name": "TF_NEED_S3",
                                        "value": self.TF_NEED_S3
                                    },
                                    {
                                        "name": "TF_NEED_KAFKA",
                                        "value": self.TF_NEED_KAFKA
                                    },
                                    {
                                        "name": "TF_NEED_OPENCL_SYCL",
                                        "value": self.TF_NEED_OPENCL_SYCL
                                    },
                                    {
                                        "name": "TF_DOWNLOAD_CLANG",
                                        "value": self.TF_DOWNLOAD_CLANG
                                    },
                                    {
                                        "name": "TF_SET_ANDROID_WORKSPACE",
                                        "value": self.TF_SET_ANDROID_WORKSPACE
                                    },
                                    {
                                        "name": "TF_NEED_TENSORRT",
                                        "value": self.TF_NEED_TENSORRT
                                    },
                                    {
                                        "name": "NCCL_INSTALL_PATH",
                                        "value": self.NCCL_INSTALL_PATH
                                    },
                                    {
                                        "name": "NB_PYTHON_VER",
                                        "value": nb_python_ver
                                    },
                                    {
                                        "name": "BAZEL_VERSION",
                                        "value": self.BAZEL_VERSION
                                    },
                                    {
                                        "name": "TF_GIT_BRANCH",
                                        "value": self.TF_GIT_BRANCH
                                    },
                                    {
                                        "name": "TEST_WHEEL_FILE",
                                        "value": self.TEST_WHEEL_FILE
                                    },
                                    {
                                        "name": "GIT_RELEASE_REPO",
                                        "value": self.GIT_RELEASE_REPO
                                    },
                                    {
                                        "name": "GIT_TOKEN",
                                        "value": self.SESHETA_GITHUB_ACCESS_TOKEN
                                    }
                                ],
                                "name": application_name,
                                "image": builder_imagesream,
                                "command": ["/entrypoint", "/usr/libexec/s2i/run"],
                                "resources": {
                                    "limits": {
                                        "cpu": self.RESOURCE_LIMITS_CPU,
                                        "memory": self.RESOURCE_LIMITS_MEMORY
                                    },
                                    "requests": {
                                        "cpu": self.RESOURCE_LIMITS_CPU,
                                        "memory": self.RESOURCE_LIMITS_MEMORY
                                    }
                                }
                            }
                        ],
                        "restartPolicy": "Never"
                    }
                }
            }
        }
        return job

    def create_job(self, job):
        job_endpoint = '{}/apis/batch/v1/namespaces/{}/jobs'.format(self.url, self.namespace)
        job_response = requests.post(job_endpoint, json=job, headers=self.headers, verify=False)
        print("Status code for job POST request: ", job_response.status_code)
        if job_response.status_code == 201:
            return True
        else:
            print("Error for job POST request: ", job_response.text)
            return False

    def update_job(self, job, application_name):
        job_endpoint = '{}/apis/batch/v1/namespaces/{}/jobs/{}'.format(self.url, self.namespace, application_name)
        job_response = requests.post(job_endpoint, json=job, headers=self.headers, verify=False)
        print("Status code for job PUT request: ", job_response.status_code)
        if job_response.status_code == 200:
            return True
        else:
            print("Error for job PUT request: ", job_response.text)
            return False

    def get_job_status(self, application_name):
        job_status_endpoint = '{}/apis/batch/v1/namespaces/{}/jobs/{}'.format(self.url, self.namespace,
                                                                              application_name)
        job_status_response = requests.get(job_status_endpoint, headers=self.headers, verify=False)
        print("Status code for job GET status request: ", job_status_response.status_code)
        if job_status_response.status_code == 200:
            job_details = job_status_response.json().get('status')
            print('Job Status: ', job_details)
            if job_details and 'active' in job_details:
                return True
            else:
                return False
        else:
            print("Error for job GET request: ", job_status_response.text)
            return False

    def delete_job(self, application_name):
        job_delete_endpoint = '{}/apis/batch/v1/namespaces/{}/jobs/{}'.format(self.url, self.namespace,
                                                                              application_name)
        job_delete_response = requests.delete(job_delete_endpoint, headers=self.headers, verify=False)
        print("Status code for job DELETE request: ", job_delete_response.status_code)
        if job_delete_response.status_code == 200:
            return True
        else:
            print("Error for job DELETE request: ", job_delete_response.text)
            return False

    def get_usable_Gi_quota(self, quota_val):
        max_usable_quota = str(int(quota_val.strip("Gi")) - (int(self.RESOURCE_LIMITS_MEMORY.strip("Gi")) + 3)) + 'Gi'
        return max_usable_quota

    def get_usable_Mi_quota(self, quota_val):
        max_usable_quota = str(
            (int(quota_val.strip("Gi")) - (int(self.RESOURCE_LIMITS_MEMORY.strip("Gi")) + 3)) * 1000) + 'Mi'
        return max_usable_quota

    def get_resource_quota(self, quota_name):
        resource_quota_endpoint = '{}/api/v1/namespaces/{}/resourcequotas/{}'.format(self.url, self.namespace,
                                                                                     quota_name)
        resource_quota_response = requests.get(resource_quota_endpoint, headers=self.headers, verify=False)
        print("Status code for resource quota GET request: ", resource_quota_response.status_code)
        if resource_quota_response.status_code == 200:
            print("Resource Quota: ", resource_quota_response.json())
            if 'status' in resource_quota_response.json() and resource_quota_response.json().get('status'):
                quota = resource_quota_response.json().get('status')
                print("Used Quota: \n CPU:{} \n Memory:{}".format(quota['used'].get("limits.cpu", ""),
                                                                  quota['used'].get("limits.memory", "")))
                if 'Gi' in quota['used'].get("limits.memory", "") and quota['used'].get(
                        "limits.memory") > self.get_usable_Gi_quota(quota['hard'].get("limits.memory")):
                    return True
                if 'Mi' in quota['used'].get("limits.memory", "") and quota['used'].get(
                        "limits.memory") > self.get_usable_Mi_quota(quota['hard'].get("limits.memory")):
                    return True
                if 'm' in quota['used'].get("limits.cpu", "") and quota['used'].get("limits.cpu") > str(
                        (int(quota['hard'].get("limits.cpu")) - (int(self.RESOURCE_LIMITS_CPU) + 3)) * 1000) + 'm':
                    return True
                if quota['used'].get("limits.cpu") > str(
                        int(quota['hard'].get("limits.cpu")) - (int(self.RESOURCE_LIMITS_CPU) + 3)):
                    return True
                return False
            else:
                print("Error for resource quota status request: ", resource_quota_response.text)
                return False
        else:
            print("Error for resource quota GET request: ", resource_quota_response.text)
            return False

    def main(self):
        if not self.url or not self.namespace or not self.access_token:
            raise Exception("Release Trigger can't start! OCP credentials are not provided!")
        if self.BUILD_MAP:
            for py_version, os_details in json.loads(self.BUILD_MAP).items():
                for os_version, image_details in os_details.items():
                    try:
                        application_build_name = "tf-{}-build-image-{}".format(os_version.lower(),
                                                                               py_version.replace('.', ''))
                        application_name = 'tf-{}-build-job-{}'.format(os_version.lower(), py_version.replace('.', ''))
                        builder_imagesream = '{}:{}'.format(application_build_name, self.VERSION)
                        nb_python_ver = py_version
                        docker_file_path = 'Dockerfile.{}'.format(os_version.lower())
                        print("-------------------VARIABLES-------------------------")
                        print("APPLICATION_BUILD_NAME: ", application_build_name)
                        print("APPLICATION_NAME: ", application_name)
                        print("BUILDER_IMAGESTREAM: ", builder_imagesream)
                        print("PYTHON VERSION: ", nb_python_ver)
                        print("DOCKERFILE: ", docker_file_path)
                        for var_key, var_val in image_details.items():
                            self.__dict__[var_key] = var_val
                            print("{}: ".format(var_key), var_val)
                        print("-----------------------------------------------------")
                        if not self.get_imagestream(application_build_name=application_build_name):
                            imagestream = self.imagestream_template(application_build_name=application_build_name)
                            generated_img = self.create_imagestream(imagestream=imagestream)
                            if not generated_img:
                                raise Exception('Image could not be generated for {}'.format(application_build_name))
                        if not self.get_buildconfig(application_build_name=application_build_name):
                            buildconfig = self.builconfig_template(application_build_name=application_build_name,
                                                                   docker_file_path=docker_file_path,
                                                                   nb_python_ver=nb_python_ver)
                            created_build = self.create_buildconfig(buildconfig=buildconfig)
                            if not created_build:
                                raise Exception('Build could not be created for {}'.format(application_build_name))
                        else:
                            latest_build_id = self.get_latest_build(application_build_name=application_build_name)
                            status = self.get_status_build('{}-{}'.format(application_build_name, str(latest_build_id)))
                            if status.get('phase') != 'Running' or status.get('phase') != 'Pending':
                                self.trigger_build(application_build_name=application_build_name,
                                                   nb_python_ver=nb_python_ver)

                        latest_build_id = self.get_latest_build(application_build_name=application_build_name)
                        status = self.get_status_build('{}-{}'.format(application_build_name, str(latest_build_id)))
                        while status.get('phase') in ['Running', 'Pending', 'New']:
                            if status.get('phase') == 'New' and status.get('reason') == 'CannotCreateBuildPod':
                                print('Build failed due to', status.get('reason'))
                                break
                            time.sleep(90)
                            status = self.get_status_build('{}-{}'.format(application_build_name, str(latest_build_id)))

                        if status.get('phase') == 'Failed':
                            for tries in range(3):
                                latest_build_id = self.get_latest_build(application_build_name=application_build_name)
                                build_pod_name = '{}-{}-build'.format(application_build_name, latest_build_id)
                                log_status = self.get_logs(build_pod=build_pod_name)
                                if log_status and 'gpg: keyserver receive failed: Keyserver error' in open(
                                        build_pod_name + ".txt").read():
                                    trigger_status = self.trigger_build(application_build_name=application_build_name,
                                                                        nb_python_ver=nb_python_ver)
                                    if trigger_status:
                                        print("Rebuild try:", tries + 1)
                                        latest_build_id = self.get_latest_build(
                                            application_build_name=application_build_name)
                                        status = self.get_status_build(
                                            '{}-{}'.format(application_build_name, str(latest_build_id)))
                                        while status.get('phase') in ['Running', 'Pending', 'New']:
                                            if status.get('phase') == 'New' and status.get(
                                                    'reason') == 'CannotCreateBuildPod':
                                                print('Build failed due to', status.get('reason'))
                                                break
                                            time.sleep(90)
                                            status = self.get_status_build(
                                                '{}-{}'.format(application_build_name, str(latest_build_id)))
                                        if status.get('phase') == 'Failed':
                                            continue
                                        else:
                                            break
                                    else:
                                        raise Exception('Build can not be re triggered! check the error in log.')
                                else:
                                    raise Exception('Build Failed due to unknown reason! check the error in log.')

                        if status.get('phase') == 'Complete':
                            if not self.get_job(application_name=application_name):
                                job = self.job_template(application_name=application_name,
                                                        builder_imagesream=builder_imagesream,
                                                        nb_python_ver=nb_python_ver)
                                self.create_job(job=job)
                            else:
                                if not self.get_job_status(application_name=application_name):
                                    job_deleted = self.delete_job(application_name=application_name)
                                    while self.get_job_status(application_name=application_name):
                                        time.sleep(5)
                                    if job_deleted:
                                        job = self.job_template(application_name=application_name,
                                                                builder_imagesream=builder_imagesream,
                                                                nb_python_ver=nb_python_ver)
                                        self.create_job(job=job)

                        else:
                            raise Exception("Build didn't complete successfully, Please check openshift events. Build "
                                            "{} status: {}".format(application_build_name, status))
                    except Exception as e:
                        print('Exception: ', e)
                        print('Error in Tensorflow Build or Job trigger! Please refer the above log, Starting the next '
                              'one in queue!')
                        pass
                    print("IS RESOURCE QUOTA SET ?", self.RESOURCE_QUOTA)
                    if self.RESOURCE_QUOTA == "1":
                        if self.QUOTA_NAME:
                            print("QUOTA_NAME", self.QUOTA_NAME)
                            wait_quota = self.get_resource_quota(quota_name=self.QUOTA_NAME)
                        else:
                            print("QUOTA_NAME", '{}-quota'.format(self.namespace))
                            wait_quota = self.get_resource_quota(quota_name='{}-quota'.format(self.namespace))
                        while wait_quota:
                            print("Waiting for available quota")
                            time.sleep(180)
                            wait_quota = self.get_resource_quota(quota_name='{}-quota'.format(self.namespace))
        else:
            raise Exception("Issue in BUILD_MAP!!!")


if __name__ == '__main__':
    urllib3.disable_warnings()
    tensorflow_build_trigger = TensorflowBuildTrigger()
    tensorflow_build_trigger.main()
