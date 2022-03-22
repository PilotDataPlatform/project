pipeline {

    agent { label 'small' }

    stages {

        stage('DEV: Git clone') {
            when { branch 'k8s-dev' }
            steps {
                git branch: 'k8s-dev',
                    url: 'https://git.indocresearch.org/pilot/project.git',
                    credentialsId: 'lzhao'
            }
        }

    }

}
