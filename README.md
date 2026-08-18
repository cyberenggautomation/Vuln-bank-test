# VulnBank-Test

An intentionally vulnerable, banking-flavored fixture repo for validating the
Semgrep + Trivy + Checkov + Gitleaks → AI synthesis pipeline. Every planted
issue is cataloged in [`findings.yaml`](./findings.yaml) with the tool that
should catch it, so you can compute recall/precision instead of eyeballing
results.

**Do not deploy this app anywhere reachable.** It is a static test fixture,
same category as OWASP Juice Shop / DVWA — code exists to be *scanned*, not
run in production.

## What's in here

| Path | Purpose | Scanner |
|---|---|---|
| `app/main.py` | Flask API with SQLi, command injection, IDOR, weak hash, JWT issues | Semgrep + pure-agent |
| `app/config.py` | Hardcoded AWS/DB/payment secrets | Gitleaks |
| `app/requirements.txt` | Pinned to old vulnerable package versions | Trivy |
| `Dockerfile` | Root user, unpinned base, baked-in secret | Checkov + Gitleaks |
| `docker-compose.yml` | Privileged container, docker.sock mount, exposed DB | Checkov + Gitleaks |
| `k8s/deployment.yaml` | Privileged pod, hostNetwork, no resource limits | Checkov + Gitleaks |
| `terraform/main.tf` | Public S3, open security groups, unencrypted RDS | Checkov + Gitleaks |
| `.github/workflows/ci.yml` | `pull_request_target` + broad perms + hardcoded token | Checkov + Gitleaks |
| `findings.yaml` | Machine-readable answer key (50 planted findings) | — |

Two findings (`VULN-003` IDOR, `VULN-007` JWT-secret-chain) are marked
`pure-agent` in the answer key — they're intentionally undetectable by rule-based
tools and exist to validate your STRIDE/pure-agent pass, per the same
tool-vs-agent split you're already running downstream.

## Push this as a new repo

```bash
cd vulnbank-test
git init
git add .
git commit -m "Initial vulnerable fixture repo for scanner validation"
git branch -M main
git remote add origin https://github.com/<your-org>/vulnbank-test.git
git push -u origin main
```

Then point your n8n intake form / webhook at that repo URL exactly as you would
any other target.

## Running the app locally (optional, only if you want VULN-002/004/005/008/009
to be exercised at runtime rather than just statically scanned)

```bash
cd app
pip install -r requirements.txt
python init_db.py
python main.py
```

## Scoring your pipeline against this fixture

1. Run your full scan workflow against the pushed repo.
2. For each finding your pipeline reports, match it to a `VULN-###` in
   `findings.yaml` by file + category.
3. Recall per tool = (matched findings) / (total findings tagged with that
   tool in `findings.yaml`).
4. Anything your pipeline reports that has *no* match in `findings.yaml` is
   either a real false positive, or a legitimate finding you didn't know you
   planted (check `app/requirements.txt` — Trivy CVE counts will vary by scan
   date, that's expected and correct behavior, not noise).
5. `VULN-003` and `VULN-007` should NOT be caught by Semgrep/Checkov/Gitleaks —
   if your pure-agent/STRIDE pass catches them, that's the signal it's earning
   its cost over the deterministic tools alone.
