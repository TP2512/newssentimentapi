pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                // Checkout your code from version control
                git 'your_repo_url'
            }
        }

        stage('Build') {
            steps {
                // Build your FastAPI application
                sh 'docker build -t sentimentanalysisapi:latest .'
            }
        }

        stage('Test') {
            steps {
                // Run tests for your application
                sh 'docker run --rm sentimentanalysisapi:latest pytest /code/test'
            }
        }

        stage('Deploy') {
            steps {
                // Deploy your application to Kubernetes
                sh 'kubectl apply -f deployment.yml'
            }
        }
    }

    post {
        always {
            // Cleanup steps
            sh 'docker rmi your_image_name'
        }
    }
}
