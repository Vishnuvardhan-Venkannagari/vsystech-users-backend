from inspect import indentsize
from logging import debug
import os
import sys
# import framework
import uvicorn
import argparse

sys.path.append(os.getcwd())
parser = argparse.ArgumentParser(description='Parse Model & generate code for a target language.')
parser.add_argument('-c','--config', action='store_true', help='Sample config file.')
args = parser.parse_args()

if __name__ == "__main__":
    debug: bool = False
    reload: bool = False
    port: int = int(os.environ.get("PORT", 8000))
    host: str = str(os.environ.get("HOST", "127.0.0.1"))
    if args.config:
        sys.exit(0)

    if os.environ.get("MODE", "prod") == "dev":
        debug = True
        reload = True
    uvicorn.run("restapi:app",port=port, host=host, reload=reload, reload_dirs=[os.getcwd()])#, debug=debug
