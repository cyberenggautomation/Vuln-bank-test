# VULN-015 (Checkov CKV_DOCKER_7): using 'latest' tag, not pinned
FROM python:latest

# VULN-016 (Checkov CKV_DOCKER_3): no USER instruction — runs as root
WORKDIR /app

# VULN-017 (Checkov CKV_DOCKER_2): no HEALTHCHECK
COPY app/requirements.txt .

# VULN-018 (Checkov: ADD instead of COPY for local files — expands attack surface)
ADD app/ /app/

RUN pip install -r requirements.txt

# VULN-019 (Gitleaks/Checkov CKV_DOCKER_ENV_SECRET-style): secret baked into image layer
ENV API_SECRET_KEY="build-time-secret-do-not-commit-12345"

EXPOSE 5000

# VULN-020 (Checkov CKV_DOCKER_9): apt-get without --no-install-recommends / no cleanup
RUN apt-get update && apt-get install -y curl netcat

CMD ["python", "main.py"]
