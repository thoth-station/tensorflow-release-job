# Tensorflow-trigger-job
A applciation for triggering new builds and jobs for tensorflow-build releases

Deploying the application on Openshift as a **Job** :
-----------------------------------------------------
- `oc new-build https://github.com/thoth-station/tensorflow-trigger-job.git --image-stream=python --name=tensorflow-trigger`
- `oc create --filename openshift/job_template.yaml`
- `oc new-app --template=tensorflow-trigger-job -p OCP_SECRET=<secret>`

Deploying the application on Openshift as a **Buildconfig,Deploymentconfig**
----------------------------------------------------------------------------
- `oc new-app https://github.com/thoth-station/tensorflow-trigger-job.git --image-stream=python --name=tensorflow-trigger`
- `oc set env {bc|dc}/tensorflow-trigger <varibales key:value>`
- `oc set env --from=secret/<secret> {bc|dc}/tensorflow-trigger`