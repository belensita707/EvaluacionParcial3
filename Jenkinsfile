pipeline {
    agent any

    environment {
        SONARQUBE = 'Sonar-Server'
        DEP_CHECK_PATH = "${WORKSPACE}/dependency-check-report"
        TARGET_URL = "http://sonarqube:9000" 
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Instalar Dependencias') {
            steps {
                echo "Instalando dependencias de Python..."
                sh 'pip install -r requirements.txt --break-system-packages || echo "Advertencia: Hubo un problema con pip, pero intentaremos continuar..."'
            }
        }

        stage('SonarQube Analysis') {
            steps {
                script {
                    def scannerHome = tool 'SonarScanner'
                    withSonarQubeEnv('Sonar-Server') {
                        sh "${scannerHome}/bin/sonar-scanner -Dsonar.projectKey=ExamenParcial3 -Dsonar.sources=. -Dsonar.python.version=3"
                    }
                }
            }
        }

        stage('OWASP Dependency-Check') {
            steps {
                // AGREGAMOS --noupdate para que no descargue la BD gigante y no se reinicie Jenkins
                dependencyCheck additionalArguments: '--format HTML --format XML --noupdate', odcInstallation: 'Default Dependency-Check'
            }
            post {
                always {
                    publishHTML([allowMissing: true, alwaysLinkToLastBuild: true, keepAll: true, reportDir: '.', reportFiles: 'dependency-check-report.html', reportName: 'Dependency-Check Report'])
                }
            }
        }
        
        stage('OWASP ZAP (DAST Scan)') {
            steps {
                // Escaneo dinámico
                sh '''
                docker run --network="red-examen" --rm \
                zaproxy/zap-stable zap-baseline.py \
                -t http://mysql-db:5000/ \
                -r zap_report.html || true
                '''
            }
            post {
                always {
                    publishHTML([allowMissing: true, alwaysLinkToLastBuild: true, keepAll: true, reportDir: '.', reportFiles: 'zap_report.html', reportName: 'OWASP ZAP Security Report'])
                }
            }
        }
    }
}
