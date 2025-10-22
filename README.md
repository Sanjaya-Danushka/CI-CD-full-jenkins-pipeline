# My Python App

A simple Flask application with a comprehensive Jenkins CI/CD pipeline.

## Project Structure

```
my-python-app/
│
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── test_app.py         # Unit tests
├── Dockerfile          # Docker container definition
├── Jenkinsfile         # Jenkins pipeline definition
├── performance_test.py # Performance tests with Locust
├── k8s/
│   ├── staging/        # Staging Kubernetes manifests
│   └── production/     # Production Kubernetes manifests
└── README.md          # This file
```

## Jenkins Pipeline Features

The Jenkinsfile includes the following stages:

### 1. **Checkout**
- Retrieves code from the source control repository

### 2. **Setup Python Environment**
- Creates a virtual environment
- Installs project dependencies

### 3. **Run Tests**
- Executes unit tests with pytest
- Generates coverage reports
- Publishes test results and coverage reports

### 4. **Code Quality Analysis**
- Runs linting with flake8
- Checks code formatting with black
- Validates import sorting with isort

### 5. **Security Scan**
- Runs dependency vulnerability scans with safety
- Performs static security analysis with bandit

### 6. **Build Docker Image**
- Builds Docker image with the application
- Pushes to container registry with build number and 'latest' tags

### 7. **Deploy to Staging**
- Deploys application to staging environment using Kubernetes
- Waits for deployment readiness

### 8. **Integration Tests**
- Runs tests against the staging environment
- Validates health endpoints and basic functionality

### 9. **Performance Tests**
- Executes load tests using Locust
- Validates application performance under load

### 10. **Deploy to Production**
- Requires manual approval before deployment
- Deploys to production environment

## Prerequisites

### Jenkins Setup
1. **Install Required Plugins:**
   - Pipeline
   - Docker Pipeline
   - Kubernetes Deploy
   - Email Extension
   - Cobertura (for coverage reports)
   - JUnit (for test results)

2. **Configure Credentials:**
   - `docker-registry-credentials`: Docker registry credentials
   - `kubeconfig`: Kubernetes cluster access credentials

3. **Configure Tools:**
   - Python 3.x
   - Docker
   - kubectl

### Environment Variables
Update the following in the Jenkinsfile:
- `DOCKER_REGISTRY`: Your Docker registry URL
- `SONARQUBE_SERVER`: Your SonarQube server name (if using)
- Update Kubernetes deployment files with your domain names

## Running the Pipeline

### Automatic Triggers
The pipeline can be triggered by:
- SCM changes (push to repository)
- Scheduled builds (cron expressions)
- Manual triggers from Jenkins UI

### Manual Execution
1. Go to your Jenkins job
2. Click "Build Now"
3. Monitor the pipeline progress
4. Check console output for detailed logs

## Pipeline Stages Explained

### Environment Variables
```groovy
environment {
    DOCKER_IMAGE = 'my-python-app'
    DOCKER_TAG = "${env.BUILD_NUMBER}"
    DOCKER_REGISTRY = 'your-registry.com'
    KUBECONFIG = credentials('kubeconfig')
}
```

### Test Results Integration
- JUnit XML reports are automatically published
- Coverage reports are generated in HTML and XML formats
- Test artifacts are archived for historical reference

### Docker Integration
```groovy
docker.withRegistry("https://${DOCKER_REGISTRY}", 'docker-registry-credentials') {
    def app = docker.build("${DOCKER_REGISTRY}/${DOCKER_IMAGE}:${DOCKER_TAG}")
    app.push()
    app.push('latest')
}
```

### Kubernetes Deployment
- Uses `kubernetesDeploy` step for deployment
- Supports environment-specific configurations
- Includes health checks and resource limits

## Notifications

The pipeline includes email notifications for:
- **Success**: Build completed successfully
- **Failure**: Build failed with error details
- **Unstable**: Build completed but with warnings

## Troubleshooting

### Common Issues

1. **Docker Build Fails**
   - Check Docker daemon is running
   - Verify registry credentials
   - Ensure sufficient disk space

2. **Kubernetes Deployment Fails**
   - Verify cluster connectivity
   - Check kubectl configuration
   - Validate YAML syntax in deployment files

3. **Tests Failing**
   - Check Python environment setup
   - Verify test dependencies
   - Review test logs for specific errors

### Debug Mode
Enable verbose logging in Jenkins:
```groovy
options {
    timestamps()
    ansiColor('xterm')
}
```

## Security Considerations

- All credentials are stored securely in Jenkins
- Container images are scanned for vulnerabilities
- Code is analyzed for security issues with Bandit
- Dependencies are checked for known vulnerabilities with Safety

## Performance Monitoring

- Integration tests validate functionality in staging
- Performance tests ensure application can handle load
- Health checks monitor application availability
- Resource limits prevent resource exhaustion

## Next Steps

1. Customize the pipeline for your specific requirements
2. Add more comprehensive tests
3. Integrate with monitoring tools (Prometheus, Grafana)
4. Set up automated rollback mechanisms
5. Add blue-green deployment strategy

## Support

For issues with the pipeline:
1. Check Jenkins system logs
2. Review pipeline console output
3. Validate configuration in Jenkins UI
4. Check plugin compatibility
