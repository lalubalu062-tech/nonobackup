from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import engine, SessionLocal, Base
from models import Worker, Project, User
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

    workers=db.query(Worker).filter(
        Worker.status=="online"
    ).all()

    selected=None

    if workers:
        workers=sorted(
            workers,
            key=lambda w:(
                int(w.projects or 0),
                float(w.cpu or 0),
                float(w.ram or 0)
            )
        )
        selected=workers[0].worker_id

    project = Project(
        name=name,
        runtime=runtime,
        repo=repo,
        user_id=current_user["user_id"],
        status="pending",
        worker_id=selected
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
def get_jobs(
    worker_id:str,
    db:Session=Depends(get_db)
):
    return db.query(Project).filter(
        Project.status.in_(["pending","restarting"]),
        Project.worker_id==worker_id
    ).all()

@app.post("/jobs/{job_id}/claim")
def claim_job(
    job_id: int,
    worker_id: str,
    db: Session = Depends(get_db)
):

    from datetime import datetime, timedelta

    project=db.query(Project).filter(
        Project.id==job_id
    ).first()

    if not project:
        return {
            "error":"project not found"
        }


    if project.status not in ["pending","restarting"]:
        return {
            "error":"already claimed"
        }

    if project.status == "restarting":
        project.restart_count = (project.restart_count or 0) + 1


    worker=db.query(Worker).filter(
        Worker.worker_id==worker_id
    ).first()


    if not worker:
        return {
            "error":"worker not found"
        }


    if worker.status!="online":
        return {
            "error":"worker offline"
        }


    if worker.last_seen < datetime.utcnow()-timedelta(minutes=2):
        return {
            "error":"worker heartbeat expired"
        }


    project.status="running"
    project.worker_id=worker_id


    db.commit()
    db.refresh(project)


    return {
        "id":project.id,
        "status":project.status,
        "worker_id":project.worker_id
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



@app.get("/projects/{project_id}/status")
def project_status(project_id:int, user=Depends(get_current_user)):

    import os

    db=SessionLocal()

    project=db.query(Project).filter(
        Project.id==project_id
    ).first()

    if not project:
        return {
            "error":"not found"
        }

    alive=False

    if project.pid:
        try:
            os.kill(project.pid,0)
            alive=True
        except:
            alive=False

    return {
        "id":project.id,
        "name":project.name,
        "status": "running" if alive else "stopped",
        "pid":project.pid,
        "worker_id":project.worker_id
    }


@app.post("/jobs/{job_id}/status")
def update_job_status(
    job_id:int,
    status:str,
    pid:int=0
):
    db=SessionLocal()

    project=db.query(Project).filter(
        Project.id==job_id
    ).first()

    if not project:
        return {
            "error":"project not found"
        }

    project.status=status

    if pid:
        project.pid=pid

    db.commit()

    return {
        "id":job_id,
        "status":status,
        "pid":pid
    }

@app.post("/workers/heartbeat")
def worker_heartbeat(data: dict):

    from datetime import datetime

    db = SessionLocal()

    worker_id=data.get("worker_id")

    worker=db.query(Worker).filter(
        Worker.worker_id==worker_id
    ).first()

    if worker:

        worker.status="online"
        worker.last_seen=datetime.utcnow()
        worker.cpu=str(data.get("cpu",0))
        worker.ram=str(data.get("ram",0))
        worker.hostname=data.get("hostname")
        worker.projects=int(data.get("projects",0))

    else:

        worker=Worker(
            worker_id=worker_id,
            status="online",
            cpu=str(data.get("cpu",0)),
            ram=str(data.get("ram",0)),
            hostname=data.get("hostname"),
            projects=int(data.get("projects",0))
        )

        db.add(worker)

    db.commit()
    db.close()

    return {
        "status":"ok",
        "worker_id":worker_id
    }


@app.post("/projects/{project_id}/stop")
def stop_project(
    project_id:int,
    current_user: dict = Depends(get_current_user)
):
    import os
    import signal
    from process_manager import kill_process

    db = SessionLocal()

    project = db.query(Project).filter(
        Project.id == project_id
    ).first()

    if not project:
        return {
            "error":"project not found"
        }

    if project.pid:
        try:
            kill_process(
                project.pid
            )
            print(
                "Stopped PID:",
                project.pid
            )
        except Exception as e:
            print(
                "Kill error:",
                e
            )

    project.status="stopped"
    project.pid=None

    db.commit()
    db.close()

    return {
        "id":project_id,
        "status":"stopped"
    }

@app.post("/projects/{project_id}/restart")
def restart_project(
    project_id:int,
    current_user: dict = Depends(get_current_user)
):
    import os
    import signal
    from process_manager import kill_process

    db = SessionLocal()

    project = db.query(Project).filter(
        Project.id == project_id
    ).first()

    if not project:
        return {
            "error":"project not found"
        }

    # stop old process
    if project.pid:
        try:
            kill_process(
                project.pid
            )
            print(
                "Old process stopped:",
                project.pid
            )
        except Exception as e:
            print(
                "Stop error:",
                e
            )

    # reset for new deploy
    project.pid = None
    project.status = "pending"

    db.commit()
    db.close()

    return {
        "id":project_id,
        "status":"pending",
        "message":"restart queued"
    }


@app.get("/workers")
def get_workers(db: Session = Depends(get_db)):

    workers = db.query(Worker).all()

    return [
        {
            "worker_id": w.worker_id,
            "status": w.status,
            "cpu": w.cpu,
            "ram": w.ram,
            "projects": w.projects,
            "hostname": w.hostname,
            "last_seen": str(w.last_seen)
        }
        for w in workers
    ]



@app.get("/workers/{worker_id}")
def worker_detail(worker_id:str):
    db=SessionLocal()

    worker=db.query(Worker).filter(
        Worker.worker_id==worker_id
    ).first()

    if not worker:
        db.close()
        return {"error":"worker not found"}

    projects=db.query(Project).filter(
        Project.worker_id==worker_id
    ).all()

    data={
        "worker_id":worker.worker_id,
        "status":worker.status,
        "cpu":worker.cpu,
        "ram":worker.ram,
        "hostname":worker.hostname,
        "last_seen":str(worker.last_seen),
        "projects":[
            {
                "id":p.id,
                "name":p.name,
                "status":p.status,
                "pid":p.pid,
                "restart_count":p.restart_count
            }
            for p in projects
        ]
    }

    db.close()
    return data



@app.post("/internal/projects/{project_id}/restart")
def internal_restart_project(
    project_id:int
):
    db=SessionLocal()

    project=db.query(Project).filter(
        Project.id==project_id
    ).first()

    if not project:
        return {
            "error":"project not found"
        }

    project.status="restarting"
    project.pid=None

    db.commit()
    db.close()

    return {
        "id":project_id,
        "status":"restarting"
    }



@app.post("/internal/projects")
def internal_create_project(
    name:str,
    runtime:str="python",
    repo:str="local",
    db:Session=Depends(get_db)
):

    workers=db.query(Worker).filter(
        Worker.status=="online"
    ).all()

    selected=None

    if workers:
        workers=sorted(
            workers,
            key=lambda w:int(w.projects or 0)
        )
        selected=workers[0].worker_id


    project=Project(
        name=name,
        runtime=runtime,
        repo=repo,
        user_id=1,
        status="pending",
        auto_restart="yes",
        worker_id=selected
    )

    db.add(project)
    db.commit()
    db.refresh(project)

    return {
        "id":project.id,
        "status":project.status,
        "worker_id":project.worker_id
    }



@app.get("/projects/{project_id}/info")
def project_info(
    project_id:int,
    db:Session=Depends(get_db)
):

    import psutil
    import json
    import os

    project=db.query(Project).filter(
        Project.id==project_id
    ).first()

    if not project:
        return {
            "error":"project not found"
        }


    data={
        "id":project.id,
        "name":project.name,
        "status":project.status,
        "pid":project.pid,
        "worker_id":project.worker_id,
        "restart_count":project.restart_count or 0,
        "cpu":0,
        "ram":0
    }


    if project.pid:

        try:

            proc=psutil.Process(
                project.pid
            )

            data["cpu"]=proc.cpu_percent(
                interval=0.1
            )

            data["ram"]=round(
                proc.memory_info().rss/1024/1024,
                2
            )

        except:
            pass


    return data






@app.get("/projects/{project_id}/logs")
def project_logs(
    project_id:int
):

    import os

    log_file=f"/home/jeet/nono/projects/{project_id}/logs/app.log"

    if not os.path.exists(log_file):
        return {
            "id":project_id,
            "logs":""
        }

    with open(log_file,"r") as f:
        logs=f.read()

    return {
        "id":project_id,
        "logs":logs[-5000:]
    }

