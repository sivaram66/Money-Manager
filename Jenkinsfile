pipeline {
  agent any

  environment {
    IMAGE      = "sivaram66/money-manager"
    REGISTRY   = "https://registry.hub.docker.com"
    CRED_ID    = "docker-hub-creds"       // define in Jenkins
  }

  stages {
    stage('Checkout') {
      steps { checkout scm }
    }

    stage('Build Image') {
      steps {
        script {
          dockerImage = docker.build("${IMAGE}:${env.BUILD_NUMBER}")
        }
      }
    }

    stage('Run Tests') {
      steps {
        script {
          dockerImage.inside {
            sh 'python manage.py test --failfast'
          }
        }
      }
    }

    stage('Push to Docker Hub') {
      when { branch 'main' }
      steps {
        withCredentials([usernamePassword(credentialsId: env.CRED_ID,
                                          usernameVariable: 'DOCKER_USER',
                                          passwordVariable: 'DOCKER_PASS')]) {
          script {
            docker.withRegistry(env.REGISTRY, env.CRED_ID) {
              dockerImage.push('latest')
              dockerImage.push("${env.BUILD_NUMBER}")
            }
          }
        }
      }
    }

    stage('Deploy with Compose') {
      steps {
        sh 'docker-compose down'
        sh 'docker-compose up -d --build'
      }
    }
  }
}