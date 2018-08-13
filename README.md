# Tensorflow-trigger-job

A application for triggering new builds and jobs for tensorflow-build releases.

### Deploying the application on Openshift as a **Job** :
1. `oc new-build https://github.com/thoth-station/tensorflow-trigger-job.git --image-stream=python --name=tensorflow-trigger`
2. `oc set image-lookup tensorflow-trigger`
3. `oc create --filename openshift/job_template.yaml`
4. `oc new-app --template=tensorflow-trigger-job -p OCP_SECRET=<secret> -p BUILD_MAP="$(cat config.json)" -p SESHETA_GITHUB_ACCESS_TOKEN=<GITHUB_TOKEN>`

- The build map(config.json) contains the python version and os version for which tensorflow-build is to be triggered. 

##### Structure of config.json:
```json
{
	"python_version": {
		"os_version": "os_registry"
	}
}
```

#### The OCP_SECRETS are the openshift variables:
- OCP_URL = <openshift_url | ex: https://paas.upshift.redhat.com >
- OCP_NAMESPACE =<openshift_namespace | ex: thoth-station>
- OCP_TOKEN = <openshift_token> <p>(Use Service account token for production | For Testing , Session Token can be used(As these have 24hr life))
</br> Store the above information in secret and pass it to the appliction as parameter(shown in step-4).</p>

#### Create SECRET in openshift:
```openshift
oc create secret generic <secret-name> --from-literal=OCP_URL= <OCP_URL> --from-literal=OCP_TOKEN=<OCP_TOKEN> --from-literal=OCP_NAMESPACE=<OCP_NAMESPACE>
```

 - All the tensorflow build related parameters can be passed to step3 as parameters.(Default: fedora28 python36)

### Deploying the application on Openshift as a **Buildconfig,Deploymentconfig**
- `oc new-app https://github.com/thoth-station/tensorflow-trigger-job.git --image-stream=python --name=tensorflow-trigger`
- `oc set env {bc|dc}/tensorflow-trigger <varibales key:value>`
- `oc set env --from=secret/<secret> {bc|dc}/tensorflow-trigger`