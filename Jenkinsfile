// iloveawschoolunch/Jenkinsfile

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

        // 3단계: 프론트엔드 배포하기 (수정된 최종 버전)
        stage('Deploy Frontend') {
            steps {
                // 먼저 빌드가 완료된 'frontend/dist' 폴더 안으로 이동합니다.
                dir('frontend/dist') {
                    script {
                        withAWS(credentials: 'aws-credentials', region: 'ap-northeast-2') {
                            def bucketName = "iloveawschoolunch-frontend-bucket-210cb53cc6da0d61"
                            
                            // 현재 폴더(dist)의 모든 내용물을 버킷 최상위에 '공개 읽기' 권한으로 업로드합니다.
                            s3Upload(
                                bucket: bucketName,
                                path: '/',
                                file: '**/*', // 현재 폴더의 모든 파일 및 하위 폴더를 의미
                                uploadingStrategy: 'publicRead' // 공개 읽기 권한으로 설정
                            )
                        }
                    }
                }
            }
        }
    }
}