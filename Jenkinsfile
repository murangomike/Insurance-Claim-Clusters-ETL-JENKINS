pipeline {
    agent any

    environment {
        VENV_DIR = 'venv'
    }

    stages {
        stage('Checkout Code') {
            steps {
                echo '🔄 Cloning repository...'
                git 'https://github.com/murangomike/Insurance-Claim-Clusters-ETL-JENKINS.git'
            }
        }

        stage('Install System Dependencies') {
            environment {
                SUDO_PASSWORD = '@2021'
            }
            steps {
                echo '🔧 Installing system packages...'
                sh '''
                    echo "$SUDO_PASSWORD" | sudo -S apt-get update -y
                    echo "$SUDO_PASSWORD" | sudo -S apt-get install -y \
                        build-essential gcc g++ python3-dev \
                        libblas-dev liblapack-dev libatlas-base-dev gfortran
                '''
            }
        }

        stage('Set Up Python Environment') {
            steps {
                echo '🐍 Setting up Python virtual environment...'
                sh '''
                    python3 -m venv $VENV_DIR
                    . $VENV_DIR/bin/activate

                    pip install --upgrade pip setuptools wheel

                    pip install Flask==2.3.3 Flask-CORS==4.0.0

                    pip install --only-binary=all scikit-learn==1.3.0 || pip install scikit-learn==1.3.0

                    [ -f requirements.txt ] && pip install -r requirements.txt
                '''
            }
        }

        stage('Verify Installation') {
            steps {
                echo '🔍 Verifying package installation...'
                sh '''
                    . $VENV_DIR/bin/activate
                    python -c "import flask; print('✅ Flask:', flask.__version__)"
                    python -c "import sklearn; print('✅ scikit-learn:', sklearn.__version__)"
                    python -c "import flask_cors; print('✅ Flask-CORS imported successfully')"
                '''
            }
        }

        stage('Run Tests') {
            when {
                expression { fileExists('tests') }
            }
            steps {
                echo '🧪 Running tests...'
                sh '''
                    . $VENV_DIR/bin/activate
                    if ! command -v pytest > /dev/null; then
                        pip install pytest
                    fi
                    pytest tests/
                '''
            }
        }

        stage('Run App') {
            steps {
                echo '🚀 Launching application...'
                sh '''
                    . $VENV_DIR/bin/activate

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
                        echo "❌ Failed to start the app. See logs below:"
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
                . $VENV_DIR/bin/activate
                echo "📦 Installed packages:"
                pip list
            '''
        }
        failure {
            echo '❌ Build failed. Debug logs:'
            sh '''
                [ -f app.log ] && cat app.log || echo "No app.log found."
            '''
        }
    }
}
