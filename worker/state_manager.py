import requests
from config import API_URL

def set_state(job_id,state,error=None):
    try:
        r=requests.post(
            f"{API_URL}/jobs/{job_id}/status",
            params={
                "status":state,
                "pid":0
            },
            timeout=5
        )

        print(
            "STATE",
            job_id,
            state,
            r.text
        )

        if error:
            print(
                "ERROR:",
                error
            )

    except Exception as e:
        print(
            "STATE UPDATE ERROR",
            e
        )
