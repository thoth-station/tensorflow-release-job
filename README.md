# Tensorflow-trigger-job
A job for triggering new builds and jobs for tensorflow-build releases

Deploying the job on Openshift:

- `oc new-build https://github.com/thoth-station/tensorflow-trigger-job.git --image=python --name=tensorflow-trigger`
- `oc create --filename openshift/job_template.yaml`
- `oc new-app --template=tensorflow-trigger-job -p OCP_SECRET=<secret>`
