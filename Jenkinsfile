pipeline {

    agent { label 'small' }

    environment {
        imagename = 'registry-gitlab.indocresearch.org/pilot/project'
        commit = sh(returnStdout: true, script: 'git describe --always').trim()
        registryCredential = 'pilot-gitlab-registry'
    }

    stages {

        stage('DEV: Git clone') {
            when { branch 'k8s-dev' }
            steps {
                git branch: 'k8s-dev',
                    url: 'https://git.indocresearch.org/pilot/project.git',
                    credentialsId: 'lzhao'
            }
        }

        stage('DEV: Build and push image') {
            when { branch 'k8s-dev' }
            steps {
                script {
                    docker.withRegistry('https://registry-gitlab.indocresearch.org', registryCredential) {
                        customImage = docker.build('registry-gitlab.indocresearch.org/pilot/project:$commit', '--add-host git.indocresearch.org:10.4.3.151 .')
                        customImage.push()
                    }
                }
            }
        }

        stage('DEV: Remove image') {
            when { branch 'k8s-dev' }
            steps {
                sh 'docker rmi $imagename:$commit'
            }
        }

    }

}
