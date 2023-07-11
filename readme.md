# Demo dash app using devcontainers

[
    ![Open in Remote - Containers](
        https://img.shields.io/static/v1?label=Remote%20-%20Containers&message=Open&color=blue&logo=visualstudiocode
    )
](
    https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://github.com/hyui/devcon2
)

## Getting started

Assumes you have VScode installed with the [shell command `code` installed in your path](https://code.visualstudio.com/docs/setup/mac#_launching-from-the-command-line).

Open a terminal and enter the following commands

```bash
cd devcon2
cp .env.example .env
code .
```

Then from VSCode, [open](https://code.visualstudio.com/docs/devcontainers/containers#_quick-start-open-an-existing-folder-in-a-container) this directory in its devcontainer, navigate to the VSCode terminal, and enter the following.

```bash
python web/app.py
```
## Developing on your local machine

Again, this assumes that you're using VSCode and you wish to develop using 'devcontainers'. Since there is more than one service, then there are separate `.devcontainer.json` files and `Dockerfile`(s) for each service, and additional `compose.dev.yml` file that extends the core `compose.yml` file to work the VSCode.

You will need to start each service one at a time, and in a separate VSCode window. Since the focus here is on developing the frontend, then having opened the main project (defined by the location of the `.git` directory, and the `devcon2.code-workspace` file), you need to use the command palette (`F1` or `CMD-SHIFT-P`), and **Dev Containers: Open Folder in Container...** and then select the **web** folder.

This is slow the first time as it has to build the docker images, but less painful thereafter. It should then replace your previous VSCode window with one attached to _just_ the **web** folder but hosted from a docker container built from the same `Dockerfile` that will be used in deployment. Your development and deployment environments should therefore be identical.

Importantly

- the **api** service will be automatically started (as you'd expect from the `compose.yml` file)
- the actual **web** application (also specified in `compose.yml`) will **not** start, and you need to open a terminal in VSCode and run `./start` yourself. The ports are however mapped properly and you should be able to reach both endpoints on your local machine.
    - the FastAPI service is at http://localhost:8301
    - the Flask/Dash app is at http://localhost:8300
- both **web** and **api** services are started with a `./start` script kicking off a gunicorn and uvicorn server respectively, both in 'debug' mode with the 'reload' option.

Port configuration is set in the `.env` file, and picked up in the `compose.yml` file.

If you wish to develop the backend **api** (the FastAPI service in the `./api (the FastAPI service in the `./api`) (the FastAPI service in the `./api`) directory then you need a fresh VScode window, and repeat the above process but select the appropriate folder.

See the [VSCode documentation](https://code.visualstudio.com/remote/advancedcontainers/connect-multiple-containers) for more information.


## Deploying

You should be able to use docker compose as usual from the project root.

```bash
docker compose up -d --build 
```
And with logging to the terminal

```bash
docker compose up -d --build && docker compose logs -f
```

Press `CTRL-C` to exit (the logs), and `docker compose down` to stop the services.