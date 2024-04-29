from fastapi import APIRouter

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/login")
def login():
    return {"message": "Login"}

@router.get("/logout")
def logout():
    return {"message": "Logout"}

@router.get("/register")
def register():
    return {"message": "Register"}
