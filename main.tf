provider "aws" {
  region = "ap-south-1"

  # VULN-035 (Gitleaks/Checkov: hardcoded cloud credentials in IaC)
  access_key = "AKIAIOSFODNN7EXAMPLE"
  secret_key = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
}

resource "aws_s3_bucket" "statements" {
  bucket = "vulnbank-customer-statements"

  # VULN-036 (Checkov CKV_AWS_21): versioning not enabled
  # VULN-037 (Checkov CKV_AWS_18): access logging not enabled
  # VULN-038 (Checkov CKV_AWS_19): server-side encryption not configured
}

resource "aws_s3_bucket_public_access_block" "statements" {
  bucket = aws_s3_bucket.statements.id

  # VULN-039 (Checkov CKV_AWS_53/54/55/56): public access block explicitly disabled
  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

resource "aws_security_group" "bank_api" {
  name        = "bank-api-sg"
  description = "Security group for bank API"

  ingress {
    description = "VULN-040 (Checkov CKV_AWS_24/260): SSH open to the world"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "VULN-041 (Checkov CKV_AWS_260): unrestricted DB port"
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_db_instance" "core_banking" {
  identifier        = "core-banking-db"
  engine            = "postgres"
  instance_class    = "db.t3.medium"
  allocated_storage = 20

  # VULN-042 (Checkov CKV_AWS_16): storage not encrypted
  storage_encrypted = false

  # VULN-043 (Checkov CKV_AWS_17): publicly accessible RDS instance
  publicly_accessible = true

  # VULN-044 (Gitleaks: hardcoded DB master password)
  username = "bankadmin"
  password = "Sup3rS3cretPass!"

  # VULN-045 (Checkov CKV_AWS_293): deletion protection disabled
  deletion_protection = false

  # VULN-046 (Checkov CKV_AWS_133): backup retention set to 0
  backup_retention_period = 0
}
