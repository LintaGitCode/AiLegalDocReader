# AWS Deployment Plan

AWS deployment should come after the local Docker flow is reliable.

## Docker

Build separate Docker images for the backend and frontend. Keep environment-specific configuration outside the images.

## ECR

Push backend and frontend images to Amazon Elastic Container Registry.

## ECS Fargate

Run containers on ECS Fargate so the app does not require managing EC2 servers.

## Application Load Balancer

Place an Application Load Balancer in front of the services. Route frontend traffic to the frontend service and API traffic to the backend service.

## S3 for uploaded PDFs

Store uploaded PDFs in S3 if the app later needs persistence, audit trails, or multi-document workflows. v1 does not store uploaded PDFs.

## Secrets Manager or SSM Parameter Store

Store `OPENAI_API_KEY` in AWS Secrets Manager or SSM Parameter Store. Do not bake secrets into Docker images or commit them to Git.

## Managed vector search

When RAG is added, evaluate managed vector search options that fit the project budget and learning goals.
