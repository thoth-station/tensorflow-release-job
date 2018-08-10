# Tensorflow-trigger-job
A applciation for triggering new builds and jobs for tensorflow-build releases

Deploying the application on Openshift as a **Job** :
-----------------------------------------------------
- `oc new-build https://github.com/thoth-station/tensorflow-trigger-job.git --image-stream=python --name=tensorflow-trigger`
- `oc create --filename openshift/job_template.yaml`
- `oc new-app --template=tensorflow-trigger-job -p OCP_SECRET=<secret>`

The OCP_SECRETS are the openshift variables:
- OCP_URL = <openshift_url|ex: https://paas.upshift.redhat.com >
- OCP_NAMESPACE =<openshift_namespace|ex: thoth-station>
- OCP_TOKEN = <openshift_token> (Use Service account token for production | For Testing , Session Token can be used(As these have 24hr life).)
store the above information in secret and pass it to the appliction as parameter(shown in step3).

All the tensorflow build related parameters can be passed to step3 as parameters.(Default: fedora28 python36)

Deploying the application on Openshift as a **Buildconfig,Deploymentconfig**
----------------------------------------------------------------------------
- `oc new-app https://github.com/thoth-station/tensorflow-trigger-job.git --image-stream=python --name=tensorflow-trigger`
- `oc set env {bc|dc}/tensorflow-trigger <varibales key:value>`
- `oc set env --from=secret/<secret> {bc|dc}/tensorflow-trigger`