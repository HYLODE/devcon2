## Log
Notes in reverse chronological order

### 2023-07-11 09:28:23 mwe with devcontainers and docker compose
open vscode
then follow the prompts to reopen in a devcontainer
this will automatically start the other services (e.g. api) and drop you into a session where you can edit the frontend; but you need to drop into the terminal to run the web service
and ensure you navigate to the workspace folder `/workspaces/devcon2/`

this is confusing b/c if you inspect docker `docker compose ps` then the port mapping appears to have been done but there is no app behind port 8300

```
cd /workspaces/devcon2
python app.py
```
now you can edit the flask app and b/c the debugger option is switched on in `./web/app.py` then you are both able to develop your app and use the provided backend

however to make this work I had to bin all the vscode devcontainer features which stopped the build b/c of issues installing python tools updating pip error externally managed environment
see https://pythonspeed.com/articles/externally-managed-environment-pep-668/

### 2023-07-10 23:10:59 mwe with fastapi and flask separately
now need to stitch together using docker compose
then convert to a devcontainer setup
will need to think about which service you wish to focus on developing
see also https://spin.atomicobject.com/2021/06/16/docker-development-container/

### 2023-07-10 21:28:48 now try to set-up with docker compose
just explored making edits to the dockerfile
since the `./devcontainer/Dockerfile` is expressly for developing then it may be best to think of this as a development Docker image. In which case, it seems reasonable for it not to have a `CMD` or `ENTRYPOINT` since you're never calling it to 'do' anything

### 2023-07-10 12:26:39 Failed attempt to swap to non-root users
Lots of issues with features in devcontainers.json not working
Currently works by using the `FROM mcr.microsoft.com/devcontainers/python:3.10` line which comes pre-built with a `vscode` user


### 2023-07-10 09:22:29 Setting up devcontainers 

#### MWE complete
Having installed the https://aka.ms/vscode-remote/download/containers extension
then use the "Open workspace in container" command
and you're environment including the terminal should be configured correctly
check this by running the hello world app in the vscode terminal, and then opening "localhost:8400" in your browser

```sh
python app.py
```

Note that you must not specify a python version in the feature

#### Now with a dash app

```bash
python hello_dash.py
```
I got an error message the first time but not the second time I ran this app.

```
Loading chunk 790 failed.
(error: http://localhost:8050/_dash-component-suites/dash/dash_table/async-highlight.js)
```




