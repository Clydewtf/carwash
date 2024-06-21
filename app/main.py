from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app import models, schemas, dependencies
from app.database import engine, SessionLocal
from app.dependencies import create_access_token, get_password_hash, authenticate_user
from datetime import timedelta
from app.api.endpoints import cars, services, users, customercars, orders
from app.api.endpoints.car import cars_endpoints

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/token", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(dependencies.get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=dependencies.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": str(user.id)}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me/", response_model=schemas.User)
def read_users_me(current_user: models.User = Depends(dependencies.get_current_active_user)):
    return current_user


app.include_router(cars_endpoints.router, prefix="/cars", tags=["cars"])
app.include_router(services.router, prefix="/services", tags=["services"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(customercars.router, prefix="/customercars", tags=["customercars"])
app.include_router(orders.router, prefix="/orders", tags=["orders"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)