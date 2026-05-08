I have everything I need. Here is the full deployment plan.

---

# Deployment Plan

## Coding Agent Guidance

### Starting Claude Code

Always launch Claude Code from inside your HealthHelper project root. Every file reference and `CLAUDE.md` lookup depends on this being your working directory.

```shell
cd /path/to/healthhelper
claude
```

### Where Your Spec4 Files Live

Spec4 has created a `.spec4/` directory at the project root. Your 13 phase files are at:

```
.spec4/phases/phase1.json
.spec4/phases/phase2.json
...
.spec4/phases/phase13.json
```

### How to Reference Phase Files

Claude Code supports `@`-file syntax to inject file contents directly into your prompt context. To kick off any phase, use this pattern inside the interactive session:

```
Implement the requirements in @.spec4/phases/phase1.json.
Read the phase first, describe your implementation plan, then write the code.
```

Claude Code reads the JSON, pulls in any `CLAUDE.md` context from parent directories, and includes everything in the active context window. For phases that build on earlier work, reference both files:

```
Using the data models from @.spec4/phases/phase2.json as context,
implement @.spec4/phases/phase3.json.
```

You can also reference specific lines within a file using `@path/to/file.json#L10-40` if you need to direct Claude's attention to a particular section of a phase.

### Setting Up CLAUDE.md

Create a `CLAUDE.md` at your project root before starting Phase 1. This is the single biggest productivity lever in Claude Code — it persists your conventions across every session so Claude never has to re-learn them. Include:

- Your monorepo structure (frontend in `apps/mobile/`, backend in `apps/backend/`)
- TypeScript rules: strict mode, 2-space indent, single quotes, 100-char line length, PascalCase components, camelCase hooks/utilities
- Python rules: Ruff linter/formatter, mypy strict, 4-space indent, double quotes, 88-char line length, snake_case files
- A pointer to `.spec4/phases/` — e.g. `"Development phases are in .spec4/phases/phaseN.json"`
- Key architectural patterns: repository pattern on the backend, TanStack Query for server state, Zustand for client state, AI service layer abstracts online/offline routing

### Recommended Phase Workflow

1. **One phase per session.** Start a fresh Claude Code session for each phase. Run `/clear` between phases to prevent context bleed.
2. **Plan before code.** For every phase, prompt Claude to read the phase JSON and articulate its plan *before* writing any code. Use Claude Code's built-in plan mode for the more complex phases (Phase 4 WatermelonDB sync, Phase 10 llama.rn model download, Phase 12 FHIR R4).
3. **Run verification steps inline.** Each Spec4 phase includes verification criteria. After implementation, paste those criteria back and ask Claude to run the relevant tests/checks and confirm they pass.
4. **Commit after each phase.** Use `git commit` as your checkpoint. If a phase goes wrong, roll back cleanly.

### Agent-Specific Caveats for HealthHelper

- **`@`-file references are per-prompt, not persistent.** Referencing `@.spec4/phases/phase4.json` embeds that file in that prompt only. Re-reference it in follow-up messages if the conversation continues across multiple turns.
- **Context window pressure on large phases.** Phases 10 (llama.rn + resumable model download), 12 (FHIR R4), and 13 (Celery + i18n + PWA) involve large API surfaces. If Claude starts losing detail, use `/clear` and re-prime with just the relevant `@` file rather than letting the context grow stale.
- **Monorepo disambiguation.** With TypeScript frontend and Python backend in the same repo, be explicit in every prompt about which part of the codebase you're targeting — e.g. "In `apps/backend/`, implement the Alembic migration for Phase 2."
- **llama.rn native build complexity (Phase 10).** The `llama.rn` library requires native code compilation on iOS and Android. Claude Code can scaffold the JS/TS layer, but you'll need to run `npx expo prebuild` and verify the native build manually. Make this clear in your Phase 10 prompt.

---

## Target

- **Type:** Cloud
- **Provider:** AWS
- **Service:** ECS Fargate (API + Celery worker), RDS PostgreSQL 17, ElastiCache Redis 7, S3 + CloudFront (PWA)
- **Region:** us-east-1

---

## Containerisation

- **Enabled:** Yes
- **Base image:** `python:3.13-slim`
- **Registry:** AWS ECR
- **Services:**
  - `healthhelper-api` — FastAPI, runs `uvicorn`
  - `healthhelper-worker` — Celery worker, same image, different `CMD`
  - PWA frontend — static export, deployed to S3 + CloudFront (no container)

---

## CI/CD

- **Enabled:** Yes
- **Platform:** GitHub Actions
- **Trigger branch:** `main`
- **Authentication:** OIDC (no long-lived AWS credentials stored in GitHub)
- **Stages:**
  - Backend: `lint/typecheck` → `test` → `docker build & push to ECR` → `deploy to ECS (API)` → `deploy to ECS (Celery worker)`
  - Frontend: `lint/typecheck` → `expo export --platform web` → `sync to S3` → `CloudFront invalidation`

---

## Environment

**Required variables:**

- `DATABASE_URL` — PostgreSQL connection string (from RDS)
- `REDIS_URL` — ElastiCache Redis connection string
- `SECRET_KEY` — JWT signing secret
- `OPENAI_API_KEY` — OpenAI API key (never sent to client)
- `FHIR_SERVER_URL` — FHIR R4 server base URL
- `FHIR_CLIENT_ID` — SMART on FHIR client ID
- `FHIR_CLIENT_SECRET` — SMART on FHIR client secret
- `SENTRY_DSN_BACKEND` — Sentry DSN for FastAPI
- `SENTRY_DSN_FRONTEND` — Sentry DSN for Expo/React Native
- `ALLOWED_ORIGINS` — CORS allowed origins (ALB domain + CloudFront domain)
- `AWS_REGION` — us-east-1
- `ENVIRONMENT` — `production` | `staging` | `development`

**Secrets management:**
- **Production:** AWS Secrets Manager — secrets injected into ECS task definitions at container startup via IAM task execution role
- **Local development:** `.env` file at project root (never committed — add to `.gitignore`)

---

## Monitoring

- **Error tracking:** Sentry — `@sentry/react-native` on the Expo frontend; `sentry-sdk[fastapi]` on the backend
- **Infrastructure metrics:** AWS CloudWatch — automatically enabled for ECS Fargate (CPU, memory, task health), RDS, and ElastiCache
- **Uptime monitoring:** Better Stack — HTTP ping on your ALB endpoint every 60 seconds with alerting

---

## Deployment Steps

### 1. Install Prerequisites

Install the AWS CLI, Terraform, and the Expo CLI if not already present.

```shell
# AWS CLI v2
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip && sudo ./aws/install

# Terraform (via tfenv for version management)
brew install tfenv          # macOS
tfenv install 1.9.0
tfenv use 1.9.0

# Expo CLI
npm install -g expo-cli eas-cli

# Verify
aws --version
terraform --version
expo --version
```

### 2. Configure AWS CLI

```shell
aws configure
# Enter: AWS Access Key ID, Secret Access Key, region (us-east-1), output format (json)

# Verify
aws sts get-caller-identity
```

### 3. Create an ECR Repository

```shell
aws ecr create-repository \
  --repository-name healthhelper-backend \
  --region us-east-1

# Note the repositoryUri from the output — you'll need it in Terraform variables
```

### 4. Initialise and Apply Terraform

```shell
cd infrastructure/

# Initialise providers
terraform init

# Preview what will be created
terraform plan -var-file="production.tfvars"

# Provision all infrastructure (~10–15 minutes)
terraform apply -var-file="production.tfvars"

# Note the outputs: ALB DNS, CloudFront domain, RDS endpoint, ElastiCache endpoint
terraform output
```

### 5. Populate Secrets in AWS Secrets Manager

After Terraform creates the secret placeholders, populate the actual values:

```shell
aws secretsmanager put-secret-value \
  --secret-id healthhelper/production/database-url \
  --secret-string "postgresql+asyncpg://healthhelper:YOUR_PASSWORD@YOUR_RDS_ENDPOINT:5432/healthhelper" \
  --region us-east-1

aws secretsmanager put-secret-value \
  --secret-id healthhelper/production/redis-url \
  --secret-string "rediss://:YOUR_AUTH_TOKEN@YOUR_ELASTICACHE_ENDPOINT:6379/0" \
  --region us-east-1

aws secretsmanager put-secret-value \
  --secret-id healthhelper/production/secret-key \
  --secret-string "$(openssl rand -hex 32)" \
  --region us-east-1

aws secretsmanager put-secret-value \
  --secret-id healthhelper/production/openai-api-key \
  --secret-string "sk-..." \
  --region us-east-1

aws secretsmanager put-secret-value \
  --secret-id healthhelper/production/fhir-client-secret \
  --secret-string "YOUR_FHIR_CLIENT_SECRET" \
  --region us-east-1
```

### 6. Configure GitHub Actions OIDC

```shell
# Get your AWS account ID
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

# Create the OIDC identity provider for GitHub (one-time per AWS account)
aws iam create-open-id-connect-provider \
  --url https://token.actions.githubusercontent.com \
  --client-id-list sts.amazonaws.com \
  --thumbprint-list 6938fd4d98bab03faadb97b34396831e3780aea1

# The IAM role for GitHub Actions is created by Terraform (github_actions_role)
# Add these as GitHub Actions variables (not secrets) in your repo settings:
# AWS_ACCOUNT_ID = your 12-digit account ID
# CLOUDFRONT_DISTRIBUTION_ID = from terraform output
```

### 7. Run Database Migrations

After the API service is running on ECS, run Alembic migrations using a one-off ECS task:

```shell
# Get cluster and task definition names from Terraform output
CLUSTER=$(terraform output -raw ecs_cluster_name)
TASK_DEF=$(terraform output -raw api_task_definition_arn)
SUBNET=$(terraform output -raw private_subnet_ids | jq -r '.[0]')
SG=$(terraform output -raw api_security_group_id)

aws ecs run-task \
  --cluster $CLUSTER \
  --task-definition $TASK_DEF \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[$SUBNET],securityGroups=[$SG],assignPublicIp=DISABLED}" \
  --overrides '{"containerOverrides":[{"name":"healthhelper-api","command":["alembic","upgrade","head"]}]}' \
  --region us-east-1
```

### 8. Deploy the PWA Frontend (First Deploy)

The GitHub Actions workflow handles this on every push to `main`. For a manual first deploy:

```shell
cd apps/mobile/

# Install dependencies
npm install

# Build the PWA static export
npx expo export --platform web

# Sync to S3
S3_BUCKET=$(cd ../../infrastructure && terraform output -raw pwa_s3_bucket_name)
aws s3 sync dist/ s3://$S3_BUCKET --delete --cache-control "max-age=31536000"

# Invalidate CloudFront cache
CF_ID=$(cd ../../infrastructure && terraform output -raw cloudfront_distribution_id)
aws cloudfront create-invalidation --distribution-id $CF_ID --paths "/*"
```

### 9. Configure Sentry Projects

```shell
# Install Sentry CLI
npm install -g @sentry/cli

# Create two Sentry projects via the Sentry dashboard:
# 1. healthhelper-backend  (platform: Python/FastAPI)
# 2. healthhelper-frontend (platform: React Native / Expo)

# Add DSNs to Secrets Manager
aws secretsmanager put-secret-value \
  --secret-id healthhelper/production/sentry-dsn-backend \
  --secret-string "https://YOUR_KEY@oXXXXXX.ingest.sentry.io/XXXXXXX" \
  --region us-east-1

aws secretsmanager put-secret-value \
  --secret-id healthhelper/production/sentry-dsn-frontend \
  --secret-string "https://YOUR_KEY@oXXXXXX.ingest.sentry.io/XXXXXXX" \
  --region us-east-1
```

### 10. Configure Better Stack Uptime Monitor

1. Sign up at [betterstack.com](https://betterstack.com)
2. Create a new monitor: **HTTP** type
3. URL: `https://YOUR_ALB_DNS/health` (your FastAPI `/health` endpoint)
4. Check interval: 60 seconds
5. Add alert channels (email, Slack, PagerDuty, etc.)

---

## Configuration Files

### `Dockerfile`

Single Dockerfile for the FastAPI backend. Used for both the API service (`uvicorn`) and the Celery worker service (different `CMD` set in ECS task definition).

```dockerfile
# syntax=docker/dockerfile:1
FROM python:3.13-slim AS base

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Install system dependencies required for psycopg2, cryptography, etc.
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# ── Builder stage: install Python dependencies ──
FROM base AS builder

COPY apps/backend/requirements.txt .
RUN pip install --prefix=/install --no-cache-dir -r requirements.txt

# ── Runtime stage: lean final image ──
FROM base AS runtime

# Copy installed packages from builder
COPY --from=builder /install /usr/local

# Copy application code
COPY apps/backend/ .

# Create non-root user for security
RUN addgroup --system --gid 1001 appgroup && \
    adduser --system --uid 1001 --gid 1001 --no-create-home appuser
USER appuser

# Health check for ECS (hits FastAPI /health endpoint)
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

EXPOSE 8000

# Default command: FastAPI via uvicorn
# Celery worker overrides this CMD in the ECS task definition
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
```

### `.env.example`

Template for local development. Copy to `.env` and fill in values. Never commit `.env`.

```shell
# Database
DATABASE_URL=postgresql+asyncpg://healthhelper:password@localhost:5432/healthhelper

# Redis (local Docker)
REDIS_URL=redis://localhost:6379/0

# Auth
SECRET_KEY=local-dev-secret-key-change-in-production

# OpenAI
OPENAI_API_KEY=sk-...

# FHIR
FHIR_SERVER_URL=https://r4.smarthealthit.org
FHIR_CLIENT_ID=your-client-id
FHIR_CLIENT_SECRET=your-client-secret

# Sentry (optional for local dev)
SENTRY_DSN_BACKEND=
SENTRY_DSN_FRONTEND=

# CORS
ALLOWED_ORIGINS=http://localhost:8081,http://localhost:19006

# App
ENVIRONMENT=development
AWS_REGION=us-east-1
```

### `.github/workflows/deploy.yml`

Full CI/CD pipeline. Two jobs run in parallel: backend (ECS) and frontend (S3 + CloudFront). Both use OIDC — no stored AWS credentials.

```yaml
name: Deploy HealthHelper

on:
  push:
    branches: [main]

permissions:
  id-token: write
  contents: read

env:
  AWS_REGION: us-east-1
  ECR_REPOSITORY: healthhelper-backend
  ECS_CLUSTER: healthhelper-production
  API_SERVICE: healthhelper-api
  WORKER_SERVICE: healthhelper-worker
  API_TASK_DEFINITION: healthhelper-api
  WORKER_TASK_DEFINITION: healthhelper-worker
  CONTAINER_NAME: healthhelper-api

jobs:
  # ── Backend: lint, test, build, push to ECR, deploy to ECS ──
  backend:
    name: Backend — Test & Deploy
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: apps/backend

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.13"
          cache: "pip"

      - name: Install dependencies
        run: pip install -r requirements.txt -r requirements-dev.txt

      - name: Lint & type-check
        run: |
          ruff check .
          ruff format --check .
          mypy .

      - name: Run tests
        run: pytest --cov=app --cov-report=xml -q
        env:
          DATABASE_URL: postgresql+asyncpg://test:test@localhost:5432/test
          REDIS_URL: redis://localhost:6379/0
          SECRET_KEY: test-secret-key
          ENVIRONMENT: test

      - name: Configure AWS credentials (OIDC)
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::${{ vars.AWS_ACCOUNT_ID }}:role/healthhelper-github-actions-role
          aws-region: ${{ env.AWS_REGION }}

      - name: Login to Amazon ECR
        id: login-ecr
        uses: aws-actions/amazon-ecr-login@v2

      - name: Build, tag & push image to ECR
        id: build-image
        env:
          ECR_REGISTRY: ${{ steps.login-ecr.outputs.registry }}
          IMAGE_TAG: ${{ github.sha }}
        run: |
          docker build \
            -f ../../Dockerfile \
            -t $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG \
            -t $ECR_REGISTRY/$ECR_REPOSITORY:latest \
            ../../
          docker push $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG
          docker push $ECR_REGISTRY/$ECR_REPOSITORY:latest
          echo "image=$ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG" >> $GITHUB_OUTPUT

      - name: Download API task definition
        run: |
          aws ecs describe-task-definition \
            --task-definition ${{ env.API_TASK_DEFINITION }} \
            --query taskDefinition \
            > /tmp/api-task-definition.json

      - name: Update API task definition with new image
        id: api-task-def
        uses: aws-actions/amazon-ecs-render-task-definition@v1
        with:
          task-definition: /tmp/api-task-definition.json
          container-name: ${{ env.CONTAINER_NAME }}
          image: ${{ steps.build-image.outputs.image }}

      - name: Deploy API service to ECS
        uses: aws-actions/amazon-ecs-deploy-task-definition@v2
        with:
          task-definition: ${{ steps.api-task-def.outputs.task-definition }}
          service: ${{ env.API_SERVICE }}
          cluster: ${{ env.ECS_CLUSTER }}
          wait-for-service-stability: true

      - name: Download Celery worker task definition
        run: |
          aws ecs describe-task-definition \
            --task-definition ${{ env.WORKER_TASK_DEFINITION }} \
            --query taskDefinition \
            > /tmp/worker-task-definition.json

      - name: Update worker task definition with new image
        id: worker-task-def
        uses: aws-actions/amazon-ecs-render-task-definition@v1
        with:
          task-definition: /tmp/worker-task-definition.json
          container-name: healthhelper-worker
          image: ${{ steps.build-image.outputs.image }}

      - name: Deploy Celery worker service to ECS
        uses: aws-actions/amazon-ecs-deploy-task-definition@v2
        with:
          task-definition: ${{ steps.worker-task-def.outputs.task-definition }}
          service: ${{ env.WORKER_SERVICE }}
          cluster: ${{ env.ECS_CLUSTER }}
          wait-for-service-stability: true

  # ── Frontend: lint, build PWA, deploy to S3 + CloudFront ──
  frontend:
    name: Frontend — Build & Deploy PWA
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: apps/mobile

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Set up Node.js
        uses: actions/setup-node@v4
        with:
          node-version: "20"
          cache: "npm"
          cache-dependency-path: apps/mobile/package-lock.json

      - name: Install dependencies
        run: npm ci

      - name: Lint & type-check
        run: |
          npx eslint . --max-warnings 0
          npx tsc --noEmit

      - name: Export PWA
        run: npx expo export --platform web
        env:
          EXPO_PUBLIC_API_URL: https://${{ vars.ALB_DNS_NAME }}
          EXPO_PUBLIC_SENTRY_DSN: ${{ vars.SENTRY_DSN_FRONTEND }}
          EXPO_PUBLIC_ENVIRONMENT: production

      - name: Configure AWS credentials (OIDC)
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::${{ vars.AWS_ACCOUNT_ID }}:role/healthhelper-github-actions-role
          aws-region: ${{ env.AWS_REGION }}

      - name: Sync PWA to S3
        run: |
          aws s3 sync dist/ s3://${{ vars.PWA_S3_BUCKET }} \
            --delete \
            --cache-control "max-age=31536000,public,immutable" \
            --exclude "index.html" \
            --exclude "*.json"
          # Short cache for HTML and manifests so updates propagate quickly
          aws s3 sync dist/ s3://${{ vars.PWA_S3_BUCKET }} \
            --exclude "*" \
            --include "index.html" \
            --include "*.json" \
            --cache-control "max-age=0,no-cache,no-store,must-revalidate"

      - name: Invalidate CloudFront cache
        run: |
          aws cloudfront create-invalidation \
            --distribution-id ${{ vars.CLOUDFRONT_DISTRIBUTION_ID }} \
            --paths "/*"
```

---

## Terraform

### `main.tf`

```hcl
terraform {
  required_version = ">= 1.9.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.44"
    }
  }

  # Uncomment after creating the S3 backend bucket manually:
  # backend "s3" {
  #   bucket = "healthhelper-terraform-state"
  #   key    = "production/terraform.tfstate"
  #   region = "us-east-1"
  #   encrypt = true
  # }
}

provider "aws" {
  region = var.aws_region
}

# ── Data sources ──────────────────────────────────────────────
data "aws_caller_identity" "current" {}
data "aws_availability_zones" "available" { state = "available" }

# ── VPC ───────────────────────────────────────────────────────
resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true
  tags = { Name = "${var.app_name}-vpc" }
}

resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id
  tags   = { Name = "${var.app_name}-igw" }
}

# Public subnets (ALB, NAT gateways)
resource "aws_subnet" "public" {
  count                   = 2
  vpc_id                  = aws_vpc.main.id
  cidr_block              = cidrsubnet("10.0.0.0/16", 8, count.index)
  availability_zone       = data.aws_availability_zones.available.names[count.index]
  map_public_ip_on_launch = true
  tags                    = { Name = "${var.app_name}-public-${count.index + 1}" }
}

# Private subnets (ECS tasks, RDS, ElastiCache)
resource "aws_subnet" "private" {
  count             = 2
  vpc_id            = aws_vpc.main.id
  cidr_block        = cidrsubnet("10.0.0.0/16", 8, count.index + 10)
  availability_zone = data.aws_availability_zones.available.names[count.index]
  tags              = { Name = "${var.app_name}-private-${count.index + 1}" }
}

# NAT Gateway (for private subnet outbound internet — e.g. OpenAI API calls)
resource "aws_eip" "nat" {
  domain = "vpc"
  tags   = { Name = "${var.app_name}-nat-eip" }
}

resource "aws_nat_gateway" "main" {
  allocation_id = aws_eip.nat.id
  subnet_id     = aws_subnet.public[0].id
  tags          = { Name = "${var.app_name}-nat" }
  depends_on    = [aws_internet_gateway.main]
}

# Route tables
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }
  tags = { Name = "${var.app_name}-public-rt" }
}

resource "aws_route_table_association" "public" {
  count          = 2
  subnet_id      = aws_subnet.public[count.index].id
  route_table_id = aws_route_table.public.id
}

resource "aws_route_table" "private" {
  vpc_id = aws_vpc.main.id
  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.main.id
  }
  tags = { Name = "${var.app_name}-private-rt" }
}

resource "aws_route_table_association" "private" {
  count          = 2
  subnet_id      = aws_subnet.private[count.index].id
  route_table_id = aws_route_table.private.id
}

# ── Security Groups ───────────────────────────────────────────
resource "aws_security_group" "alb" {
  name        = "${var.app_name}-alb-sg"
  description = "Allow HTTPS inbound to ALB"
  vpc_id      = aws_vpc.main.id

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  tags = { Name = "${var.app_name}-alb-sg" }
}

resource "aws_security_group" "ecs" {
  name        = "${var.app_name}-ecs-sg"
  description = "ECS tasks — allow traffic from ALB only"
  vpc_id      = aws_vpc.main.id

  ingress {
    from_port       = 8000
    to_port         = 8000
    protocol        = "tcp"
    security_groups = [aws_security_group.alb.id]
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  tags = { Name = "${var.app_name}-ecs-sg" }
}

resource "aws_security_group" "rds" {
  name        = "${var.app_name}-rds-sg"
  description = "PostgreSQL — allow from ECS only"
  vpc_id      = aws_vpc.main.id

  ingress {
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.ecs.id]
  }
  tags = { Name = "${var.app_name}-rds-sg" }
}

resource "aws_security_group" "redis" {
  name        = "${var.app_name}-redis-sg"
  description = "Redis — allow from ECS only"
  vpc_id      = aws_vpc.main.id

  ingress {
    from_port       = 6379
    to_port         = 6379
    protocol        = "tcp"
    security_groups = [aws_security_group.ecs.id]
  }
  tags = { Name = "${var.app_name}-redis-sg" }
}

# ── ECR Repository ────────────────────────────────────────────
resource "aws_ecr_repository" "backend" {
  name                 = "${var.app_name}-backend"
  image_tag_mutability = "MUTABLE"
  force_delete         = false

  image_scanning_configuration {
    scan_on_push = true
  }

  tags = { Name = "${var.app_name}-ecr" }
}

resource "aws_ecr_lifecycle_policy" "backend" {
  repository = aws_ecr_repository.backend.name
  policy = jsonencode({
    rules = [{
      rulePriority = 1
      description  = "Keep last 10 images"
      selection = {
        tagStatus   = "any"
        countType   = "imageCountMoreThan"
        countNumber = 10
      }
      action = { type = "expire" }
    }]
  })
}

# ── RDS PostgreSQL 17 ─────────────────────────────────────────
resource "aws_db_subnet_group" "main" {
  name       = "${var.app_name}-db-subnet-group"
  subnet_ids = aws_subnet.private[*].id
  tags       = { Name = "${var.app_name}-db-subnet-group" }
}

resource "aws_db_parameter_group" "postgres17" {
  name   = "${var.app_name}-postgres17"
  family = "postgres17"

  parameter {
    name  = "shared_buffers"
    value = "{DBInstanceClassMemory/4}"
  }
  parameter {
    name  = "log_connections"
    value = "1"
  }

  tags = { Name = "${var.app_name}-postgres17-params" }
}

resource "aws_db_instance" "main" {
  identifier              = "${var.app_name}-postgres"
  engine                  = "postgres"
  engine_version          = "17"
  instance_class          = var.db_instance_class
  allocated_storage       = 20
  max_allocated_storage   = 100
  storage_type            = "gp3"
  storage_encrypted       = true
  db_name                 = "healthhelper"
  username                = "healthhelper"
  password                = var.db_password
  parameter_group_name    = aws_db_parameter_group.postgres17.name
  db_subnet_group_name    = aws_db_subnet_group.main.name
  vpc_security_group_ids  = [aws_security_group.rds.id]
  publicly_accessible     = false
  skip_final_snapshot     = false
  final_snapshot_identifier = "${var.app_name}-final-snapshot"
  backup_retention_period = 7
  backup_window           = "03:00-04:00"
  maintenance_window      = "sun:04:00-sun:05:00"
  deletion_protection     = true
  multi_az                = var.enable_multi_az

  tags = { Name = "${var.app_name}-rds" }
}

# ── ElastiCache Redis 7 ───────────────────────────────────────
resource "aws_elasticache_subnet_group" "main" {
  name       = "${var.app_name}-redis-subnet-group"
  subnet_ids = aws_subnet.private[*].id
  tags       = { Name = "${var.app_name}-redis-subnet-group" }
}

resource "aws_elasticache_replication_group" "redis" {
  replication_group_id       = "${var.app_name}-redis"
  description                = "Redis for Celery broker and result backend"
  node_type                  = var.redis_node_type
  num_cache_clusters         = 1
  automatic_failover_enabled = false
  at_rest_encryption_enabled = true
  transit_encryption_enabled = true
  auth_token                 = var.redis_auth_token
  engine_version             = "7.1"
  port                       = 6379
  subnet_group_name          = aws_elasticache_subnet_group.main.name
  security_group_ids         = [aws_security_group.redis.id]

  log_delivery_configuration {
    destination      = aws_cloudwatch_log_group.redis_slow_log.name
    destination_type = "cloudwatch-logs"
    log_format       = "text"
    log_type         = "slow-log"
  }

  tags = { Name = "${var.app_name}-redis" }
}

resource "aws_cloudwatch_log_group" "redis_slow_log" {
  name              = "/aws/elasticache/${var.app_name}/slow-log"
  retention_in_days = 30
}

# ── Application Load Balancer ─────────────────────────────────
resource "aws_lb" "main" {
  name               = "${var.app_name}-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb.id]
  subnets            = aws_subnet.public[*].id

  enable_deletion_protection = true
  tags                       = { Name = "${var.app_name}-alb" }
}

resource "aws_lb_target_group" "api" {
  name        = "${var.app_name}-api-tg"
  port        = 8000
  protocol    = "HTTP"
  vpc_id      = aws_vpc.main.id
  target_type = "ip"

  health_check {
    enabled             = true
    path                = "/health"
    protocol            = "HTTP"
    matcher             = "200"
    interval            = 30
    timeout             = 10
    healthy_threshold   = 2
    unhealthy_threshold = 3
  }

  tags = { Name = "${var.app_name}-api-tg" }
}

resource "aws_lb_listener" "http_redirect" {
  load_balancer_arn = aws_lb.main.arn
  port              = 80
  protocol          = "HTTP"

  default_action {
    type = "redirect"
    redirect {
      port        = "443"
      protocol    = "HTTPS"
      status_code = "HTTP_301"
    }
  }
}

resource "aws_lb_listener" "https" {
  load_balancer_arn = aws_lb.main.arn
  port              = 443
  protocol          = "HTTPS"
  ssl_policy        = "ELBSecurityPolicy-TLS13-1-2-2021-06"
  certificate_arn   = var.acm_certificate_arn

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.api.arn
  }
}

# ── ECS Cluster ───────────────────────────────────────────────
resource "aws_ecs_cluster" "main" {
  name = "${var.app_name}-production"

  setting {
    name  = "containerInsights"
    value = "enabled"
  }

  tags = { Name = "${var.app_name}-ecs-cluster" }
}

resource "aws_cloudwatch_log_group" "ecs_api" {
  name              = "/ecs/${var.app_name}/api"
  retention_in_days = 30
}

resource "aws_cloudwatch_log_group" "ecs_worker" {
  name              = "/ecs/${var.app_name}/worker"
  retention_in_days = 30
}

# ── IAM: ECS Task Execution Role ──────────────────────────────
resource "aws_iam_role" "ecs_task_execution" {
  name = "${var.app_name}-ecs-task-execution-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action    = "sts:AssumeRole"
      Effect    = "Allow"
      Principal = { Service = "ecs-tasks.amazonaws.com" }
    }]
  })
}

resource "aws_iam_role_policy_attachment" "ecs_task_execution" {
  role       = aws_iam_role.ecs_task_execution.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

resource "aws_iam_role_policy" "ecs_secrets" {
  name = "${var.app_name}-ecs-secrets-policy"
  role = aws_iam_role.ecs_task_execution.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Action = [
        "secretsmanager:GetSecretValue",
        "secretsmanager:DescribeSecret"
      ]
      Resource = "arn:aws:secretsmanager:${var.aws_region}:${data.aws_caller_identity.current.account_id}:secret:${var.app_name}/*"
    }]
  })
}

# ── IAM: ECS Task Role (runtime permissions) ──────────────────
resource "aws_iam_role" "ecs_task" {
  name = "${var.app_name}-ecs-task-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action    = "sts:AssumeRole"
      Effect    = "Allow"
      Principal = { Service = "ecs-tasks.amazonaws.com" }
    }]
  })
}

# ── IAM: GitHub Actions OIDC Role ────────────────────────────
resource "aws_iam_openid_connect_provider" "github" {
  url             = "https://token.actions.githubusercontent.com"
  client_id_list  = ["sts.amazonaws.com"]
  thumbprint_list = ["6938fd4d98bab03faadb97b34396831e3780aea1"]
}

resource "aws_iam_role" "github_actions" {
  name = "${var.app_name}-github-actions-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = {
        Federated = aws_iam_openid_connect_provider.github.arn
      }
      Action = "sts:AssumeRoleWithWebIdentity"
      Condition = {
        StringLike = {
          "token.actions.githubusercontent.com:sub" = "repo:${var.github_org}/${var.github_repo}:*"
        }
        StringEquals = {
          "token.actions.githubusercontent.com:aud" = "sts.amazonaws.com"
        }
      }
    }]
  })
}

resource "aws_iam_role_policy" "github_actions" {
  name = "${var.app_name}-github-actions-policy"
  role = aws_iam_role.github_actions.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "ecr:GetAuthorizationToken",
          "ecr:BatchCheckLayerAvailability",
          "ecr:GetDownloadUrlForLayer",
          "ecr:BatchGetImage",
          "ecr:PutImage",
          "ecr:InitiateLayerUpload",
          "ecr:UploadLayerPart",
          "ecr:CompleteLayerUpload"
        ]
        Resource = "*"
      },
      {
        Effect = "Allow"
        Action = [
          "ecs:DescribeTaskDefinition",
          "ecs:RegisterTaskDefinition",
          "ecs:UpdateService",
          "ecs:DescribeServices"
        ]
        Resource = "*"
      },
      {
        Effect   = "Allow"
        Action   = ["iam:PassRole"]
        Resource = [
          aws_iam_role.ecs_task_execution.arn,
          aws_iam_role.ecs_task.arn
        ]
      },
      {
        Effect = "Allow"
        Action = [
          "s3:PutObject",
          "s3:GetObject",
          "s3:DeleteObject",
          "s3:ListBucket"
        ]
        Resource = [
          aws_s3_bucket.pwa.arn,
          "${aws_s3_bucket.pwa.arn}/*"
        ]
      },
      {
        Effect   = "Allow"
        Action   = ["cloudfront:CreateInvalidation"]
        Resource = aws_cloudfront_distribution.pwa.arn
      }
    ]
  })
}

# ── ECS Task Definitions ──────────────────────────────────────
resource "aws_ecs_task_definition" "api" {
  family                   = "${var.app_name}-api"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = var.api_cpu
  memory                   = var.api_memory
  execution_role_arn       = aws_iam_role.ecs_task_execution.arn
  task_role_arn            = aws_iam_role.ecs_task.arn

  container_definitions = jsonencode([{
    name  = "${var.app_name}-api"
    image = "${aws_ecr_repository.backend.repository_url}:latest"

    portMappings = [{
      containerPort = 8000
      protocol      = "tcp"
    }]

    secrets = [
      { name = "DATABASE_URL",        valueFrom = aws_secretsmanager_secret.database_url.arn },
      { name = "REDIS_URL",           valueFrom = aws_secretsmanager_secret.redis_url.arn },
      { name = "SECRET_KEY",          valueFrom = aws_secretsmanager_secret.secret_key.arn },
      { name = "OPENAI_API_KEY",      valueFrom = aws_secretsmanager_secret.openai_api_key.arn },
      { name = "FHIR_CLIENT_SECRET",  valueFrom = aws_secretsmanager_secret.fhir_client_secret.arn },
      { name = "SENTRY_DSN_BACKEND",  valueFrom = aws_secretsmanager_secret.sentry_dsn_backend.arn }
    ]

    environment = [
      { name = "ENVIRONMENT",      value = "production" },
      { name = "AWS_REGION",       value = var.aws_region },
      { name = "FHIR_SERVER_URL",  value = var.fhir_server_url },
      { name = "FHIR_CLIENT_ID",   value = var.fhir_client_id },
      { name = "ALLOWED_ORIGINS",  value = "https://${aws_cloudfront_distribution.pwa.domain_name}" }
    ]

    logConfiguration = {
      logDriver = "awslogs"
      options = {
        "awslogs-group"         = aws_cloudwatch_log_group.ecs_api.name
        "awslogs-region"        = var.aws_region
        "awslogs-stream-prefix" = "api"
      }
    }

    healthCheck = {
      command     = ["CMD-SHELL", "curl -f http://localhost:8000/health || exit 1"]
      interval    = 30
      timeout     = 10
      retries     = 3
      startPeriod = 40
    }
  }])
}

resource "aws_ecs_task_definition" "worker" {
  family                   = "${var.app_name}-worker"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = var.worker_cpu
  memory                   = var.worker_memory
  execution_role_arn       = aws_iam_role.ecs_task_execution.arn
  task_role_arn            = aws_iam_role.ecs_task.arn

  container_definitions = jsonencode([{
    name    = "${var.app_name}-worker"
    image   = "${aws_ecr_repository.backend.repository_url}:latest"
    command = ["celery", "-A", "app.worker", "worker", "--loglevel=info", "--concurrency=4"]

    secrets = [
      { name = "DATABASE_URL",       valueFrom = aws_secretsmanager_secret.database_url.arn },
      { name = "REDIS_URL",          valueFrom = aws_secretsmanager_secret.redis_url.arn },
      { name = "SECRET_KEY",         valueFrom = aws_secretsmanager_secret.secret_key.arn },
      { name = "OPENAI_API_KEY",     valueFrom = aws_secretsmanager_secret.openai_api_key.arn },
      { name = "SENTRY_DSN_BACKEND", valueFrom = aws_secretsmanager_secret.sentry_dsn_backend.arn }
    ]

    environment = [
      { name = "ENVIRONMENT", value = "production" },
      { name = "AWS_REGION",  value = var.aws_region }
    ]

    logConfiguration = {
      logDriver = "awslogs"
      options = {
        "awslogs-group"         = aws_cloudwatch_log_group.ecs_worker.name
        "awslogs-region"        = var.aws_region
        "awslogs-stream-prefix" = "worker"
      }
    }
  }])
}

# ── ECS Services ──────────────────────────────────────────────
resource "aws_ecs_service" "api" {
  name            = "${var.app_name}-api"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.api.arn
  desired_count   = var.api_desired_count
  launch_type     = "FARGATE"

  network_configuration {
    subnets          = aws_subnet.private[*].id
    security_groups  = [aws_security_group.ecs.id]
    assign_public_ip = false
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.api.arn
    container_name   = "${var.app_name}-api"
    container_port   = 8000
  }

  depends_on = [aws_lb_listener.https]

  lifecycle {
    ignore_changes = [task_definition, desired_count]
  }
}

resource "aws_ecs_service" "worker" {
  name            = "${var.app_name}-worker"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.worker.arn
  desired_count   = var.worker_desired_count
  launch_type     = "FARGATE"

  network_configuration {
    subnets          = aws_subnet.private[*].id
    security_groups  = [aws_security_group.ecs.id]
    assign_public_ip = false
  }

  lifecycle {
    ignore_changes = [task_definition, desired_count]
  }
}

# ── AWS Secrets Manager ───────────────────────────────────────
locals {
  secrets = {
    "database-url"       = "healthhelper/${var.environment}/database-url"
    "redis-url"          = "healthhelper/${var.environment}/redis-url"
    "secret-key"         = "healthhelper/${var.environment}/secret-key"
    "openai-api-key"     = "healthhelper/${var.environment}/openai-api-key"
    "fhir-client-secret" = "healthhelper/${var.environment}/fhir-client-secret"
    "sentry-dsn-backend" = "healthhelper/${var.environment}/sentry-dsn-backend"
  }
}

resource "aws_secretsmanager_secret" "database_url" {
  name                    = local.secrets["database-url"]
  recovery_window_in_days = 7
}

resource "aws_secretsmanager_secret" "redis_url" {
  name                    = local.secrets["redis-url"]
  recovery_window_in_days = 7
}

resource "aws_secretsmanager_secret" "secret_key" {
  name                    = local.secrets["secret-key"]
  recovery_window_in_days = 7
}

resource "aws_secretsmanager_secret" "openai_api_key" {
  name                    = local.secrets["openai-api-key"]
  recovery_window_in_days = 7
}

resource "aws_secretsmanager_secret" "fhir_client_secret" {
  name                    = local.secrets["fhir-client-secret"]
  recovery_window_in_days = 7
}

resource "aws_secretsmanager_secret" "sentry_dsn_backend" {
  name                    = local.secrets["sentry-dsn-backend"]
  recovery_window_in_days = 7
}

# ── S3 + CloudFront (PWA) ─────────────────────────────────────
resource "aws_s3_bucket" "pwa" {
  bucket = "${var.app_name}-pwa-${data.aws_caller_identity.current.account_id}"
  tags   = { Name = "${var.app_name}-pwa" }
}

resource "aws_s3_bucket_public_access_block" "pwa" {
  bucket                  = aws_s3_bucket.pwa.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_cloudfront_origin_access_control" "pwa" {
  name                              = "${var.app_name}-pwa-oac"
  description                       = "OAC for HealthHelper PWA S3 bucket"
  origin_access_control_origin_type = "s3"
  signing_behavior                  = "always"
  signing_protocol                  = "sigv4"
}

resource "aws_cloudfront_distribution" "pwa" {
  enabled             = true
  is_ipv6_enabled     = true
  default_root_object = "index.html"
  price_class         = "PriceClass_100"

  origin {
    domain_name              = aws_s3_bucket.pwa.bucket_regional_domain_name
    origin_id                = "s3-pwa"
    origin_access_control_id = aws_cloudfront_origin_access_control.pwa.id
  }

  default_cache_behavior {
    allowed_methods        = ["GET", "HEAD", "OPTIONS"]
    cached_methods         = ["GET", "HEAD"]
    target_origin_id       = "s3-pwa"
    viewer_protocol_policy = "redirect-to-https"
    compress               = true

    forwarded_values {
      query_string = false
      cookies { forward = "none" }
    }

    min_ttl     = 0
    default_ttl = 3600
    max_ttl     = 86400
  }

  # SPA fallback — serve index.html for unknown paths
  custom_error_response {
    error_code            = 403
    response_code         = 200
    response_page_path    = "/index.html"
    error_caching_min_ttl = 0
  }

  custom_error_response {
    error_code            = 404
    response_code         = 200
    response_page_path    = "/index.html"
    error_caching_min_ttl = 0
  }

  restrictions {
    geo_restriction { restriction_type = "none" }
  }

  viewer_certificate {
    cloudfront_default_certificate = true
  }

  tags = { Name = "${var.app_name}-pwa-cf" }
}

resource "aws_s3_bucket_policy" "pwa" {
  bucket = aws_s3_bucket.pwa.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = { Service = "cloudfront.amazonaws.com" }
      Action    = "s3:GetObject"
      Resource  = "${aws_s3_bucket.pwa.arn}/*"
      Condition = {
        StringEquals = {
          "AWS:SourceArn" = aws_cloudfront_distribution.pwa.arn
        }
      }
    }]
  })
}
```

### `variables.tf`

```hcl
variable "app_name" {
  description = "Application name, used as a prefix for all resources"
  type        = string
  default     = "healthhelper"
}

variable "environment" {
  description = "Deployment environment"
  type        = string
  default     = "production"
}

variable "aws_region" {
  description = "AWS region for all resources"
  type        = string
  default     = "us-east-1"
}

variable "github_org" {
  description = "GitHub organisation or username that owns the repository"
  type        = string
}

variable "github_repo" {
  description = "GitHub repository name"
  type        = string
}

# ── Database ──────────────────────────────────────────────────
variable "db_instance_class" {
  description = "RDS instance class"
  type        = string
  default     = "db.t3.micro"
}

variable "db_password" {
  description = "RDS master password — store in tfvars, never commit"
  type        = string
  sensitive   = true
}

variable "enable_multi_az" {
  description = "Enable Multi-AZ for RDS (recommended for production)"
  type        = bool
  default     = false
}

# ── Redis ─────────────────────────────────────────────────────
variable "redis_node_type" {
  description = "ElastiCache Redis node type"
  type        = string
  default     = "cache.t3.micro"
}

variable "redis_auth_token" {
  description = "Auth token for ElastiCache Redis TLS — store in tfvars, never commit"
  type        = string
  sensitive   = true
}

# ── ECS ───────────────────────────────────────────────────────
variable "api_cpu" {
  description = "Fargate CPU units for API task (1024 = 1 vCPU)"
  type        = number
  default     = 512
}

variable "api_memory" {
  description = "Fargate memory (MB) for API task"
  type        = number
  default     = 1024
}

variable "api_desired_count" {
  description = "Number of API ECS task replicas"
  type        = number
  default     = 2
}

variable "worker_cpu" {
  description = "Fargate CPU units for Celery worker task"
  type        = number
  default     = 512
}

variable "worker_memory" {
  description = "Fargate memory (MB) for Celery worker task"
  type        = number
  default     = 1024
}

variable "worker_desired_count" {
  description = "Number of Celery worker ECS task replicas"
  type        = number
  default     = 1
}

# ── ACM ───────────────────────────────────────────────────────
variable "acm_certificate_arn" {
  description = "ARN of the ACM certificate for the ALB HTTPS listener (must be in us-east-1)"
  type        = string
}

# ── FHIR ─────────────────────────────────────────────────────
variable "fhir_server_url" {
  description = "FHIR R4 server base URL"
  type        = string
  default     = "https://r4.smarthealthit.org"
}

variable "fhir_client_id" {
  description = "SMART on FHIR client ID"
  type        = string
}
```

### `outputs.tf`

```hcl
output "alb_dns_name" {
  description = "DNS name of the Application Load Balancer — use for API calls and Better Stack monitoring"
  value       = aws_lb.main.dns_name
}

output "cloudfront_domain_name" {
  description = "CloudFront domain for the PWA — set as EXPO_PUBLIC_API_URL in CI"
  value       = aws_cloudfront_distribution.pwa.domain_name
}

output "cloudfront_distribution_id" {
  description = "CloudFront distribution ID — used for cache invalidation in GitHub Actions"
  value       = aws_cloudfront_distribution.pwa.id
}

output "ecr_repository_url" {
  description = "ECR repository URL for the backend image"
  value       = aws_ecr_repository.backend.repository_url
}

output "ecs_cluster_name" {
  description = "ECS cluster name"
  value       = aws_ecs_cluster.main.name
}

output "api_task_definition_arn" {
  description = "ARN of the API ECS task definition (used for one-off migration tasks)"
  value       = aws_ecs_task_definition.api.arn
}

output "rds_endpoint" {
  description = "RDS PostgreSQL endpoint (host only)"
  value       = aws_db_instance.main.endpoint
  sensitive   = true
}

output "redis_endpoint" {
  description = "ElastiCache Redis primary endpoint"
  value       = aws_elasticache_replication_group.redis.primary_endpoint_address
  sensitive   = true
}

output "pwa_s3_bucket_name" {
  description = "S3 bucket name for PWA static files"
  value       = aws_s3_bucket.pwa.bucket
}

output "api_security_group_id" {
  description = "Security group ID for ECS tasks — used for one-off migration tasks"
  value       = aws_security_group.ecs.id
}

output "private_subnet_ids" {
  description = "Private subnet IDs — used for one-off ECS tasks"
  value       = aws_subnet.private[*].id
}

output "github_actions_role_arn" {
  description = "IAM role ARN for GitHub Actions OIDC — add as AWS_ACCOUNT_ID var in GitHub"
  value       = aws_iam_role.github_actions.arn
}
```

### `production.tfvars`

```hcl
# production.tfvars — DO NOT COMMIT — add to .gitignore

app_name    = "healthhelper"
environment = "production"
aws_region  = "us-east-1"

# GitHub — for OIDC trust policy
github_org  = "your-github-org"
github_repo = "healthhelper"

# RDS
db_instance_class = "db.t3.small"
db_password       = "CHANGE_ME_USE_STRONG_PASSWORD"
enable_multi_az   = false   # set true for production resilience

# Redis
redis_node_type  = "cache.t3.micro"
redis_auth_token = "CHANGE_ME_USE_STRONG_RANDOM_TOKEN"

# ECS sizing
api_cpu           = 512
api_memory        = 1024
api_desired_count = 2

worker_cpu           = 512
worker_memory        = 1024
worker_desired_count = 1

# ACM — request a certificate in us-east-1 before applying
acm_certificate_arn = "arn:aws:acm:us-east-1:YOUR_ACCOUNT_ID:certificate/YOUR_CERT_ID"

# FHIR
fhir_server_url = "https://r4.smarthealthit.org"
fhir_client_id  = "your-fhir-client-id"
```

---

## Notes

**Cost estimate (us-east-1, minimal production setup):**
| Service | Approx. monthly cost |
|---|---|
| ECS Fargate (API × 2 + worker × 1, 0.5 vCPU / 1 GB each) | ~$30–45 |
| RDS PostgreSQL 17 (db.t3.small, 20 GB gp3) | ~$25–30 |
| ElastiCache Redis (cache.t3.micro) | ~$15 |
| ALB | ~$20 |
| NAT Gateway | ~$35 (per AZ + data transfer) |
| S3 + CloudFront | ~$1–5 |
| AWS Secrets Manager (6 secrets) | ~$3 |
| CloudWatch Logs | ~$2–5 |
| **Total** | **~$130–160/month** |

**Before your first `terraform apply`:**
1. Request an ACM certificate for your domain in `us-east-1` via the AWS Console — Terraform cannot create one without a verified domain.
2. Add `production.tfvars` to your `.gitignore` immediately.
3. Create an S3 bucket manually for Terraform remote state, then uncomment the `backend "s3"` block in `main.tf`.

**Mobile app distribution:** The Expo iOS and Android builds are distributed through the App Store and Google Play respectively — not through this AWS infrastructure. Use Expo EAS Build (`eas build`) and EAS Submit (`eas submit`) for mobile app builds and store submissions. The `EXPO_PUBLIC_API_URL` environment variable in EAS should point to your ALB DNS name.

**On-device model download (Phase 10):** The 2–3 GB GGUF model files should be served from a separate S3 bucket with CloudFront, not from your API. This keeps large binary transfers off your Fargate tasks. Create a dedicated `healthhelper-models` S3 bucket with CloudFront and pre-signed URLs issued by the API.

**HIPAA / clinical data:** If HealthHelper will handle PHI (Protected Health Information) in a US context, you will need to enable AWS HIPAA-eligible services configuration, sign a Business Associate Agreement (BAA) with AWS, enable RDS encryption at rest (already included), and review your CloudWatch log retention to avoid logging PHI. Consult a compliance specialist before go-live.