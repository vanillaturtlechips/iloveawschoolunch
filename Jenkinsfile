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

        // 3단계: 프론트엔드 배포하기 (수정된 최종 버전)
        stage('Deploy Frontend') {
            steps {
                script {
                    withAWS(credentials: 'aws-credentials', region: 'ap-northeast-2') {
                        def bucketName = "iloveawschoolunch-frontend-bucket-210cb53cc6da0d61"
                        
                        // 'frontend/dist' 폴더의 내용물을 버킷에 업로드합니다.
                        s3Upload(
                            bucket: bucketName,
                            path: '/',
                            // 1. 파일 경로를 더 명확하게 지정합니다.
                            file: 'frontend/dist/', 
                            // 2. 권한 설정 옵션을 표준 파라미터로 변경합니다.
                            acl: 'PublicRead' 
                        )
                    }
                }
            }
        }
    }
}