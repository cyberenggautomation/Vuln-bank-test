"""App config — deliberately leaky, for Gitleaks/secret-scan testing."""

# VULN-011 (Gitleaks: aws-access-token)
AWS_ACCESS_KEY_ID = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_ACCESS_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"

# VULN-012 (Gitleaks: generic-database-connection-string)
DATABASE_URL = "postgres://bankadmin:Sup3rS3cretPass!@prod-db.internal:5432/core_banking"

# VULN-013 (Gitleaks: stripe-access-token)
PAYMENT_GATEWAY_KEY = "sk_live_4eC39HqLyjWDarjtT1zdp7dc"

# VULN-014 (Gitleaks: generic-api-key)
SMTP_PASSWORD = "n0tif y-svc-2024-prod-password"
