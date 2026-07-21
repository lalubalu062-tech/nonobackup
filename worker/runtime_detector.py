import os


def detect_runtime(app_dir):

    files=os.listdir(app_dir)


    # Docker first
    if "Dockerfile" in files:
        return {
            "runtime":"docker",
            "command":"docker build ."
        }


    # Node
    if "package.json" in files:

        if "server.js" in files:
            cmd="node server.js"

        elif "app.js" in files:
            cmd="node app.js"

        else:
            cmd="npm start"


        return {
            "runtime":"node",
            "command":cmd
        }


    # Python

    if "main.py" in files:
        return {
            "runtime":"python",
            "command":"python3 -u main.py"
        }


    if "app.py" in files:
        return {
            "runtime":"python",
            "command":"python3 -u app.py"
        }


    if "server.py" in files:
        return {
            "runtime":"python",
            "command":"python3 -u server.py"
        }


    return {
        "runtime":"unknown",
        "command":None
    }
