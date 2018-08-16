# Tensorflow-trigger-job

A application for triggering new builds and jobs for tensorflow-build releases.

### Deploying the application on Openshift as a *Job* :
1. `oc new-build https://github.com/thoth-station/tensorflow-trigger-job.git --image-stream=python --name=tensorflow-trigger`
2. `oc set image-lookup tensorflow-trigger`
3. `oc create --filename openshift/job_template.yaml`
4. `oc new-app --template=tensorflow-trigger-job -p OCP_SECRET=<secret> -p BUILD_MAP="$(cat config.json)" -p SESHETA_GITHUB_ACCESS_TOKEN=<GITHUB_TOKEN>`

- The build map(config.json) contains the python version and os version for which tensorflow-build is to be triggered. 

##### Structure of config.json:

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

##### Check for the Resource Quota:

- The functionality of resource quota check while triggering builds and jobs is provided in the application. Required variables to set:

	To Set the name of the resource quota:</br>
	- `QUOTA_NAME = <resource_quota_name> (default: <namespace>-quota )`</br>
	
	To Disable the check for resource quota:</br>
	- `RESOURCE_QUOTA = 0 (default: 1)`</br>

	(Pass it as a parameter in Step 4 of Deployment)</br>
	
##### The OCP_SECRETS are the openshift variables:
- OCP_URL = <openshift_url | ex: https://paas.upshift.redhat.com >
- OCP_NAMESPACE =<openshift_namespace | ex: thoth-station>
- OCP_TOKEN = <openshift_token> <p>(Use Service account token for production | For Testing , Session Token can be used(As these have 24hr life))
</br> Store the above information in secret and pass it to the appliction as parameter(shown in step-4 of Deployment).</p>

##### Create *SECRET* in openshift:
```openshift
oc create secret generic <secret-name> --from-literal=OCP_URL= <OCP_URL> --from-literal=OCP_TOKEN=<OCP_TOKEN> --from-literal=OCP_NAMESPACE=<OCP_NAMESPACE>
```

 - All the tensorflow build related parameters can be passed to step-4 of Deployment as parameters.</br> (Default: fedora28 python36)

### Deploying the application on Openshift as a *Buildconfig, Deploymentconfig* (<span style="color:blue">Deprecated</span>)
- `oc new-app https://github.com/thoth-station/tensorflow-trigger-job.git --image-stream=python --name=tensorflow-trigger`
- `oc set env dc/tensorflow-trigger <varibales key:value>`
- `oc set env --from=secret/<secret> dc/tensorflow-trigger`

or 

- `oc create --filename openshift/buildconfig_template.yaml`
- `oc create --filename openshift/deploymentconfig_template.yaml`
- `oc new-app --template=tensorflow-trigger-buildconfig`
- `oc new-app --template=tensorflow-trigger-deployment -p OCP_SECRET=<secret> -p BUILD_MAP="$(cat config.json)" -p SESHETA_GITHUB_ACCESS_TOKEN=<GITHUB_TOKEN>`
