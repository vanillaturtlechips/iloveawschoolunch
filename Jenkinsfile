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

        // 3단계: 프론트엔드 배포하기 (수정된 버전)
        stage('Deploy Frontend') {
            steps {
                script {
                    withAWS(credentials: 'aws-credentials', region: 'ap-northeast-2') {
                        def bucketName = "iloveawschoolunch-frontend-bucket-210cb53cc6da0d61"
                        
                        // 기존 버킷 내용 삭제 (선택사항)
                        sh "aws s3 rm s3://${bucketName}/ --recursive"
                        
                        // dist 폴더의 모든 파일을 버킷 루트에 업로드
                        s3Upload(
                            bucket: bucketName,
                            path: '',  // 버킷 루트에 업로드
                            includePathPattern: '**/*',  // 모든 파일 포함
                            workingDir: 'frontend/dist',  // 작업 디렉토리 지정
                            acl: 'PublicRead'  // 공개 읽기 권한 부여
                        )
                        
                        // 업로드 결과 확인
                        sh "aws s3 ls s3://${bucketName}/ --recursive"
                    }
                }
            }
        }
    }
}