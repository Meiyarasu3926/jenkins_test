pipeline {
    agent any
    environment {
        VENV_PATH = 'venv'  // Virtual environment path
    }
    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'main', url: 'https://github.com/Meiyarasu3926/jenkins_test.git'
            }
        }
        stage('Setup Virtual Environment') {
            steps {
                sh 'python3 -m venv $VENV_PATH'
                sh '. $VENV_PATH/bin/activate && pip install -r requirements.txt'
            }
        }
        stage('Run FastAPI App') {
            steps {
                sh '. $VENV_PATH/bin/activate && nohup uvicorn main:app --host 0.0.0.0 --port 8000 &'
            }
        }
    }
}
