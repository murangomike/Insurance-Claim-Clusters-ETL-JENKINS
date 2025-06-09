pipeline {
    agent {
        docker {
            image 'python:3.11-slim'
            args '-u root'  // runs container as root so `apt-get` works without sudo
        }
    }

    environment {
        VENV_DIR = 'venv'
    }

    stages {
        stage('Checkout Code') {
            steps {
                echo '🔄 Cloning repository...'
                git url: 'https://github.com/murangomike/Insurance-Claim-Clusters-ETL-JENKINS.git'
            }
        }

        stage('Install System Dependencies') {
            steps {
                echo '🔧 Installing system packages...'
                sh '''
                    apt-get update -y
                    apt-get install -y build-essential gcc g++ python3-dev \
                        libblas-dev liblapack-dev libatlas-base-dev gfortran
                '''
            }
        }

        stage('Set Up Python Environment') {
            steps {
                echo '🐍 Setting up Python virtual environment...'
                sh '''
                    python3 -m venv "$VENV_DIR"
                    . "$VENV_DIR/bin/activate"

                    pip install --upgrade pip setuptools wheel
                    pip install Flask==2.3.3 Flask-CORS==4.0.0
                    pip install --only-binary=all scikit-learn==1.3.0 || pip install scikit-learn==1.3.0

                    [ -f requirements.txt ] && pip install -r requirements.txt
                '''
            }
        }

        stage('Verify Installation') {
            steps {
                echo '🔍 Verifying packages...'
                sh '''
                    . "$VENV_DIR/bin/activate"
                    python -c "import flask; print('✅ Flask:', flask.__version__)"
                    python -c "import sklearn; print('✅ scikit-learn:', sklearn.__version__)"
                    python -c "import flask_cors; print('✅ Flask-CORS imported successfully')"
                '''
            }
        }

        stage('Run Tests') {
            when {
                expression { return fileExists('tests') }
            }
            steps {
                echo '🧪 Running tests...'
                sh '''
                    . "$VENV_DIR/bin/activate"
                    command -v pytest >/dev/null || pip install pytest
                    pytest tests/
                '''
            }
        }

        stage('Run App') {
            steps {
                echo '🚀 Launching app...'
                sh '''
                    . "$VENV_DIR/bin/activate"

                    if [ ! -f app.py ]; then
                        echo "❌ app.py not found!"
                        ls -la
                        exit 1
                    fi

                    nohup python app.py > app.log 2>&1 &
                    echo $! > app.pid
                    sleep 3

                    if ps -p $(cat app.pid) > /dev/null; then
                        echo "✅ App started with PID $(cat app.pid)"
                    else
                        echo "❌ App failed to start. Logs:"
                        cat app.log
                        exit 1
                    fi
                '''
            }
        }
    }

    post {
        always {
            echo '🧹 Cleaning up...'
            sh '''
                if [ -f app.pid ]; then
                    PID=$(cat app.pid)
                    if ps -p $PID > /dev/null; then
                        kill $PID || true
                    fi
                    rm -f app.pid
                fi
            '''
        }

        success {
            echo '✅ Deployment successful!'
            sh '''
                . "$VENV_DIR/bin/activate"
                pip list
            '''
        }

        failure {
            echo '❌ Build failed. Dumping app logs:'
            sh '''
                [ -f app.log ] && cat app.log || echo "No app.log found."
            '''
        }
    }
}
