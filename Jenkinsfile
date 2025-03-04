pipeline {
    agent any
    environment {
        VENV_PATH = 'venv'  // Virtual environment path
    }
    stages {
        stage('Clone Repository') {
            steps {
                git 'https://github.com/your-username/your-repo.git'
            }
        }
        stage('Setup Virtual Environment') {
            steps {
                sh 'python3 -m venv $VENV_PATH'
                sh 'source $VENV_PATH/bin/activate && pip install -r requirements.txt'
            }
        }
        stage('Run FastAPI App') {
            steps {
                sh 'source $VENV_PATH/bin/activate && nohup python main.py &'
            }
        }
    }
}
