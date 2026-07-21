from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import engine, SessionLocal, Base
from models import Project, User
from pydantic import BaseModel
from auth import hash_password, verify_password, create_token, get_current_user

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="NONO API",
    version="0.1.0"
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def home():
    return {
        "name": "NONO",
        "status": "online"
    }

@app.post("/projects")
def create_project(
    name: str,
    runtime: str,
    repo: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    project = Project(
        name=name,
        runtime=runtime,
        repo=repo,
        user_id=current_user["user_id"],
        status="pending",
    )

    db.add(project)
    db.commit()
    db.refresh(project)

    return {
        "id": project.id,
        "name": project.name,
        "status": project.status
    }


@app.get("/projects")
def list_projects(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    return db.query(Project).filter(
        Project.user_id == current_user["user_id"]
    ).all()


@app.get("/jobs")
def get_jobs(db: Session = Depends(get_db)):
    return db.query(Project).filter(Project.status=="pending").all()

@app.post("/jobs/{job_id}/claim")
def claim_job(job_id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == job_id).first()

    if not project:
        return {"error": "project not found"}

    if project.status != "pending":
        return {"error": "already claimed"}

    project.status = "running"
    db.commit()

    return {
        "id": project.id,
        "status": project.status
    }

@app.post("/jobs/{job_id}/complete")
def complete_job(job_id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == job_id).first()

    if not project:
        return {"error": "project not found"}

    project.status = "completed"
    db.commit()

    return {
        "id": project.id,
        "status": project.status
    }


@app.get("/processes")
def get_processes():
    import json

    try:
        with open("data/processes.json") as f:
            return json.load(f)

    except Exception as e:
        return {
            "error": str(e)
        }


@app.get("/projects/{project_id}/logs")
def get_logs(project_id: int):

    import os

    log_file = f"/home/jeet/nono/runner/logs/{project_id}.log"

    if not os.path.exists(log_file):
        return {
            "logs": ""
        }

    with open(log_file) as f:
        return {
            "logs": f.read()
        }


@app.get("/projects/{project_id}/status")
def project_status(project_id: int):

    import json

    try:
        with open("data/processes.json") as f:
            processes = json.load(f)

        pid_data = processes.get(str(project_id))

        if not pid_data:
            return {
                "id": project_id,
                "status": "not_running"
            }

        return {
            "id": project_id,
            "pid": pid_data["pid"],
            "runtime": pid_data["runtime"],
            "status": pid_data["status"]
        }

    except Exception as e:
        return {
            "error": str(e)
        }


@app.post("/projects/{project_id}/stop")
def stop_project(project_id: int):

    import json
    import os
    import signal

    file="/home/jeet/nono/runner/processes.json"

    try:
        with open(file) as f:
            data=json.load(f)

        pid_data=data.get(str(project_id))

        if not pid_data:
            return {"error":"process not found"}

        pid=pid_data["pid"]

        os.kill(pid, signal.SIGTERM)

        pid_data["status"]="stopped"

        with open(file,"w") as f:
            json.dump(data,f,indent=2)

        return {
            "id":project_id,
            "status":"stopped"
        }

    except Exception as e:
        return {"error":str(e)}
@app.get("/projects/{project_id}/resources")
def project_resources(project_id: int):
    import json

    file="/home/jeet/nono/runner/processes.json"

    try:
        with open(file) as f:
            data=json.load(f)

        project=data.get(str(project_id))

        if not project:
            return {
                "error":"process not found"
            }

        return {
            "id": project_id,
            "status": project.get("status"),
            "ram_mb": project.get("ram_mb",0),
            "ram_limit_mb": project.get("limit_ram_mb",512),
            "cpu_percent": project.get("cpu_percent",0),
            "cpu_limit_percent": project.get("limit_cpu_percent",50)
        }

    except Exception as e:
        return {
            "error":str(e)
        }
@app.get("/projects/{project_id}/dashboard")
def project_dashboard(project_id: int):

    import json
    import os
    process_file="/home/jeet/nono/runner/processes.json"
    log_file=f"/home/jeet/nono/runner/logs/{project_id}.log"

    try:

        with open(process_file) as f:
            processes=json.load(f)

        project=processes.get(str(project_id))

        if not project:
            return {"error":"project not found"}

        logs=""

        if os.path.exists(log_file):
            with open(log_file) as f:
                logs="\n".join(f.readlines()[-100:])


        return {
            "id": project_id,
            "status": project.get("status"),
            "runtime": project.get("runtime"),

            "resources":{
                "ram_mb":project.get("ram_mb",0),
                "ram_limit_mb":project.get("limit_ram_mb",512),
                "cpu_percent":project.get("cpu_percent",0),
                "cpu_limit_percent":project.get("limit_cpu_percent",50)
            },

            "logs":logs,

            "controls":{
                "stop":True,
                "restart":True
            }
        }

    except Exception as e:
        return {"error":str(e)}
@app.post("/projects/sync")
def sync_projects(db: Session = Depends(get_db)):
    import json
    import os

    process_file = "/home/jeet/nono/runner/processes.json"

    if not os.path.exists(process_file):
        return {"error": "process file not found"}

    with open(process_file) as f:
        processes = json.load(f)

    projects = db.query(Project).all()

    updated = 0

    for project in projects:
        pdata = processes.get(str(project.id))

        if pdata:
            project.status = pdata.get("status", project.status)
            updated += 1

    db.commit()

    return {
        "success": True,
        "updated": updated
    }


class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str


class LoginRequest(BaseModel):
    username: str
    password: str



@app.post("/register")
def register(
    data: RegisterRequest,
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.username == data.username
    ).first()

    if user:
        return {
            "error":"username already exists"
        }


    new_user = User(
        username=data.username,
        email=data.email,
        password=hash_password(data.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)


    return {
        "message":"user created",
        "id":new_user.id
    }



@app.post("/login")
def login(
    data: LoginRequest,
    db: Session = Depends(get_db)
):

    user=db.query(User).filter(
        User.username == data.username
    ).first()


    if not user:
        return {
            "error":"user not found"
        }


    if not verify_password(
        data.password,
        user.password
    ):
        return {
            "error":"wrong password"
        }


    token=create_token({
        "user_id":user.id,
        "username":user.username
    })


    return {
        "access_token":token,
        "token_type":"bearer"
    }
