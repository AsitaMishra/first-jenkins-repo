pipeline{
    agent any

    environment{
        VENV = 'VENV'
        GCP_PROJECT = credentials('gcp-project')
        LOCATION = credentials('location')
        CONTAINER = '${LOCATION}-docker.pkg.dev/$(GCP_PROJECT}/jtest/jt'
    }

    stages{
        stage('Clone To Repository'){
            steps{
                echo 'Cloning To Repository'
                checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'jenkins-git-token', url: 'https://github.com/AsitaMishra/jenkins-mlf.git']])
            }
        }
        stage('Create Venv'){
            steps{
                echo 'Creating Venv'
                sh'''
                python3 -m venv ${VENV}
                source ${VENV}/bin/activate
                '''
            }
        }
        stage('Building And Pushing Docker Image To Registry'){
            steps{
                withCredentials([file(credentialsId: 'gcp-key', var: 'GOOGLE_APPLCATION_CREDENTIALS')]){
                    echo 'Pushing To Artifact Registry'
                    sh '''
                    gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}

                    gcloud config set project ${GCP_PROJECT}

                    gcloud builds submit -t ${CONTAINER}
                    '''
                }
            }
        }
        stage('Deploy To Cloud Run'){
            steps{
                withCredentials([file(credentialsId: 'gcp-key', var: 'GOOGLE_APPLCATION_CREDENTIALS')]){
                    echo 'Deploying Image To Cloud Run'
                    sh '''
                    gcloud run deploy --region ${LOCATION} --container ${CONTAINER}
                    '''
                }
            }
        }
    }
}