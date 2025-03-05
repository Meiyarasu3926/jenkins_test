pipeline {
    agent any
    
    environment {
        VENV_PATH = 'venv'
        APP_PORT = '8000'
        APP_HOST = '0.0.0.0'
    }
    
    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'main', url: 'https://github.com/Meiyarasu3926/jenkins_test.git'
            }
        }
        
        stage('Setup Virtual Environment') {
            steps {
                sh '''
                python3 -m venv $VENV_PATH || true
                . $VENV_PATH/bin/activate
                pip install -r requirements.txt
                pip install gunicorn  # Add gunicorn for production deployment
                '''
            }
        }
        
        stage('Run Tests') {
            steps {
                sh '. $VENV_PATH/bin/activate && echo "Running tests (placeholder)"'
            }
        }
        
        stage('Deploy FastAPI App') {
            steps {
                sh '''
                . $VENV_PATH/bin/activate
                
                # Kill any existing instances of the app
                pkill -f "gunicorn main:app" || true
                pkill -f "uvicorn main:app" || true
                
                # Start the app with Gunicorn for production
                nohup gunicorn main:app \
                    --workers 4 \
                    --worker-class uvicorn.workers.UvicornWorker \
                    --bind $APP_HOST:$APP_PORT \
                    --access-logfile app_access.log \
                    --error-logfile app_error.log \
                    --capture-output \
                    --daemon
                
                # Wait for the app to start
                sleep 10
                
                # Check if the process is running
                pgrep -f "gunicorn main:app" || {
                    echo "Application failed to start"
                    cat app_error.log
                    exit 1
                }
                
                # Perform health check
                response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:$APP_PORT/health)
                if [ "$response" != "200" ]; then
                    echo "Health check failed with status $response"
                    cat app_error.log
                    exit 1
                fi
                
                echo "Application started successfully"
                '''
            }
        }
        
        stage('Public Access Info') {
            steps {
                sh '''
                echo "Application should be running on:"
                echo "Internal URL: http://localhost:$APP_PORT"
                
                # Fetch public IP using an external service
                public_ip=$(curl -s https://api.ipify.org)
                
                echo "Public IP: $public_ip"
                echo "Full Public URL: http://$public_ip:$APP_PORT"
                
                # Create a simple info file
                echo "Application is running at: http://$public_ip:$APP_PORT" > app_info.txt
                cat app_info.txt
                '''
            }
        }
    }
    
    post {
        success {
            echo 'Pipeline completed successfully!'
            sh 'cat app_info.txt || echo "Application is running on port $APP_PORT"'
        }
        failure {
            echo 'Pipeline failed!'
            sh 'cat app_error.log || true'
        }
        always {
            echo 'Finished pipeline execution'
        }
    }
}
