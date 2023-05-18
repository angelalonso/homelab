# Home Lab Applications

This folder includes all client-dedicated applications that will run on the cluster.

## How to deploy

So far, apart from the notes about Docker below, there is nothing in place.

## Automatic deployment (I don't trust myself calling this CD)
Locally:
- Work in a Git branch
- Test script should update a file called VERSION automatically
- Merge branch to master

On the compiler machine:
- Check for changes on the git repo
[ $(git rev-parse HEAD) = $(git ls-remote $(git rev-parse --abbrev-ref @{u} | \
sed 's/\// /g') | cut -f1) ] && echo up to date || echo not up to date
- Test the code
- Build image, add new tag, push to docker hub
docker build . -t <account>/<repo>:<version>
docker push <account>/<repo>:<version>

On the Management machine:
- Check for the newest build
- Bring new container up
- Test the new container
- Send traffic to the new container
- Change current version globally, to scale up based on it
- delete old container(s)

## Build 

docker build -t ${APP} .

## Tag

docker tag ${IMAGEID} ${USERNAME}/${REPO}:${VERSION}
docker push  ${USERNAME}/${REPO}:${VERSION}


## Run

docker run -it -p ${HOSTPORT}:${DOCKERPORT} ${APP}


