# Tensorflow-release-job
A application for triggering new builds and jobs for tensorflow-build releases.

## Build status
Build status of continus integration i.e. Quay. -

[![Docker Repository on Quay](https://quay.io/repository/aicoe/tensorflow-release-job/status)](https://quay.io/repository/aicoe/tensorflow-release-job)

## Deploying the application on Openshift as a *Job* :
```shell
$ oc create --filename openshift/job_template.yaml
$ oc new-app --template=tensorflow-release-job -p OCP_SECRET=<secret> -p BUILD_MAP="$(cat config.json)" -p SESHETA_GITHUB_ACCESS_TOKEN=<GITHUB_TOKEN>
```

- The build map [config.json](https://github.com/thoth-station/tensorflow-release-job/blob/master/config.json) contains the python version and os version for which tensorflow-build is to be triggered.

## How to use?
- Structure of config.json:

    - OS Version specific variables can be specified inside the os_version value with Upper Case Key variable(required).</br> Ex: "TF_NEED_HDFS": "{1|0}" 

		```json
		{
			"python_version": {
				"os_version": {
					"S2I_IMAGE": "os_registry",
					"BAZEL_VERSION": "bazel_version",
					"TF_NEED_CUDA": "{1|0}",
					"RESOURCE_LIMITS_CPU": "4",
					"RESOURCE_LIMITS_MEMORY": "8Gi"
				}
			}
		}
		```

- Check for the Resource Quota:

	- The functionality of resource quota check while triggering builds and jobs is provided in the application. Required variables to set:

		To Set the name of the resource quota:</br>
		- `QUOTA_NAME = <resource_quota_name> (default: <namespace>-quota )`</br>

		To Disable the check for resource quota:</br>
		- `RESOURCE_QUOTA = 0 (default: 1)`</br>

		(Pass it as a parameter in Step 2 of Deployment)</br>
	
- The OCP_SECRETS are the openshift variables:
	- OCP_URL = `<openshift_url | ex: https://paas.upshift.redhat.com>`
	- OCP_NAMESPACE =`<openshift_namespace | ex: thoth-station>`
	- OCP_TOKEN = `<openshift_token>` <p>(Use Service account token for production | For Testing , Session Token can be used(As these have 24hr life))
	</br> Store the above information in secret and pass it to the appliction as parameter(shown in step-2 of Deployment).</p>

- Create *SECRET* in openshift:
	```shell
		$ oc create secret --namespace "{{ OCP_NAMESPACE }}" generic {{OCP_SECRET}} \
	        --from-literal=OCP_URL="{{ OCP_URL }}" \
	        --from-literal=OCP_TOKEN="{{ OCP_TOKEN }}" \
	        --from-literal=OCP_NAMESPACE="{{ OCP_NAMESPACE }}" \
	        --type=opaque
	```

	- All the tensorflow build related parameters can be passed to step-2 of Deployment as parameters.</br> (Default: fedora28 python36)

## License
[GNU General Public License v3.0](https://github.com/thoth-station/tensorflow-release-job/blob/master/LICENSE)