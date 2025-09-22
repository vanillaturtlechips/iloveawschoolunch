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
                    // 빌드 결과 확인
                    sh 'ls -la dist/'
                }
            }
        }

        // 3단계: 프론트엔드 배포하기 (AWS CLI 없이)
        stage('Deploy Frontend') {
            steps {
                script {
                    withAWS(credentials: 'aws-credentials', region: 'ap-northeast-2') {
                        def bucketName = "iloveawschoolunch-frontend-bucket-210cb53cc6da0d61"
                        
                        // S3 플러그인만 사용해서 업로드
                        s3Upload(
                            bucket: bucketName,
                            path: '',  // 버킷 루트에 업로드
                            includePathPattern: '**/*',  // 모든 파일 포함
                            workingDir: 'frontend/dist'  // 작업 디렉토리 지정
                        )
                        
                        echo "Frontend deployed to S3 bucket: ${bucketName}"
                    }
                }
            }
        }
    }
}