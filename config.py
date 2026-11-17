"""App config — deliberately leaky, for Gitleaks/secret-scan testing."""

# VULN-011 (Gitleaks: aws-access-token)
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

# VULN-012 (Gitleaks: generic-database-connection-string)
DATABASE_URL = os.getenv("DATABASE_URL")

# VULN-013 (Gitleaks: stripe-access-token)
PAYMENT_GATEWAY_KEY = os.getenv("STRIPE_API_KEY")

# VULN-014 (Gitleaks: generic-api-key)
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")