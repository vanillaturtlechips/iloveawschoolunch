// iloveawschoolunch/Jenkinsfile

pipeline {
    agent any
    
    stages {
        stage('Checkout') {
            steps {
                // 이 부분은 GitHub에서 코드를 가져오는 기본 단계입니다.
                // Jenkins가 자동으로 처리해주므로 직접 쓸 필요가 없습니다.
                // 혼란을 줄이기 위해 이 부분은 삭제하고 아래처럼 단순화합니다.
                checkout scm
            }
        }
        stage('Build Frontend') {
            // "이 stage를 시작하기 전에 'node-20'이라는 NodeJS 도구를 준비해줘"
            tools {
                nodejs 'node-20'
            }
            steps {
                // 'frontend' 디렉토리 안에서 명령어를 실행
                dir('frontend') {
                    // 이제 Jenkins는 npm 명령어가 어디 있는지 알고 있습니다.
                    sh 'npm install'
                    sh 'npm run build'
                }
            }
        }
    }
}