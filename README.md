## What does this app do?

Checks for jobs run in any 002 project in the last 24g and sends notifications to Slack.  
If any jobs have failed in a project a message will be sent to egg-alerts, and those projects where all jobs completed successfully a message will be sent to egg-logs.

## What are typical use cases for this app?

Daily check to see if any issues are present.

## What data are required for this app to run?

This requires Hermes to be in ../hermes relative to dx_job_monitor. This will need the Hermes slack token file to be there too.  
The dnanexus_token file needs to be in the same folder as dx_job_monitor.py:

+-- hermes/  
|   &nbsp;&nbsp;&nbsp;&nbsp;+-- hermes.py  
+-- dx_job_monitor/  
|   &nbsp;&nbsp;&nbsp;&nbsp;+-- dx_job_monitor.py  
|   &nbsp;&nbsp;&nbsp;&nbsp;+-- hermes.log  
|   &nbsp;&nbsp;&nbsp;&nbsp;+-- dnanexus_token.py  

Running `python dx_job_monitor.py` will create a log in dx_job_monitor

## What does this app output?

A txt file called hermes.log logs all that is going on.  
Sends messages to egg-logs necessarily and egg-alerts if there are failed jobs.

### This was made by EMEE GLH
