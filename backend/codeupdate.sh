#!/bin/bash
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
    rsync -aSP $BASEDIR/framework/ /opt/framework/ --delete
    rsync -aSP $BASEDIR/opt/socialswag/application/ /opt/socialswag/application/ --delete --exclude .env
    rsync -aSP $BASEDIR/opt/socialswag/adminportal/ /opt/socialswag/adminportal/ --delete --exclude .env
    rsync -aSP $BASEDIR/opt/socialswag/websocket/  /opt/socialswag/websocket/ --delete --exclude .env
    rsync -aSP $BASEDIR/opt/socialswag/integrations/ /opt/socialswag/integrations/ --delete --exclude .env
    rsync -aSP $BASEDIR/opt/socialswag/templates/ /opt/socialswag/templates/ --delete --exclude .env
    rsync -aSP $BASEDIR/opt/socialswag/camunda/ /opt/socialswag/camunda/ --delete --exclude .env
    rsync -aSP $BASEDIR/opt/socialswag/user_certificates/ /opt/socialswag/user_certificates/ --delete --exclude .env 
   
    if [ ! -f /opt/socialswag/integrations/.env ]; then
        ln -sf /opt/socialswag/adminportal/.env /opt/socialswag/integrations/.env
    fi
    if [ ! -f /opt/socialswag/websocket/.env ]; then
        ln -sf /opt/socialswag/adminportal/.env /opt/socialswag/websocket/.env
    fi
    cd $BASEDIR
    rsync -aS etc/systemd/system/* /etc/systemd/system/ --exclude keycloak.service
    systemctl daemon-reload
}

configureframework() {
    cd /opt/framework
    $PYTHON_PATH -m pip install -e .
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
    systemctl enable integrations.service
    systemctl restart integrations.service
    sleep 5
    systemctl enable websocket.service
    systemctl restart websocket.service
}

runMigration() {
    cd /opt/socialswag/adminportal/
    $PYTHON_PATH $BASEDIR/migrationScripts/updateDefaults.py
    $PYTHON_PATH $BASEDIR/migrationScripts/updateRoles.py
}

prepareforUpdate
updateCode
configureframework
restartServices
runMigration
#
