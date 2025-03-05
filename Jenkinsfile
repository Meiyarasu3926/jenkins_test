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
                pkill -f "python3 main.py" || true
                
                # Start the app in the background with nohup
                nohup python3 main.py $APP_PORT > app.log 2>&1 &
                
                # Store the PID
                echo $! > app.pid
                
                # Wait for the app to start
                sleep 20
                
                # Check if the process is running
                max_attempts=5
                attempt=0
                success=false
                
                while [ $attempt -lt $max_attempts ]; do
                    if ps -p $(cat app.pid) > /dev/null; then
                        # Perform health check
                        response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:$APP_PORT/health)
                        if [ "$response" = "200" ]; then
                            echo "Health check successful"
                            success=true
                            break
                        fi
                    fi
                    
                    echo "Attempt $((attempt+1))/$max_attempts failed"
                    sleep 5
                    attempt=$((attempt+1))
                done
                
                if [ "$success" != "true" ]; then
                    echo "Failed to start application"
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
