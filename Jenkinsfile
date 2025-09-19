// iloveawschoolunch/Jenkinsfile

pipeline {
    agent any // Jenkins가 가능한 아무 작업 컴퓨터에서나 이 파이프라인을 실행

    stages {
        stage('Checkout') {
            steps {
                // GitHub에서 소스 코드를 가져오는 단계
                git branch: 'main', credentialsId: 'github-username-pat', url: 'https://github.com/vanillaturtlechips/iloveawschoolunch.git'
            }
        }
        stage('Build Frontend') {
            steps {
                // 'frontend' 디렉토리 안에서 명령어를 실행
                dir('frontend') {
                    // Node.js v20.11.0 버전을 사용하도록 설정 (Jenkins 서버에 설치됨)
                    tool name: 'node-20', type: 'nodejs'
                    // npm install 과 npm run build 스크립트를 실행
                    sh 'npm install'
                    sh 'npm run build'
                }
            }
        }
    }
}