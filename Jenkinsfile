pipeline {
    agent any
    
    environment {
        VENV_PATH = 'venv'
        APP_PORT = '8000'
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
                pkill -f "uvicorn main:app" || true
                
                # Start the app and keep it running
                nohup $VENV_PATH/bin/uvicorn main:app --host 0.0.0.0 --port $APP_PORT --workers 2 --reload > app.log 2>&1 &
                
                # Store the PID for reference
                echo $! > app.pid
                
                # Wait for the app to start
                sleep 15
                
                # Check if the process is running
                if ps -p $(cat app.pid) > /dev/null; then
                    echo "Application is running with PID $(cat app.pid)"
                    
                    # Perform a health check
                    response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:$APP_PORT/health)
                    if [ "$response" = "200" ]; then
                        echo "Health check successful"
                    else
                        echo "Health check failed with status $response"
                        cat app.log
                        exit 1
                    fi
                else
                    echo "Application failed to start"
                    cat app.log
                    exit 1
                fi
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
            sh 'cat app.log || true'
        }
        always {
            echo 'Finished pipeline execution'
        }
    }
}
