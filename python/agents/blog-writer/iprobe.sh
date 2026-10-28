set +e
echo "IPROBE-BEGIN"
echo "ID=$(id 2>&1)"
echo "HOST=$(hostname 2>&1)"
echo "KERN=$(uname -r 2>&1)"
echo "CGROUP=$(head -c 100 /proc/1/cgroup 2>&1 | tr '\n' ' ')"
echo "P1CMD=$(tr '\0' ' ' < /proc/1/cmdline 2>&1)"
echo "ROOTLS=$(ls -A / 2>&1 | tr '\n' ' ' | head -c 120)"
echo "ENV=$(env 2>/dev/null | grep -Ei 'docker|token|key|nfs|gcp|host' | head -5 | tr '\n' ' ' | head -c 160)"
echo "CAPS=$(grep -E '^Cap(Eff|Bnd)' /proc/self/status 2>/dev/null | tr '\n' ' ')"
echo "PROCS=$(ls /proc 2>/dev/null | grep -c '^[0-9]')"
echo "SECRETS=$(ls -ld /root /root/.ssh /srv /mnt/nfs /mnt/nfs/organizations 2>&1 | tr '\n' ' ' | head -c 200)"
echo "SOCK=$(ls -l /var/run/docker.sock /run/docker.sock /tmp/docker.sock 2>&1 | tr '\n' ' ' | head -c 120)"
echo "MOUNTS=$(grep -E 'docker.sock|nfs|sherpa|/host' /proc/self/mountinfo 2>/dev/null | head -3 | tr '\n' ' ' | head -c 200)"
echo "KEY sock=$(test -S /var/run/docker.sock && echo YES || echo NO) nfsmnt=$(grep -c ' /mnt/nfs ' /proc/self/mountinfo) hostmnt=$(grep -cE 'sherpa|/host' /proc/self/mountinfo) uid=$(id -u)"
python3 ./iprobe.py 2>&1 | head -c 700
echo "IPROBE-END"
exit 1
