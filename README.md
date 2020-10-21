## What does this app do?

Check if the 002 projects had jobs run and if any failed sending messages to egg-alerts if that is the case and egg-logs to inform the team of projects that had either no jobs run in the last 24h and no issues on jobs run in the last 24h.

## What are typical use cases for this app?

Daily check to see if any issues are present.

## What data are required for this app to run?

This requires Hermes in the following structure:

+-- hermes/  
|   &nbsp;&nbsp;&nbsp;&nbsp;+-- hermes.py  
+-- dx_job_monitor/  
|   &nbsp;&nbsp;&nbsp;&nbsp;+-- dx_job_monitor.py  
|   &nbsp;&nbsp;&nbsp;&nbsp;+-- hermes.log  

Running `python dx_job_monitor.py` will create a log in dx_job_monitor

## What does this app output?

A txt file called hermes.log logs all that is going on.

### This was made by EMEE GLH
