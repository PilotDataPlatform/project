pipeline {

    agent { label 'small' }

    environment {
        imagename = 'ghcr.io/pilotdataplatform/project'
        commit = sh(returnStdout: true, script: 'git describe --always').trim()
        registryCredential = 'pilot-ghcr'
    }

    stages {

        stage('DEV: Git clone') {
            when { branch 'develop' }
            steps {
                git branch: 'develop',
                    url: 'https://github.com/PilotDataPlatform/project.git',
                    credentialsId: 'pilot-gh'
            }
        }

        stage('DEV: Build and push image') {
            when { branch 'develop' }
            steps {
                script {
                    docker.withRegistry('https://ghcr.io', registryCredential) {
                        customImage = docker.build('$imagename:$commit')
                        customImage.push()
                    }
                }
            }
        }

        stage('DEV: Remove image') {
            when { branch 'develop' }
            steps {
                sh 'docker rmi $imagename:$commit'
            }
        }

    }

}
