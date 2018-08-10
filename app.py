"""
Tensorflow wheel files builds and jobs trigger script 
"""

# Packages
import os
import requests


class Tensorflow_Build_Trigger:
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
        # Buildconfig and Imagestream variables
        self.APPLICATION_BUILD_NAME = os.getenv('APPLICATION_NAME', 'tf-fedora28-build-image-36')
        self.GENERIC_WEBHOOK_SECRET = os.getenv('GENERIC_WEBHOOK_SECRET', 'tf-build-secret')
        self.SOURCE_REPOSITORY = os.getenv('SOURCE_REPOSITORY',
                                           'https://github.com/thoth-station/tensorflow-build-s2i.git')
        self.DOCKER_FILE_PATH = os.getenv('DOCKER_FILE_PATH', 'Dockerfile.fedora28')
        self.S2I_IMAGE = os.getenv('S2I_IMAGE', 'registry.fedoraproject.org/f28/s2i-core')
        self.NB_PYTHON_VER = os.getenv('NB_PYTHON_VER', '3.6')
        self.BAZEL_VERSION = os.getenv('BAZEL_VERSION', '0.11.0')
        self.VERSION = os.getenv('VERSION', '1')

        # job variables
        self.APPLICATION_NAME = os.getenv('APPLICATION_NAME', 'tf-fedora28-build-job-36')
        self.BUILDER_IMAGESTREAM = os.getenv('BUILDER_IMAGESTREAM', 'tf-fedora28-build-image-36:1')
        self.CUSTOM_BUILD = os.getenv('CUSTOM_BUILD', "bazel build --copt=-mavx --copt=-mavx2 --copt=-mfma "
                                                      "--copt=-mfpmath=both --copt=-msse4.2  "
                                                      "--cxxopt='-D_GLIBCXX_USE_CXX11_ABI=0' --local_resources 2048,"
                                                      "2.0,1.0 --verbose_failures "
                                                      "//tensorflow/tools/pip_package:build_pip_package")
        self.BUILD_OPTS = os.getenv('BUILD_OPTS', "")
        self.TF_CUDA_VERSION = os.getenv('TF_CUDA_VERSION', "9.2")
        self.TF_CUDA_COMPUTE_CAPABILITIES = os.getenv('TF_CUDA_COMPUTE_CAPABILITIES', "3.03.55.26.06.17.0")
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
        self.SESHETA_GITHUB_ACCESS_TOKEN = os.getenv('SESHETA_GITHUB_ACCESS_TOKEN', "")
        self.GIT_RELEASE_REPO = os.getenv('GIT_RELEASE_REPO', "https://github.com/AICoE/tensorflow-wheels.git")

    def get_imagestream(self):
        imagestream_get_endpoint = '{}/apis/image.openshift.io/v1/namespaces/{}/imagestreams/{}'.format(self.url,
                                                                                                        self.namespace,
                                                                                                        self.APPLICATION_BUILD_NAME)
        imagestream_get_response = requests.get(imagestream_get_endpoint, headers=self.headers, verify=False)
        print(imagestream_get_response.status_code)
        if imagestream_get_response.status_code == 200:
            return True
        else:
            return False

    def imagestream_template(self):
        imagestream = {
            "kind": "ImageStream",
            "apiVersion": "v1",
            "metadata": {
                "name": self.APPLICATION_BUILD_NAME,
                "labels": {
                    "appTypes": "tensorflow-build-image",
                    "appName": self.APPLICATION_BUILD_NAME
                }
            },
            "spec": {
                "lookupPolicy": {
                    "local": true
                }
            }
        }
        return imagestream

    def create_imagestream(self, imagestream):
        imagestream_endpoint = '{}/apis/image.openshift.io/v1/namespaces/{}/imagestreams'.format(self.url,
                                                                                                 self.namespace)
        imagestream_response = requests.post(imagestream_endpoint, json=imagestream, headers=self.headers, verify=False)
        print(imagestream_response.status_code)
        if imagestream_response.status_code == 200:
            return True
        else:
            return False

    def get_buildconfig(self):
        buildconfig_get_endpoint = '{}/apis/build.openshift.io/v1/namespaces/{}/buildconfigs/{}'.format(self.url,
                                                                                                        self.namespace,
                                                                                                        self.APPLICATION_BUILD_NAME)
        buildconfig_get_response = requests.get(buildconfig_get_endpoint, headers=self.headers, verify=False)
        print(buildconfig_get_response.status_code)
        if buildconfig_get_response.status_code == 200:
            return True
        else:
            return False

    def builconfig_template(self):
        buildconfig = {
            "kind": "BuildConfig",
            "apiVersion": "v1",
            "metadata": {
                "name": self.APPLICATION_BUILD_NAME,
                "labels": {
                    "appTypes": "tensorflow-build-image",
                    "appName": self.APPLICATION_BUILD_NAME
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
                            "secret": self.GENERIC_WEBHOOK_SECRET
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
                        "noCache": true,
                        "dockerfilePath": self.DOCKER_FILE_PATH,
                        "from": {
                            "kind": "DockerImage",
                            "name": self.S2I_IMAGE
                        },
                        "env": [
                            {
                                "name": "NB_PYTHON_VER",
                                "value": self.NB_PYTHON_VER
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
                        "name": self.APPLICATION_BUILD_NAME + ":" + self.VERSION
                    }
                },
                "resources": {
                    "limits": {
                        "cpu": "4",
                        "memory": "8Gi"
                    },
                    "requests": {
                        "cpu": "4",
                        "memory": "8Gi"
                    }
                }
            }
        }
        return buildconfig

    def create_buildconfig(self, buildconfig):
        buildconfig_endpoint = '{}/apis/build.openshift.io/v1/namespaces/{}/buildconfigs'.format(self.url,
                                                                                                 self.namespace)
        buildconfig_response = requests.post(buildconfig_endpoint, json=buildconfig, headers=self.headers, verify=False)
        print(buildconfig_response.status_code)

    def trigger_build(self):
        build_trigger_api = 'https://paas.upshift.redhat.com/oapi/v1/namespaces/aicoe/buildconfigs/tf-fedora27-build' \
                            '-image-27/webhooks/tf-build-secret/generic '
        build_trigger_response = requests.get(build_trigger_api, headers=self.headers, verify=False)
        print(build_trigger_response.status_code)
        if build_trigger_response.status_code == 200:
            return True
        else:
            return False

    def get_latest_build(self):
        latest_build_endpoint = '{}/apis/build.openshift.io/v1/namespaces/{}/buildconfigs/{}'.format(self.url,
                                                                                                     self.namespace,
                                                                                                     self.APPLICATION_BUILD_NAME)
        latest_build_response = requests.get(latest_build_endpoint, headers=self.headers, verify=False)
        print(latest_build_response.status_code)
        if 'status' in latest_build_response.json():
            latest_build_status = latest_build_response.json().get('status')
            return latest_build_status.get('lastVersion')
        else:
            # raise
            return ""

    def get_status_build(self, build_name):
        build_status_endpoint = '{}/apis/build.openshift.io/v1/namespaces/{}/builds/{}'.format(self.url,
                                                                                               self.namespace,
                                                                                               build_name)
        build_status_response = requests.get(build_status_endpoint, headers=self.headers, verify=False)
        print(build_status_response.status_code)
        if 'status' in build_status_response.json():
            build_status = build_status_response.json().get('status')
            return build_status.get('phase')
        else:
            # raise
            return ""

    def get_job(self):
        job_get_endpoint = '{}/apis/batch/v1/namespaces/{}/jobs/{}'.format(self.url, self.namespace,
                                                                           self.APPLICATION_NAME)
        job_get_response = requests.get(job_get_endpoint, headers=self.headers, verify=False)
        print(job_get_response.status_code)
        if job_get_response.status_code == 200:
            return True
        else:
            return False

    def job_template(self):
        job = {
            "kind": "Job",
            "apiVersion": "batch/v1",
            "metadata": {
                "name": self.APPLICATION_NAME,
                "labels": {
                    "appTypes": "tensorflow-build-job",
                    "appName": self.APPLICATION_NAME
                }
            },
            "spec": {
                "template": {
                    "metadata": {
                        "labels": {
                            "appTypes": "tensorflow-build-job",
                            "deploymentconfig": self.APPLICATION_NAME,
                            "appName": self.APPLICATION_NAME
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
                                        "value": self.NB_PYTHON_VER
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
                                "name": self.APPLICATION_NAME,
                                "image": self.BUILDER_IMAGESTREAM,
                                "command": ["/entrypoint", "/usr/libexec/s2i/run"],
                                "resources": {
                                    "limits": {
                                        "cpu": "4",
                                        "memory": "8Gi"
                                    },
                                    "requests": {
                                        "cpu": "4",
                                        "memory": "8Gi"
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
        print(job_response.status_code)
        if job_response.status_code == 200:
            return True
        else:
            return False

    def update_job(self, job):
        job_endpoint = '{}/apis/batch/v1/namespaces/{}/jobs/{}'.format(self.url, self.namespace, self.APPLICATION_NAME)
        job_response = requests.post(job_endpoint, json=job, headers=self.headers, verify=False)
        print(job_response.status_code)
        if job_response.status_code == 200:
            return True
        else:
            return False

    def main(self):
        if not self.get_imagestream():
            imagestream = self.imagestream_template()
            self.create_imagestream(imagestream)
        if not self.get_buildconfig():
            buildconfig = self.builconfig_template()
            self.create_buildconfig(buildconfig)
        else:
            self.trigger_build()
        latest_build_id = self.get_latest_build()
        status = self.get_status_build(self.APPLICATION_BUILD_NAME + '-' + latest_build_id)
        while status != 'completed':
            status = self.get_status_build(self.APPLICATION_BUILD_NAME + '-' + latest_build_id)
        if not self.get_job():
            job = self.job_template()
            self.create_job(job)
        else:
            job = self.job_template()
            self.update_job(job)


if __name__ == '__main__':
    tensorflow_build_trigger = Tensorflow_Build_Trigger()
    tensorflow_build_trigger.main()
