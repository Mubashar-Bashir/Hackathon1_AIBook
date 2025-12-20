#!/usr/bin/env python3
"""
Deployment Configurator Script

This script sets up deployment configurations for different environments for the Physical AI & Humanoid Robotics textbook project.
"""

import argparse
import json
import os
from typing import Dict, List, Any

def load_deployment_patterns():
    """Load deployment patterns from assets/deployment_patterns.json"""
    patterns_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'deployment_patterns.json')
    if os.path.exists(patterns_path):
        with open(patterns_path, 'r') as f:
            return json.load(f)
    else:
        # Default deployment patterns
        return {
            "environments": {
                "development": {
                    "name": "Development",
                    "variables": {
                        "DEBUG": "True",
                        "LOG_LEVEL": "DEBUG",
                        "DATABASE_URL": "sqlite:///dev.db",
                        "ENVIRONMENT": "development"
                    },
                    "scaling": {
                        "min_instances": 1,
                        "max_instances": 1,
                        "cpu_limit": "500m",
                        "memory_limit": "512Mi"
                    }
                },
                "staging": {
                    "name": "Staging",
                    "variables": {
                        "DEBUG": "False",
                        "LOG_LEVEL": "INFO",
                        "DATABASE_URL": "postgresql://staging_db",
                        "ENVIRONMENT": "staging"
                    },
                    "scaling": {
                        "min_instances": 1,
                        "max_instances": 2,
                        "cpu_limit": "1000m",
                        "memory_limit": "1Gi"
                    }
                },
                "production": {
                    "name": "Production",
                    "variables": {
                        "DEBUG": "False",
                        "LOG_LEVEL": "WARNING",
                        "DATABASE_URL": "postgresql://prod_db",
                        "ENVIRONMENT": "production",
                        "SECRET_KEY": "set_in_env_var",
                        "ALLOWED_HOSTS": "yourdomain.com"
                    },
                    "scaling": {
                        "min_instances": 2,
                        "max_instances": 10,
                        "cpu_limit": "2000m",
                        "memory_limit": "4Gi",
                        "horizontal_pod_autoscaler": True
                    }
                }
            },
            "deployment_platforms": {
                "docker": {
                    "config_files": ["Dockerfile", "docker-compose.yml"],
                    "templates": {
                        "Dockerfile": '''FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]''',
                        "docker-compose.yml": '''version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - ENVIRONMENT={environment}
      - DEBUG={debug}
    volumes:
      - .:/app
    depends_on:
      - db

  db:
    image: postgres:13
    environment:
      POSTGRES_DB: textbook
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:'''}
                },
                "kubernetes": {
                    "config_files": ["deployment.yaml", "service.yaml", "ingress.yaml"],
                    "templates": {
                        "deployment.yaml": '''apiVersion: apps/v1
kind: Deployment
metadata:
  name: ai-textbook-app
spec:
  replicas: {replicas}
  selector:
    matchLabels:
      app: ai-textbook
  template:
    metadata:
      labels:
        app: ai-textbook
    spec:
      containers:
      - name: ai-textbook
        image: ai-textbook:latest
        ports:
        - containerPort: 8000
        env:
        - name: ENVIRONMENT
          value: "{environment}"
        resources:
          requests:
            memory: "{memory_limit}"
            cpu: "{cpu_limit}"
          limits:
            memory: "{memory_limit}"
            cpu: "{cpu_limit}"'''
                    }
                },
                "vercel": {
                    "config_files": ["vercel.json"],
                    "templates": {
                        "vercel.json": '''{
  "version": 2,
  "builds": [
    {
      "src": "backend/main.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "backend/main.py"
    }
  ]
}'''
                    }
                }
            },
            "ci_cd_templates": {
                "github_actions": {
                    "filename": ".github/workflows/deploy.yml",
                    "template": '''name: Deploy

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2

    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v1

    - name: Login to DockerHub
      uses: docker/login-action@v1
      with:
        username: ${{ secrets.DOCKERHUB_USERNAME }}
        password: ${{ secrets.DOCKERHUB_TOKEN }}

    - name: Build and push
      uses: docker/build-push-action@v2
      with:
        context: .
        push: true
        tags: user/ai-textbook:latest'''
                }
            }
        }

def generate_deployment_config(project_path: str, target_env: str, platform: str, scaling_req: str) -> Dict[str, Any]:
    """Generate deployment configuration based on inputs."""

    patterns = load_deployment_patterns()

    # Get environment-specific configuration
    env_config = patterns["environments"].get(target_env, patterns["environments"]["development"])

    # Get platform-specific configuration
    platform_config = patterns["deployment_platforms"].get(platform, patterns["deployment_platforms"]["docker"])

    # Generate configuration files based on platform
    config_files = {}

    if platform == "docker":
        dockerfile_content = platform_config["templates"]["Dockerfile"]
        compose_content = platform_config["templates"]["docker-compose.yml"].format(
            environment=target_env,
            debug="true" if target_env == "development" else "false"
        )

        config_files = {
            "Dockerfile": dockerfile_content,
            "docker-compose.yml": compose_content
        }
    elif platform == "kubernetes":
        deployment_yaml = platform_config["templates"]["deployment.yaml"].format(
            replicas=env_config["scaling"]["min_instances"],
            environment=target_env,
            cpu_limit=env_config["scaling"]["cpu_limit"],
            memory_limit=env_config["scaling"]["memory_limit"]
        )

        config_files = {
            "deployment.yaml": deployment_yaml
        }
    elif platform == "vercel":
        config_files = {
            "vercel.json": platform_config["templates"]["vercel.json"]
        }

    # Generate CI/CD pipeline
    ci_cd_config = patterns["ci_cd_templates"]["github_actions"]["template"]

    # Determine scaling configuration based on requirements
    scaling_levels = {
        "low": {"min_instances": 1, "max_instances": 2},
        "medium": {"min_instances": 2, "max_instances": 5},
        "high": {"min_instances": 3, "max_instances": 10},
        "auto": {"min_instances": 2, "max_instances": 20, "autoscale": True}
    }
    scaling_config = scaling_levels.get(scaling_req, scaling_levels["medium"])

    return {
        "project_path": project_path,
        "target_environment": target_env,
        "deployment_platform": platform,
        "configuration_files": config_files,
        "environment_variables": env_config["variables"],
        "ci_cd_pipeline": {
            "type": "github_actions",
            "configuration": ci_cd_config
        },
        "scaling_strategy": {
            "requirements": scaling_req,
            "configuration": scaling_config,
            "resource_limits": env_config["scaling"]
        }
    }

def main():
    parser = argparse.ArgumentParser(description='Deployment Configurator')
    parser.add_argument('--project-path', type=str, required=True, help='Path to the project to configure for deployment')
    parser.add_argument('--target-environment', type=str, default='production',
                       choices=['development', 'staging', 'production'],
                       help='Target environment for deployment')
    parser.add_argument('--deployment-platform', type=str, default='docker',
                       choices=['docker', 'kubernetes', 'vercel'],
                       help='Platform for deployment')
    parser.add_argument('--scaling-requirements', type=str, default='medium',
                       choices=['low', 'medium', 'high', 'auto'],
                       help='Scaling requirements for the deployment')

    args = parser.parse_args()

    # Validate project path
    if not os.path.exists(args.project_path):
        print(json.dumps({
            "error": f"Project path does not exist: {args.project_path}",
            "available_options": {
                "environments": ["development", "staging", "production"],
                "platforms": ["docker", "kubernetes", "vercel"],
                "scaling": ["low", "medium", "high", "auto"]
            }
        }))
        return

    # Generate deployment configuration
    config = generate_deployment_config(
        args.project_path,
        args.target_environment,
        args.deployment_platform,
        args.scaling_requirements
    )

    # Prepare output
    output = {
        "input": {
            "project_path": args.project_path,
            "target_environment": args.target_environment,
            "deployment_platform": args.deployment_platform,
            "scaling_requirements": args.scaling_requirements
        },
        "deployment_config": config
    }

    print(json.dumps(output, indent=2))

if __name__ == "__main__":
    main()