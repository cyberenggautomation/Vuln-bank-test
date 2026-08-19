"""App config — deliberately leaky, for Gitleaks/secret-scan testing."""

# VULN-011 (Gitleaks: aws-access-token)
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

# VULN-012 (Gitleaks: generic-database-connection-string)
DATABASE_URL = "postgres://bankadmin:Sup3rS3cretPass!@prod-db.internal:5432/core_banking"

# VULN-013 (Gitleaks: stripe-access-token)
PAYMENT_GATEWAY_KEY = os.getenv("STRIPE_API_KEY")

# VULN-014 (Gitleaks: generic-api-key)
SMTP_PASSWORD = "n0tif y-svc-2024-prod-password"