# AWS Simple Storage Service (S3) Labs (LocalStack Pro)

![AWS](https://img.shields.io/badge/AWS-S3_Storage-FF9900?style=for-the-badge&logo=amazonaws)
![LocalStack](https://img.shields.io/badge/LocalStack-Pro-000000?style=for-the-badge)

This repository contains hands-on labs demonstrating core Amazon S3 concepts, from foundational storage and data protection to advanced security and lifecycle management. Using [LocalStack Pro](https://localstack.cloud/), we simulate a complete AWS storage environment locally.

## 🎯 Architecture Goals & Use Cases Covered
Based on AWS best practices (SAA-C03), these labs cover:
* **Data Protection:** Implementing Versioning to protect against accidental deletes and overwrites.
* **Security & Access Control:** (Upcoming) Exploring Bucket Policies and Access Control Lists (ACLs).
* **Lifecycle Management:** (Upcoming) Automating data transitions and expiration.
* **Hosting & Delivery:** (Upcoming) Configuring static website hosting.
* **Server-Side Encryption:** (Upcoming) Securing data at rest with SSE-S3 and SSE-KMS.

## ⚙️ Prerequisites

* [Docker](https://docs.docker.com/get-docker/) & Docker Compose
* [LocalStack Pro](https://app.localstack.cloud/) account and Auth Token
* [`awslocal` CLI](https://github.com/localstack/awscli-local) (a wrapper around the AWS CLI for LocalStack)

## 🚀 Environment Setup

1. Configure your LocalStack Auth Token in `.env`:
   ```bash
   echo "YOUR_TOKEN=your_auth_token_here" > .env
   ```

2. Start LocalStack Pro:
   ```bash
   docker-compose up -d
   ```

> [!IMPORTANT]
> **Cumulative Architecture:** These labs are designed as a cumulative scenario. You are building an evolving storage infrastructure.

## 📚 Labs Index
1. [Lab 1: Foundational S3 & Data Protection (Versioning)](./labs/lab1-s3-versioning/README.md)
2. [Lab 2: Compliance & Security (SSE-KMS & Object Lock)](./labs/lab2-s3-compliance-kms/README.md)
