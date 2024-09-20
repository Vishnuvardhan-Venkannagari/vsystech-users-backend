#!/bin/bash
cwd=`pwd`
BASEDIR=`pwd`
PYTHON_PATH="/opt/env/bin/python"

prepareforUpdate() {
    cd $BASEDIR
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
    if [ ! -d /opt/backend/adminportal ]; then
          mkdir -p /opt/socialswag/adminportal
    fi
}

updateCode() {
    cd $BASEDIR
    if [ ! -d /opt/ ]; then
        mkdir /opt
    fi
    rsync -aSP $BASEDIR/vsystech-users-backend/backend/framwork /opt/backend/framework/ --delete
    rsync -aSP $BASEDIR/vsystech-users-backend/backend/application /opt/backend/application/ --delete --exclude .env
    # rsync -aSP $BASEDIR/opt/socialswag/adminportal/ /opt/socialswag/adminportal/ --delete --exclude .env
   
    # if [ ! -f /opt/socialswag/integrations/.env ]; then
        # ln -sf /opt/socialswag/adminportal/.env /opt/socialswag/integrations/.env
    # fi
    # cd $BASEDIR
    # rsync -aS etc/systemd/system/* /etc/systemd/system/ --exclude keycloak.service
    # systemctl daemon-reload
}

configureframework() {
    cd /opt/backend/framework
    $PYTHON_PATH -m pip install -e .
    $PYTHON_PATH -m pip install .
}

restartServices() {
    # for id in {8090..8099..1}
    # do
    #     echo "Restarting socialswagapi@$id.service"
    #     systemctl enable socialswagapi@$id.service
    #     systemctl restart socialswagapi@$id.service
    #     sleep 3
    # done
    # for id in {8070..8079..1}
    # do
    #     echo "Restarting adminportalapi@$id.service"
    #     systemctl enable adminportalapi@$id.service
    #     systemctl restart adminportalapi@$id.service
    #     sleep 3
    # done
    # sleep 5
    systemctl enable backend.service
    systemctl restart backend.service
    sleep 5
}


prepareforUpdate
updateCode
configureframework
restartServices
#
