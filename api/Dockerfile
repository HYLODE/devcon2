# Use MCR image - comes prebuilt with non-root user
FROM mcr.microsoft.com/devcontainers/python:3.10

SHELL ["/bin/bash", "-o", "pipefail", "-e", "-u", "-x", "-c"]

# Update and install vim
RUN export DEBIAN_FRONTEND=noninteractive && \
    export ACCEPT_EULA=Y && \
    apt-get update && \
    apt-get install --yes --no-install-recommends vim

# Clean up after building.
RUN  apt-get autoremove && apt-get clean && rm -rf /var/lib/apt/lists/*

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Upgrade pip 
RUN python -m pip install --upgrade pip 
# Copy and install requirements
COPY requirements.txt /tmp/requirements.txt
RUN python -m pip install -r /tmp/requirements.txt 

COPY . .

CMD ["uvicorn", "backend:app", "--host", "0.0.0.0", "--port", "8301"]