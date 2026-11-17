provider "aws" {
  region = "ap-south-1"

  # VULN-035 (Gitleaks/Checkov: hardcoded cloud credentials in IaC)
  access_key = "AKIAIOSFODNN7EXAMPLE"
  secret_key = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
}

resource "aws_s3_bucket" "statements" {
  bucket = "vulnbank-customer-statements"

  versioning {
    enabled = true
  }

  logging {
    target_bucket = "some-logging-bucket"
    target_prefix = "vulnbank-customer-statements/"
  }

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }
}

resource "aws_s3_bucket_public_access_block" "statements" {
  bucket = aws_s3_bucket.statements.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
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
