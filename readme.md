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
python hello_dash.py
```


