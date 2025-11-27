pipeline {
    agent any

    environment {
        SONARQUBE = 'Sonar-Server' 
    
        NVD_API_KEY = credentials('nvdApiKey')
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Instalar Dependencias') {
            steps {
                echo "Instalando dependencias..."
                sh 'pip install -r requirements.txt --break-system-packages'
            }
        }

        stage('SonarQube Analysis') {
            steps {
                script {
                    def scannerHome = tool 'SonarQubeScanner'
                    withSonarQubeEnv('Sonar-Server') {
                        sh "${scannerHome}/bin/sonar-scanner -Dsonar.projectKey=ExamenParcial3 -Dsonar.sources=. -Dsonar.python.version=3"
                    }
                }
            }
        }

        stage('OWASP Dependency-Check') {
            steps {
                echo "Ejecutando análisis con API Key de NVD..."
                dependencyCheck additionalArguments: "--format HTML --format XML --nvdApiKey ${NVD_API_KEY}", odcInstallation: 'DependencyCheck'
            }
            post {
                always {
                    publishHTML([allowMissing: true, alwaysLinkToLastBuild: true, keepAll: true, reportDir: '.', reportFiles: 'dependency-check-report.html', reportName: 'Dependency-Check Report'])
                }
            }
        }
        
        stage('OWASP ZAP (DAST Scan)') {
            steps {
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
