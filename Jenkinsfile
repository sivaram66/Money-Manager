pipeline {
  agent any

  parameters {
    booleanParam(
      name: 'BUILD_IMAGES',
      defaultValue: true,
      description: 'Build Docker images?'
    )
    booleanParam(
      name: 'PUSH_IMAGES',
      defaultValue: true,
      description: 'Push Docker images to Docker Hub?'
    )
  }

    environment {
        DOCKER_IMAGE_NAME = 'sivaram66/money-manager'
        DOCKER_IMAGE_TAG = "$DOCKER_IMAGE_NAME:latest"
        DOCKER_HUB_CREDENTIALS = 'dockerhub-sivaram66'  // Name of the credentials ID
    }

  stages {
    stage('Clean Workspace') {
      steps {
        script {
          deleteDir()
        }
      }
    }
    stage('Checkout') {
      steps {
        git(
          url: 'https://github.com/sivaram66/Money-Manager',
          branch: 'main',
          credentialsId: 'github-credentials'
        )
        script {
          // Set the GIT_COMMIT environment variable to the short hash of the current commit
          env.GIT_COMMIT = sh(script: "git rev-parse --short HEAD", returnStdout: true).trim()
        }
      }
    }

    stage('Build Docker Images') {
      when {
        expression { params.BUILD_IMAGES }
      }
      steps {
        script {
          sh "docker-compose build --no-cache"
        }
      }
    }

    stage('Push to Docker Hub') {
      when {
        expression { params.PUSH_IMAGES }
      }
      steps {
        script {
          // Log in to Docker Hub
          withCredentials([usernamePassword(
            credentialsId: 'Docker-credentials',
            usernameVariable: 'DOCKERHUB_USERNAME',
            passwordVariable: 'DOCKERHUB_PASSWORD'
          )]) {
            sh "echo ${DOCKERHUB_PASSWORD} | docker login -u ${DOCKERHUB_USERNAME} --password-stdin"

            // Push frontend images
            sh "docker push sivaram66/money-manager:latest"
          }
        }
      }
    }
    stage('Deploy Docker Containers') {
      steps {
        script {
          withCredentials([file(credentialsId: 'env-file', variable: 'SECRET_ENV')]) {
            sh '''
                cp "$SECRET_ENV" .env
              '''
          }
        }
        sh "docker compose down --rmi all --volumes"
        sh "docker-compose up -d --force-recreate"
      }
    }
  }
}