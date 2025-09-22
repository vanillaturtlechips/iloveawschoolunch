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

        // --- Frontend Stages (기존과 동일) ---
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
                dir('backend') { // Dockerfile이 있는 backend 폴더로 이동
                    script {
                  
                       // 1. Docker Hub 로그인 (사용자 ID 적용)
                       sh """echo $DOCKERHUB_CREDENTIALS |
 docker login -u ${DOCKER_IMAGE_NAME.split('/')[0]} --password-stdin"""

                        // 2. Docker 이미지 빌드
                        sh "docker build -t ${env.DOCKER_IMAGE_NAME}:${env.DOCKER_IMAGE_TAG} ."

                        // 3. Docker Hub에 이미지 푸시
          
                        sh "docker push ${env.DOCKER_IMAGE_NAME}:${env.DOCKER_IMAGE_TAG}"
                    }
                }
            }
        }

        stage('Deploy Backend to EC2') {
            steps {
                script {
                    sh """
                        # 기존 컨테이너가 있다면 중지하고 삭제 (무중단 배포를 위한 준비)
                 
                        docker stop iloveawschoolunch-backend || true
                        docker rm iloveawschoolunch-backend || true

                        # Docker Hub에서 최신 이미지 받아오기
                        docker pull ${env.DOCKER_IMAGE_NAME}:${env.DOCKER_IMAGE_TAG}

                        # Gunicorn을 실행하는 새 컨테이너를 백그라운드에서 실행
               
                        docker run -d --name iloveawschoolunch-backend -p 8000:8000 ${env.DOCKER_IMAGE_NAME}:${env.DOCKER_IMAGE_TAG} gunicorn wsgi:application --bind 0.0.0.0:8000 --log-level debug
                    """
                }
            }
        }
    }
}