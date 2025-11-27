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
                // Aquí usamos el comando con el desbloqueo de sistema
                sh 'pip install -r requirements.txt --break-system-packages || echo "Advertencia: Hubo un problema con pip, pero intentaremos continuar..."'
            }
        }

        stage('SonarQube Analysis') {
            steps {
                script {
                    def scannerHome = tool 'SonarScanner'
                    withSonarQubeEnv('Sonar-Server') {
                        // Este es el comando que faltaba para analizar el código
                        sh "${scannerHome}/bin/sonar-scanner -Dsonar.projectKey=ExamenParcial3 -Dsonar.sources=. -Dsonar.python.version=3"
                    }
                }
            }
        }

        stage('OWASP Dependency-Check') {
            steps {
                // Este paso falló antes porque el nombre de la herramienta no coincidía
                dependencyCheck additionalArguments: '--format HTML --format XML', odcInstallation: 'Default Dependency-Check'
            }
            post {
                always {
                    publishHTML([allowMissing: true, alwaysLinkToLastBuild: true, keepAll: true, reportDir: '.', reportFiles: 'dependency-check-report.html', reportName: 'Dependency-Check Report'])
                }
            }
        }
        
        stage('OWASP ZAP (DAST Scan)') {
            steps {
                // Escaneo dinámico (ignoramos error si encuentra vulnerabilidades, que es la idea)
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
