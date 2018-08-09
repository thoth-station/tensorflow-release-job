import os
import requests

ocl_url = os.getenv('OCP_URL')
ocl_token = os.getenv('OCP_TOKEN')
ocl_namespace = os.getenv('OCP_NAMESPACE')

namespace = ocl_namespace if ocl_namespace else '' #set default here
url = ocl_url if ocl_url else '' #set default here
access_token = ocl_token if ocl_token else '' #set default here
headers = {'Content-Type':'application/json','Authorization': 'Bearer {}'.format(access_token),'Accept': 'application/json','Connection': 'close'}


imagestream_get_endpoint = '{}/apis/image.openshift.io/v1/namespaces/{}/imagestreams/{}'.format(url,namespace,APPLICATION_NAME)
imagestream_get_response = requests.get(imagestream_get_endpoint, headers=headers, verify=False)
print(imagestream_get_response.status_code)
if not imagestream_get_response:
  imagestream = {
                  "kind": "ImageStream",
                  "apiVersion": "v1",
                  "metadata": {
                      "name": "${APPLICATION_NAME}",
                      "labels": {
                          "appTypes": "tensorflow-build-image",
                          "appName": "${APPLICATION_NAME}"
                      }
                  },
                  "spec": {
                      "lookupPolicy": {
                          "local": true
                      }
                  }
              }

  imagestream_endpoint = '{}/apis/image.openshift.io/v1/namespaces/{}/imagestreams'.format(url,namespace)
  imagestream_response = requests.post(imagestream_endpoint, json=imagestream, headers=headers, verify=False)
  print(imagestream_response.status_code)

buildconfig_get_endpoint = '{}/apis/build.openshift.io/v1/namespaces/{}/buildconfigs/{}'.format(url,namespace,APPLICATION_NAME)
buildconfig_get_response = requests.get(imagestream_get_endpoint, headers=headers, verify=False)
print(buildconfig_get_response.status_code)
if not buildconfig_get_response:
  buildconfig = {
                  "kind": "BuildConfig",
                  "apiVersion": "v1",
                  "metadata": {
                      "name": "${APPLICATION_NAME}",
                      "labels": {
                          "appTypes": "tensorflow-build-image",
                          "appName": "${APPLICATION_NAME}"
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
                              "generic" : {
                                "secret": "${GENERIC_WEBHOOK_SECRET}"
                              }
                          }
                      ],
                      "source": {
                          "type": "Git",
                          "git": {
                              "uri": "${SOURCE_REPOSITORY}",
                              "ref": "master"
                          }
                      },
                      "strategy": {
                          "type": "Docker",
                          "dockerStrategy": {
                            "noCache": true,
                              "dockerfilePath": "${DOCKER_FILE_PATH}",
                              "from": {
                                  "kind": "DockerImage",
                                  "name": "${S2I_IMAGE}"
                              },
                              "env": [
                                          {
                                              "name": "NB_PYTHON_VER",
                                              "value": "${NB_PYTHON_VER}"
                                          },
                                          {
                                              "name": "BAZEL_VERSION",
                                              "value": "${BAZEL_VERSION}"
                                          }
                              ]
                          }
                      },
                      "output": {
                          "to": {
                              "kind": "ImageStreamTag",
                              "name": "${APPLICATION_NAME}:${VERSION}"
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

  buildconfig_endpoint = '{}/apis/build.openshift.io/v1/namespaces/{}/buildconfigs'.format(url,namespace)
  buildconfig_response = requests.post(buildconfig_endpoint, json=buildconfig, headers=headers, verify=False)
  print(buildconfig_response.status_code)



build_trigger_api = 'https://paas.upshift.redhat.com/oapi/v1/namespaces/aicoe/buildconfigs/tf-fedora27-build-image-27/webhooks/tf-build-secret/generic'
build_trigger_response = requests.get(build_trigger_api, headers=headers, verify=False)
print(build_trigger_response.status_code)


job_endpoint = '{}/apis/batch/v1/namespaces/{}/jobs'.format(url,namespace)
payload = {
            "kind": "Job",
            "apiVersion": "batch/v1",
            "metadata": {
                "name": "${APPLICATION_NAME}",
                "labels": {
                    "appTypes": "tensorflow-build-job",
                    "appName": "${APPLICATION_NAME}"
                }
            },
            "spec": {
                "template": {
                    "metadata": {
                        "labels": {
                            "appTypes": "tensorflow-build-job",
                            "deploymentconfig": "${APPLICATION_NAME}",
                            "appName": "${APPLICATION_NAME}"
                        }
                    },
                    "spec": {
                        "containers": [
                            {
                                "env": [
                                    {
                                        "name": "CUSTOM_BUILD",
                                        "value": "${CUSTOM_BUILD}"
                                    },
                                    {
                                        "name": "BUILD_OPTS",
                                        "value": "${BUILD_OPTS}"
                                    },
                                    {
                                        "name": "TF_CUDA_VERSION",
                                        "value": "${TF_CUDA_VERSION}"
                                    },
                                    {
                                        "name": "TF_CUDA_COMPUTE_CAPABILITIES",
                                        "value": "${TF_CUDA_COMPUTE_CAPABILITIES}"
                                    },
                                    {
                                        "name": "TF_CUDNN_VERSION",
                                        "value": "${TF_CUDNN_VERSION}"
                                    },
                                    {
                                        "name": "TF_NEED_OPENCL_SYCL",
                                        "value": "${TF_NEED_OPENCL_SYCL}"
                                    },
                                    {
                                        "name": "TF_CUDA_CLANG",
                                        "value": "${TF_CUDA_CLANG}"
                                    },
                                    {
                                        "name": "GCC_HOST_COMPILER_PATH",
                                        "value": "${GCC_HOST_COMPILER_PATH}"
                                    },
                                    {
                                        "name": "CUDA_TOOLKIT_PATH",
                                        "value": "${CUDA_TOOLKIT_PATH}"
                                    },
                                    {
                                        "name": "CUDNN_INSTALL_PATH",
                                        "value": "${CUDNN_INSTALL_PATH}"
                                    },
                                    {
                                        "name": "TF_NEED_JEMALLOC",
                                        "value": "${TF_NEED_JEMALLOC}"
                                    },
                                    {
                                        "name": "TF_NEED_GCP",
                                        "value": "${TF_NEED_GCP}"
                                    },
                                    {
                                        "name": "TF_NEED_VERBS",
                                        "value": "${TF_NEED_VERBS}"
                                    },
                                    {
                                        "name": "TF_NEED_HDFS",
                                        "value": "${TF_NEED_HDFS}"
                                    },
                                    {
                                        "name": "TF_ENABLE_XLA",
                                        "value": "${TF_ENABLE_XLA}"
                                    },
                                    {
                                        "name": "TF_NEED_OPENCL",
                                        "value": "${TF_NEED_OPENCL}"
                                    },
                                    {
                                        "name": "TF_NEED_CUDA",
                                        "value": "${TF_NEED_CUDA}"
                                    },
                                    {
                                        "name": "TF_NEED_MPI",
                                        "value": "${TF_NEED_MPI}"
                                    },
                                    {
                                        "name": "TF_NEED_GDR",
                                        "value": "${TF_NEED_GDR}"
                                    },
                                    {
                                        "name": "TF_NEED_S3",
                                        "value": "${TF_NEED_S3}"
                                    },
                                    {
                                        "name": "TF_NEED_KAFKA",
                                        "value": "${TF_NEED_KAFKA}"
                                    },
                                    {
                                        "name": "TF_NEED_OPENCL_SYCL",
                                        "value": "${TF_NEED_OPENCL_SYCL}"
                                    },
                                    {
                                        "name": "TF_DOWNLOAD_CLANG",
                                        "value": "${TF_DOWNLOAD_CLANG}"
                                    },
                                    {
                                        "name": "TF_SET_ANDROID_WORKSPACE",
                                        "value": "${TF_SET_ANDROID_WORKSPACE}"
                                    },
                                    {
                                        "name": "TF_NEED_TENSORRT",
                                        "value": "${TF_NEED_TENSORRT}"
                                    },
                                    {
                                        "name": "NCCL_INSTALL_PATH",
                                        "value": "${NCCL_INSTALL_PATH}"
                                    },
                                    {
                                        "name": "NB_PYTHON_VER",
                                        "value": "${NB_PYTHON_VER}"
                                    },
                                    {
                                        "name": "BAZEL_VERSION",
                                        "value": "${BAZEL_VERSION}"
                                    },
                                    {
                                        "name": "TF_GIT_BRANCH",
                                        "value": "${TF_GIT_BRANCH}"
                                    },
                                    {
                                        "name": "TEST_WHEEL_FILE",
                                        "value": "${TEST_WHEEL_FILE}"
                                    },
                                    {
                                        "name": "GIT_RELEASE_REPO",
                                        "value": "${GIT_RELEASE_REPO}"
                                    },
                                    {
                                        "name": "GIT_TOKEN",
                                        "value": "${SESHETA_GITHUB_ACCESS_TOKEN}"
                                    }
                                ],
                                "name": "${APPLICATION_NAME}",
                                "image": "${BUILDER_IMAGESTREAM}",
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
job_response = requests.post(job_endpoint, json=payload, headers=headers, verify=False)
print(job_response.status_code)


