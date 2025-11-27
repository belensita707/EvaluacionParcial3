pipeline {
    agent any
    environment {
        SONARQUBE = 'Sonar-Server'
        DEP_CHECK_PATH = "${WORKSPACE}/dependency-check-report"
        TARGET_URL = "http://mysql-db:5000/" 
    }
    stages {
        stage('Checkout') {
            steps {
		echo "Descargando código desde GitHub..."
        checkout scm                
            }
        }
        stage('Instalar Dependencias') {
            steps {
                sh 'pip install -r requirements.txt || echo "Pip no encontrado, saltando..."'
            }
        }
        stage('SonarQube Analysis') {
            steps {
                script {
                    def scannerHome = tool 'SonarScanner'
                    withSonarQubeEnv('Sonar-Server') {
                        sh 'pip install -r requirements.txt --break-system-packages || echo "Advertencia: Error en pip, continuando..."'
                    }
                }
            }
        }
        stage('OWASP Dependency-Check') {
            steps {
               dependencyCheck additionalArguments: '--format HTML --format XML', odcInstallation: 'Default Dependency-Check'
            }
            post {
                always {
                    publishHTML([allowMissing: true, alwaysLinkToLastBuild: true, keepAll: true, reportDir: '.', reportFiles: 'dependency-check-report.html', reportName: 'Dependency-Check Report'])
                }
            }
        }
    }
}

