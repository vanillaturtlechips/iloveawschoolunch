pipeline {
    // Jenkins가 가능한 아무 작업 컴퓨터에서나 이 파이프라인을 실행합니다.
    agent any

    // 파이프라인의 각 단계를 정의합니다.
    stages {
        
        // 1단계: 소스 코드 가져오기
        stage('Checkout') {
            steps {
                // 파이프라인 설정에 연결된 GitHub 저장소에서 코드를 가져옵니다.
                checkout scm
            }
        }

        // 2단계: 프론트엔드 빌드하기
        stage('Build Frontend') {
            // 이 단계를 실행하기 전에 Jenkins Tools에 설정된 'node-20'을 준비합니다.
            tools {
                nodejs 'node-20'
            }
            steps {
                // 'frontend' 폴더로 이동해서 아래 명령어들을 실행합니다.
                dir('frontend') {
                    sh 'npm install'
                    sh 'npm run build'
                }
            }
        }

        // 3단계: 프론트엔드 배포하기
        stage('Deploy Frontend') {
            steps {
                // 'def'와 같은 스크립트 문법을 사용하기 위해 script 블록으로 감싸줍니다.
                script {
                    // withAWS 블록으로 AWS 인증/리전 설정을 적용합니다.
                    withAWS(credentials: 'aws-credentials', region: 'ap-northeast-2') {
                        
                        // AWS S3 콘솔에서 확인한 실제 버킷 이름을 변수로 지정합니다.
                        def bucketName = "iloveawschoolunch-frontend-bucket-210cb53cc6da0d61"
                        
                        // 'frontend/dist' 폴더의 내용물을 S3 버킷 최상위 경로에 업로드합니다.
                        s3Upload(
                            file: 'frontend/dist',
                            bucket: bucketName,
                            path: '/',
                            uploadingStrategy: 'publicRead'
                        )
                    }
                }
            }
        }
    }
}

