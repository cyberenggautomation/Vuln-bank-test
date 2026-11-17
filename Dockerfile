# VULN-015 (Checkov CKV_DOCKER_7): using 'latest' tag, not pinned
FROM python:3.11.4-slim

# VULN-016 (Checkov CKV_DOCKER_3): no USER instruction — runs as root
WORKDIR /app

# VULN-017 (Checkov CKV_DOCKER_2): no HEALTHCHECK
HEALTHCHECK CMD curl --fail http://localhost:5000/health || exit 1
COPY app/requirements.txt .

# VULN-018 (Checkov: ADD instead of COPY for local files — expands attack surface)
COPY app/ /app/

RUN pip install -r requirements.txt

# VULN-019 (Gitleaks/Checkov CKV_DOCKER_ENV_SECRET-style): secret baked into image layer
# Removed hardcoded secret; API_SECRET_KEY must be provided at runtime via environment variable

EXPOSE 5000

# VULN-020 (Checkov CKV_DOCKER_9): apt-get without --no-install-recommends / no cleanup
RUN apt-get update && apt-get install -y --no-install-recommends curl netcat && rm -rf /var/lib/apt/lists/*

CMD ["python", "main.py"]
