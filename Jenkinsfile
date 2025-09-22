// iloveawschoolunch/Jenkinsfile (Final Version)

pipeline {
    agent any
    environment {
        DOCKERHUB_CREDENTIALS = credentials('DOCKERHUB_PASSWORD')
        DOCKER_IMAGE_NAME = "kwa06001/iloveawschoolunch-backend"
        DOCKER_IMAGE_TAG = "latest"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Build Frontend') {
            tools {
                nodejs 'node-20'
            }
            steps {
                dir('frontend') {
                    sh 'npm install'
                    sh 'npm run build'
                    sh 'ls -la dist/'
                }
            }
        }
        stage('Deploy Frontend') {
            steps {
                script {
                    withAWS(credentials: 'aws-credentials', region: 'ap-northeast-2') {
                        def bucketName = "iloveawschoolunch-frontend-bucket-210cb53cc6da0d61"
                        s3Upload(
                            bucket: bucketName,
                            path: '',
                            includePathPattern: '**/*',
                            workingDir: 'frontend/dist'
                        )
                        echo "Frontend deployed to S3 bucket: ${bucketName}"
                    }
                }
            }
        }
        stage('Build & Push Docker Image') {
            steps {
                dir('backend') {
                    script {
                        sh """echo $DOCKERHUB_CREDENTIALS | docker login -u ${DOCKER_IMAGE_NAME.split('/')[0]} --password-stdin"""
                        sh "docker build -t ${env.DOCKER_IMAGE_NAME}:${env.DOCKER_IMAGE_TAG} ."
                        sh "docker push ${env.DOCKER_IMAGE_NAME}:${env.DOCKER_IMAGE_TAG}"
                    }
                }
            }
        }
        stage('Deploy Backend to EC2') {
            steps {
                script {
                    sh """
                        docker stop iloveawschoolunch-backend || true
                        docker rm iloveawschoolunch-backend || true
                        docker pull ${env.DOCKER_IMAGE_NAME}:${env.DOCKER_IMAGE_TAG}
                        docker run -d --name iloveawschoolunch-backend -p 8000:8000 ${env.DOCKER_IMAGE_NAME}:${env.DOCKER_IMAGE_TAG} gunicorn wsgi:application --bind 0.0.0.0:8000 --log-level debug
                    """
                }
            }
        }
    }
}