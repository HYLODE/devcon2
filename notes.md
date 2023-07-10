## Log
Notes in reverse chronological order

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




