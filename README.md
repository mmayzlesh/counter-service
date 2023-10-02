# counter-service
Counts POST requests, returns count on GET request.

## Overview
This repository contains the source code and configuration files for a Counter Service. The service consists of three components: a custom Counter Service, Redis, and Nginx.

- **Counter Service**: A Python service that counts ```POST``` requests sent to the service and displays the count on ```GET``` requests.
- **Redis**: Utilized as an in-memory data store, persisted on a named mount on the host.
- **Nginx**: Serves as a reverse proxy to handle requests and forward them to the Counter Service.

## Repository Structure
```
├────── .github - Github actions folder
├────── nginx - Nginx configuration folder
├────── redis - Redis configuration folder
├── Dockerfile - Dockerfile for counter-service
├── counter_service.py - Main counter-service functionality
├── requirements.txt - counter-service dependencies, restored at build time
└── docker-compose.yml - Docker Compose file to orchestrate the services
```

## Prerequisites
- Docker
- Docker Compose

## CI/CD
GitHub Actions take care of the CI/CD process, which ultimately deploys to a remote host.

The remote host's address, username, and SSH key are defined as GitHub Actions Secrets for the repository.

Each push to the ```main``` branch will automatically trigger a GitHub Actions pipeline, which does the following:

1. Clones the repository.
2. Builds the counter-service Docker image based on the Dockerfile.
3. Pushes the created Docker image to the GitHub Container Registry, tagged with the branch name and GitHub Actions run number, in addition to a latest tag.
4. Copies the relevant files to the destination VM.
5. Sets Nginx and Redis configuration files in defined bind mounts on the destination VM.
6. Pulls and starts all the services using docker-compose.

Each push to a non-```main``` branch will automatically trigger a GitHub Actions pipeline, which does the following:

1. Clones the repository.
2. Builds the counter-service Docker image based on the Dockerfile.
3. Pushes the created Docker image to the GitHub Container Registry, tagged with the branch name and GitHub Actions run number.
- No deployment is performed for non-main brnahces.

## Manual Installation

To deploy the service manually, follow the steps below:

**1. Clone the Repository:**
   ```sh
   git clone [Repository URL]
   cd [Repository Name]
   ```

**2. Copy configuration files:**

Within the application directory, copy configuration files to defined bind mounts:
```
cp ./nginx/nginx.conf /etc/nginx/nginx.conf
cp ./redis/redis.conf /usr/local/etc/redis/redis.conf
```

**3. Pull latest image and start services** 
```
docker compose pull
docker compose up -d
```

## Rollback

If you need to revert to a previous version of the service due to any issue with the latest version, you can do so by modifying the `docker-compose.yml` file on the host machine.

### Steps
1. Open `docker-compose.yml` in a text editor.

2. Locate the `image` attribute under the `counter-service` service definition.

3. Replace the `latest` tag or the existing tag with the tag of the desired version:

   ```yaml
   image: ghcr.io/mmayzlesh/counter-service:<desired version>
   ```
4. Save the file and exit the text editor.

5. Navigate to the directory containing the docker-compose.yml file and run:
   ```yaml
   docker-compose up -d
   ```
   This command will stop the running service and start it again with the specified image version, thus rolling back to the older, desired version of the service.
