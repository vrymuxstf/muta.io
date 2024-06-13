import uuid
import uvicorn

from fastapi import Depends, FastAPI, WebSocket, WebSocketDisconnect, Request, HTTPException
from fastapi.responses import HTMLResponse

from sqlalchemy.orm import Session

from sqlalchemy import or_, and_

import models
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()

messages = []

user_login_sessions = []


@app.get("/")
def read_root():
    with open('index.html', 'r') as file:
        content = file.read()
    return HTMLResponse(content)


@app.get("/login")
def login():
    with open('login.html', 'r') as file:
        content = file.read()
    return HTMLResponse(content)


@app.get("/client")
def login():
    with open('client.html', 'r') as file:
        content = file.read()
    return HTMLResponse(content)


@app.get("/validation")
def validation(token: str):
    for user_login_session in user_login_sessions:
        if user_login_session["token"] == token:
            return True

    return False


@app.get("/create_user")
def create_user(username: str, password: str, db: Session = Depends(get_db)):
    db_user = models.User(username=username, password=password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@app.get("/list_users")
def list_users(token: str, db: Session = Depends(get_db)):
    if validation(token):
        return db.query(models.User).all()
    else:
        "Token not found!"

    return db.query(models.User).all()


@app.get("/list_user_login_sessions")
def list_users():
    return user_login_sessions


@app.post("/login")
def login(username: str, password: str, request: Request, db: Session = Depends(get_db)):
    for user in db.query(models.User).filter(and_(models.User.username == username, models.User.password == password)):
        user_login_session_token = str(uuid.uuid4())

        user_login_sessions.append(
            {
                "username": user.username,
                "token": user_login_session_token,
                "ip": request.client.host,
                "user_agent": request.headers.get("User-Agent"),
            }
        )

        return user_login_session_token

    raise HTTPException(status_code=401, detail="username or password incorrect")


@app.get("get_username")
def get_username(user_login_session_token: str):
    for user_login_session in user_login_sessions:
        if user_login_session["token"] == user_login_session_token:
            return user_login_session["username"]

    return ""


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, user_login_session_token: str):
    print(user_login_session_token)

    await manager.connect(websocket)

    for message in messages:
        await websocket.send_text(message)

    try:
        while True:
            data = await websocket.receive_text()
            messages.append(data)
            await manager.broadcast(data)
    except WebSocketDisconnect:
        manager.disconnect(websocket)


if __name__ == "__main__":
    uvicorn.run(app)
