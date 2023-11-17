# install git and docker in the instance
sudo dnf in docker git

# enable the docker daemon
sudo systemctl enable --now docker

# add user to the "docker" group, and start a new shell with the permissions instantiated
sudo usermod -aG docker ec2-user
id ec2-user # reloads group assignments without relogging

# install docker compose (which isn't included)
DOCKER_CONFIG=${DOCKER_CONFIG:-$HOME/.docker}
mkdir -p $DOCKER_CONFIG/cli-plugins
curl -SL https://github.com/docker/compose/releases/download/v2.23.1/docker-compose-linux-x86_64 -o $DOCKER_CONFIG/cli-plugins/docker-compose

# give exec perms to compose
chmod +x $DOCKER_CONFIG/cli-plugins/docker-compose

# clone this repo
git clone https://github.com/cs298-398f23/file-fortress

# create a .env file in flask
touch file-fortress/flask/.env

# TODO
# launch the container in the background
# cd file-fortress && docker compose up -d
