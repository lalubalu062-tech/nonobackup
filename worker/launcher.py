import os
import json


def load_config(app_dir):

    config_file=f"{app_dir}/nono.json"

    if os.path.exists(config_file):

        try:
            with open(config_file) as f:
                data=json.load(f)

                return data

        except Exception as e:
            print(
                "NONO CONFIG ERROR:",
                e
            )


    return {}



def get_start_command(app_dir,default_cmd):

    config=load_config(app_dir)

    cmd=config.get(
        "start"
    )

    port=config.get(
        "port"
    )


    if cmd:

        print(
            "CUSTOM START:",
            cmd
        )

        return cmd,port


    return default_cmd,port
