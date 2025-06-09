pipeline {
    agent any

    environment {
        VENV_DIR = 'venv'
    }

    stages {
        stage('Checkout Code') {
            steps {
                git 'https://github.com/murangomike/Insurance-Claim-Clusters-ETL-JENKINS.git'
            }
        }

        stage('Set up Python Environment') {
            steps {
                sh '''
                    python3 -m venv $VENV_DIR
                    source $VENV_DIR/bin/activate
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            when {
                expression { fileExists('tests') }
            }
            steps {
                sh '''
                    source $VENV_DIR/bin/activate
                    pytest tests/
                '''
            }
        }

        stage('Run App') {
            steps {
                sh '''
                    source $VENV_DIR/bin/activate
                    nohup python app.py &
                '''
            }
        }
    }

    post {
        success {
            echo '✅ Deployment successful!'
        }
        failure {
            echo '❌ Something failed.'
        }
    }
}
