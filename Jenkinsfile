pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'my-python-app'
        DOCKER_TAG = "${env.BUILD_NUMBER}"
        DOCKER_REGISTRY = 'your-registry.com'  // Change this to your actual registry
        SONARQUBE_SERVER = 'SonarQube'  // Change this to your SonarQube server name in Jenkins
        KUBECONFIG = credentials('kubeconfig')  // Jenkins credential ID for Kubernetes access
    }

    stages {
        stage('Checkout') {
            steps {
                echo '🚀 Starting pipeline for my-python-app...'
                checkout scm
            }
        }

        stage('Setup Python Environment') {
            steps {
                echo '🐍 Setting up Python environment...'
                sh '''
                    python3 --version
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                echo '🧪 Running tests...'
                sh '''
                    . venv/bin/activate
                    python -m pytest test_app.py -v --cov=app --cov-report=xml --cov-report=html
                '''
            }
            post {
                always {
                    junit 'test-results.xml'  // If using pytest-junit
                    cobertura coberturaReportFile: 'coverage.xml'  // If using pytest-cov
                    publishHTML([
                        allowMissing: false,
                        alwaysLinkToLastBuild: true,
                        keepAll: true,
                        reportDir: 'htmlcov',
                        reportFiles: 'index.html',
                        reportName: 'Coverage Report'
                    ])
                }
                success {
                    echo '✅ All tests passed!'
                }
                failure {
                    echo '❌ Tests failed. Check the logs above.'
                }
            }
        }

        stage('Code Quality Analysis') {
            steps {
                echo '🔍 Running code quality checks...'
                sh '''
                    . venv/bin/activate
                    pip install flake8 black isort
                    flake8 app.py --count --select=E9,F63,F7,F82 --show-source --statistics
                    black --check --diff app.py
                    isort --check-only --diff app.py
                '''
            }
        }

        stage('Security Scan') {
            steps {
                echo '🔒 Running security scan...'
                sh '''
                    . venv/bin/activate
                    pip install safety bandit
                    safety check
                    bandit -r app.py -f json -o bandit-report.json || true
                '''
            }
            post {
                always {
                    archiveArtifacts artifacts: 'bandit-report.json', allowEmptyArchive: true
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                echo '🐳 Building Docker image...'
                script {
                    docker.withRegistry("https://${DOCKER_REGISTRY}", 'docker-registry-credentials') {
                        def app = docker.build("${DOCKER_REGISTRY}/${DOCKER_IMAGE}:${DOCKER_TAG}")
                        app.push()
                        app.push('latest')
                    }
                }
            }
            post {
                success {
                    echo "✅ Docker image built and pushed: ${DOCKER_REGISTRY}/${DOCKER_IMAGE}:${DOCKER_TAG}"
                }
                failure {
                    echo '❌ Docker build failed!'
                }
            }
        }

        stage('Deploy to Staging') {
            steps {
                echo '🚀 Deploying to staging environment...'
                script {
                    // Example Kubernetes deployment
                    kubernetesDeploy(
                        configs: 'k8s/staging/*.yaml',
                        kubeconfigId: 'kubeconfig',
                        enableConfigSubstitution: true
                    )
                }
            }
        }

        stage('Integration Tests') {
            steps {
                echo '🧪 Running integration tests against staging...'
                sh '''
                    # Wait for deployment to be ready
                    sleep 30

                    # Run integration tests
                    curl -f http://staging.my-python-app.com/health || exit 1
                    curl -f http://staging.my-python-app.com/ | jq '.message' | grep "Hello, World!" || exit 1
                '''
            }
        }

        stage('Performance Tests') {
            steps {
                echo '⚡ Running performance tests...'
                sh '''
                    # Install performance testing tools
                    pip install locust

                    # Run simple performance test
                    locust -f performance_test.py --no-gui -t 30s --headless || true
                '''
            }
        }

        stage('Deploy to Production') {
            steps {
                timeout(time: 15, unit: 'MINUTES') {
                    input message: '🚀 Deploy to Production?',
                          ok: 'Deploy',
                          submitterParameter: 'APPROVER'
                }

                echo '🚀 Deploying to production...'
                script {
                    // Deploy to production
                    kubernetesDeploy(
                        configs: 'k8s/production/*.yaml',
                        kubeconfigId: 'kubeconfig',
                        enableConfigSubstitution: true
                    )
                }
            }
        }
    }

    post {
        always {
            echo '🏁 Pipeline completed!'
            cleanWs()
        }
        success {
            echo '🎉 Pipeline succeeded!'
            // Send success notification
            emailext(
                subject: "✅ SUCCESS: ${currentBuild.fullDisplayName}",
                body: "Good news! Build ${env.BUILD_NUMBER} succeeded.\n\nCheck it out: ${env.BUILD_URL}",
                recipientProviders: [[$class: 'DevelopersRecipientProvider']]
            )
        }
        failure {
            echo '💥 Pipeline failed!'
            // Send failure notification
            emailext(
                subject: "❌ FAILED: ${currentBuild.fullDisplayName}",
                body: "Build ${env.BUILD_NUMBER} failed.\n\nCheck it out: ${env.BUILD_URL}",
                recipientProviders: [[$class: 'DevelopersRecipientProvider']]
            )
        }
        unstable {
            echo '⚠️ Pipeline is unstable!'
        }
    }
}
