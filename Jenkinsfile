// iloveawschoolunch/Jenkinsfile

pipeline {
    agent any

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
                }
            }
        }

        // 3단계: 프론트엔드 배포하기 (진짜 최종 버전)
        stage('Deploy Frontend') {
            steps {
                script {
                    withAWS(credentials: 'aws-credentials', region: 'ap-northeast-2') {
                        def bucketName = "iloveawschoolunch-frontend-bucket-210cb53cc6da0d61"
                        
                        // 'frontend/dist' 폴더의 내용물을 버킷에 업로드합니다.
                        // ACL 관련 옵션을 모두 제거합니다.
                        s3Upload(
                            bucket: bucketName,
                            path: '/',
                            file: 'frontend/dist/'
                        )
                    }
                }
            }
        }
    }
}