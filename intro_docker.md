# Ref: https://docs.docker.com/get-started/

# Setting-up
- sudo apt-get install apt-transport-https ca-certificates curl gnupg-agent software-properties-common
- curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
- sudo apt-key fingerprint 0EBFCD88
- sudo add-apt-repository    "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"
- sudo apt-get update
- sudo apt-get install docker-ce docker-ce-cli containerd.io
- apt-cache madison docker-ce # just see available docker images
- sudo docker run hello-world # run hello world docker oimage

# Taste little-bit
- lsb_release -a # Check ubuntu version
- docker --version
- sudo docker run hello-world
- sudo docker image ls # show local docker images
- image vs container: https://stackoverflow.com/questions/23735149/what-is-the-difference-between-a-docker-image-and-a-container
 - image: recipe
 - container: cake
- remove all untagged images
 - docker images -q --filter "dangling=true" | xargs docker rmi
- remove stopped containers
 - docker rm `docker ps --no-trunc -aq`
