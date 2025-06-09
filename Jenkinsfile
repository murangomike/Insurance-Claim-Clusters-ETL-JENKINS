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

        stage('Install System Dependencies') {
            steps {
                sh '''
                    # Update package list and install build essentials
                    sudo apt-get update -y
                    sudo apt-get install -y build-essential gcc g++ python3-dev
                    
                    # Install additional dependencies that scikit-learn might need
                    sudo apt-get install -y libblas-dev liblapack-dev libatlas-base-dev gfortran
                '''
            }
        }

        stage('Set up Python Environment') {
            steps {
                sh '''
                    python3 -m venv $VENV_DIR
                    . $VENV_DIR/bin/activate
                    pip install --upgrade pip setuptools wheel
                    
                    # Install packages one by one to better handle errors
                    pip install Flask==2.3.3
                    pip install Flask-CORS==4.0.0
                    
                    # For scikit-learn, try using a pre-compiled wheel first
                    pip install --only-binary=all scikit-learn==1.3.0 || pip install scikit-learn==1.3.0
                    
                    # Alternative: install from requirements.txt if it exists
                    if [ -f requirements.txt ]; then
                        pip install -r requirements.txt
                    fi
                '''
            }
        }

        stage('Verify Installation') {
            steps {
                sh '''
                    . $VENV_DIR/bin/activate
                    python -c "import flask; print('Flask version:', flask.__version__)"
                    python -c "import sklearn; print('Scikit-learn version:', sklearn.__version__)"
                    python -c "import flask_cors; print('Flask-CORS imported successfully')"
                '''
            }
        }

        stage('Run Tests') {
            when {
                expression { fileExists('tests') }
            }
            steps {
                sh '''
                    . $VENV_DIR/bin/activate
                    if command -v pytest &> /dev/null; then
                        pytest tests/
                    else
                        echo "pytest not found, installing..."
                        pip install pytest
                        pytest tests/
                    fi
                '''
            }
        }

        stage('Run App') {
            steps {
                sh '''
                    . $VENV_DIR/bin/activate
                    # Check if app.py exists before running
                    if [ -f app.py ]; then
                        echo "Starting application..."
                        nohup python app.py > app.log 2>&1 &
                        echo $! > app.pid
                        sleep 2
                        if ps -p $(cat app.pid) > /dev/null; then
                            echo "Application started successfully with PID $(cat app.pid)"
                        else
                            echo "Failed to start application"
                            cat app.log
                            exit 1
                        fi
                    else
                        echo "app.py not found in the repository"
                        ls -la
                        exit 1
                    fi
                '''
            }
        }
    }

    post {
        always {
            sh '''
                # Clean up any running processes
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
                pip list
            '''
        }
        failure {
            echo '❌ Something failed.'
            sh '''
                # Show logs for debugging
                if [ -f app.log ]; then
                    echo "Application logs:"
                    cat app.log
                fi
            '''
        }
    }
}
