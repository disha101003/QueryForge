# Contributing to the Project

Welcome! We’re excited to have you contribute to this project. This guide will help you understand our directory structure, where to add code, and how to make your contributions effectively.

## Table of Contents

1. [Directory Structure](#directory-structure)
2. [Setting Up the Project](#setting-up-the-project)
3. [Contribution Guidelines](#contribution-guidelines)
4. [Code Style and Best Practices](#code-style-and-best-practices)
5. [Running Tests and Application locally](#running-tests)
6. [Submitting a Pull Request](#submitting-a-pull-request)
7. [Packaging the Application](#packaging-the-application)
8. [Versioning](#versioning)
9. [Pushing the docker image to AWS ECR](#pushing-the-docker-image-to-aws-ecr)
10. [Deploying to AWS ECS](#deploying-to-aws-ecs)
11. [Version Visibility](#version-visibility)
---

## Directory Structure

Here is an overview of the main folders in this project. Each section explains the purpose of each directory and how to contribute code to it.

### Root Directory (`.`)
The root directory contains essential files for configuration, documentation, and project setup.

- **dist/**: Compiled files and distributions go here. Generally, you won’t modify files in this folder directly.
- **htmlcov/**: Coverage reports for the codebase. These files are generated automatically when tests are run and shouldn’t be edited manually.
- **src/**: The main source folder for the project, containing all application code, organized into backend and frontend components.

### Backend (`src/backend`)
The `backend` folder contains server-side code.

- **app/**: The main application code for the backend.
  - **instance/**: Contains instance-specific configuration and temporary files. Do not commit any sensitive information in this folder.
- **database/**: Contains database models, migrations, and connection setup.
- **documents/**: Documentation files specific to the backend implementation.
- **config/**: Configuration files for setting up the backend, including environment settings, database configurations, etc.

### Frontend (`src/frontend`)
The `frontend` folder contains all client-side code.

- **css/**: Stylesheets for the frontend. Add any custom CSS files here.
- **js/**: JavaScript files for the frontend. Use this folder for custom JavaScript code.
- **templates/**: HTML templates for the frontend. All frontend views should go here.

### Tests (`src/tests`)
The `tests` folder contains all unit and integration tests.

- **unit/**: Unit tests for the application. Add any new unit tests here to cover specific functionality.

### UI (`UI`)
Files and resources for UI elements, such as images or custom assets, should be added here.

---
# Setting Up the Project

To set up the project on your local machine:

1. Clone the repository:
   ```bash
   git clone https://github.com/disha101003/QueryForge
   ```

2. Install required dependencies
  ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables based on config files in the src/backend/config folder.

# Contributing Guidelines

## Code Style and Best Practices

* **Python Code:** Follow PEP 8 guidelines
* **CSS:** Follow BEM (Block Element Modifier) naming conventions for classes

## Contribution Process

1. Fork the repository and clone it to your local machine
2. Document your code to ensure clarity
3. Code quality:
   * Follow the project's coding standards
   * Ensure all tests pass before creating a pull request

## Running Tests

Navigate to the src/tests directory and run:

```bash
pytest
```

This will execute all tests and provide a coverage report.

## Commands to run the application locally

To run the application:

1. Navigate to the backend folder:
   ```bash
   cd src/backend
   ```

2. Run the application:
   ```bash
   python -m app.app
   ```

## Submitting a Pull Request

1. Create a Branch:
   ```bash
   git checkout -b feature-name
   ```

2. Commit Changes:
   * Make sure your commits are descriptive

3. Push Changes:
   * Push your branch to your forked repository

4. Create a Pull Request:
   * Go to the main repository and open a pull request

## Packaging, Versioning, and Deployment with AWS ECR and ECS

This section outlines the complete process for packaging your application into a Docker container, managing versioning, and deploying the containerized application to AWS Elastic Container Service (ECS) via Elastic Container Registry (ECR). The workflow ensures consistent deployment and seamless version control.

---

## 1. Packaging the Application

### Step 1.1: Docker Image Creation

Create a `Dockerfile` to define your Docker image. Include:

- A base image (e.g., `python:3.9-slim`).
- Commands to install dependencies.
- Instructions to copy the application code into the container.

Example `Dockerfile`:

```dockerfile
FROM python:3.10-slim
WORKDIR QueryForge
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD cd src/backend folder && python -m app.app
```

Build the Docker image:

```bash
docker build -t <image-name>:<version> .
```

For example:

```bash
docker build -t my-app:v0.5.0 .
```

---

## 2. Versioning

### Semantic Versioning
Follow the `major.minor.patch` format:

- **Major (X.0.0):** For breaking changes or significant features.
- **Minor (0.X.0):** For backward-compatible feature additions.
- **Patch (0.0.X):** For bug fixes or minor updates.

### Current Version
Initial version: `v0.5.0`.

- **Major (0):** Early development stage.
- **Minor (5):** Reflects five feature increments.
- **Patch (0):** Indicates no bug fixes yet.

---

## 3. Pushing the Docker Image to AWS ECR

### Step 3.1: Create an ECR Repository

Create an ECR repository to store the Docker image:

```bash
aws ecr create-repository --repository-name <repository-name>
```

For example:

```bash
aws ecr create-repository --repository-name my-app
```

### Step 3.2: Authenticate Docker with ECR

Log in to ECR using AWS CLI:

```bash
aws ecr get-login-password --region <region> | docker login --username AWS --password-stdin <aws_account_id>.dkr.ecr.<region>.amazonaws.com
```

### Step 3.3: Tag and Push the Docker Image

Tag the image:

```bash
docker tag <image-name>:<version> <aws_account_id>.dkr.ecr.<region>.amazonaws.com/<repository-name>:<version>
```

Example:

```bash
docker tag my-app:v0.5.0 123456789012.dkr.ecr.us-east-1.amazonaws.com/my-app:v0.5.0
```

Push the image to ECR:

```bash
docker push <aws_account_id>.dkr.ecr.<region>.amazonaws.com/<repository-name>:<version>
```

Example:

```bash
docker push 123456789012.dkr.ecr.us-east-1.amazonaws.com/my-app:v0.5.0
```

---

## 4. Deploying to AWS ECS

### Step 4.1: Create an ECS Cluster

Create an ECS cluster to host your Docker containers:

```bash
aws ecs create-cluster --cluster-name <cluster-name>
```

Example:

```bash
aws ecs create-cluster --cluster-name my-app-cluster
```

### Step 4.2: Register a Task Definition

Create a task definition file (e.g., `task-definition.json`):

```json
{
  "family": "my-app-task",
  "containerDefinitions": [
    {
      "name": "my-app",
      "image": "123456789012.dkr.ecr.us-east-1.amazonaws.com/my-app:v0.5.0",
      "memory": 512,
      "cpu": 256,
      "essential": true,
      "portMappings": [
        {
          "containerPort": 80,
          "hostPort": 80
        }
      ]
    }
  ]
}
```

Register the task definition:

```bash
aws ecs register-task-definition --cli-input-json file://task-definition.json
```

### Step 4.3: Run a Task

Run the registered task in your ECS cluster:

```bash
aws ecs run-task --cluster <cluster-name> --task-definition <task-family-name>
```

Example:

```bash
aws ecs run-task --cluster my-app-cluster --task-definition my-app-task
```

### Step 4.4: Create a Service (Optional)

To scale and manage tasks automatically:

```bash
aws ecs create-service \
    --cluster <cluster-name> \
    --service-name <service-name> \
    --task-definition <task-family-name> \
    --desired-count <number-of-tasks>
```

Example:

```bash
aws ecs create-service \
    --cluster my-app-cluster \
    --service-name my-app-service \
    --task-definition my-app-task \
    --desired-count 2
```

---

## 5. Version Visibility

- **Docker Image Metadata:** The version is embedded in the image tag (e.g., `v0.5.0`) for easy reference.
- **Application UI:** Display the version number in the application’s footer.
