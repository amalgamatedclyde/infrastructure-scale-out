# infrastructure-scale-out

### File info

- api.py: i added handlers to create enpoints for logging errors
- app.py: changed all CPU mode calls to GPU calls
- appspec.yml: this file is the CodeDeploy manifest and resides in the dir with application files
- locustfile.py: this is one of my load test files
- nets.py: i removed extraneous code and added handling of base64 image payloads for POST requests
- py-features-api.yml: this is the CloudFormation template
- restart_supervisor.sh: this is the shell script that restarts Supervisor after a CodeDeploy install event
- web.py: the tornado server. i added some enpoints and changed the the httpserver call
