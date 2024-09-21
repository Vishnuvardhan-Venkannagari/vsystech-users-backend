#!/bin/bash
cwd=`pwd`
BASEDIR=`pwd`
PYTHON_PATH="/opt/env/bin/python"

prepareforUpdate() {
    cd $BASEDIR
    git pull origin dev
    $PYTHON_PATH -m pip install -r requirements.txt
    if [ ! -d /var/log/application/ ]; then
        mkdir -p /var/log/application/
    fi
    if [ ! -d /var/log/application/ ]; then
          mkdir -p /var/log/application/
    fi
    if [ ! -d /opt/backend/application ]; then
          mkdir -p /opt/backend/application
    fi
}

updateCode() {
    cd $BASEDIR
    if [ ! -d /opt/ ]; then
        mkdir /opt
    fi
    rsync -aSP $BASEDIR/framework/ /opt/backend/framework/ --delete
    rsync -aSP $BASEDIR/application/ /opt/backend/application/ --delete --exclude .env
    # rsync -aSP $BASEDIR/opt/socialswag/adminportal/ /opt/socialswag/adminportal/ --delete --exclude .env
   
    # if [ ! -f /opt/socialswag/integrations/.env ]; then
        # ln -sf /opt/socialswag/adminportal/.env /opt/socialswag/integrations/.env
    # fi
    # cd $BASEDIR
    # rsync -aS etc/systemd/system/* /etc/systemd/system/ --exclude keycloak.service
    # systemctl daemon-reload
}

configureframework() {
    cd /opt/backend/framework/
    $PYTHON_PATH -m pip install -e .
    $PYTHON_PATH -m pip install .
}

restartServices() {
    sudo systemctl enable backend.service
    sudo systemctl restart backend.service
    sleep 5
}


prepareforUpdate
updateCode
configureframework
restartServices
#
