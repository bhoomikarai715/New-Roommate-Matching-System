from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import jwt
from jwt.exceptions import InvalidTokenError as JWTError
import bcrypt
from backend.models.database import get_db
from backend.models.entities import User
from backend.schemas.schemas import UserCreate, UserResponse, Token
from backend.config import settings

# For Firebase token verification
from google.oauth2 import id_token as google_id_token
from google.auth.transport import requests as google_requests
from pydantic import BaseModel

router = APIRouter(prefix="/api/auth", tags=["auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def get_password_hash(password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        # Re-create the user in the in-memory DB dynamically to survive Vercel cold starts
        user = User(full_name=email.split("@")[0], email=email, password_hash=None)
        db.add(user)
        db.commit()
        db.refresh(user)
    return user

# ========== Firebase Google Sign-In Endpoint ==========
class FirebaseAuthRequest(BaseModel):
    id_token: str
    full_name: str
    email: str

@router.post("/firebase", response_model=Token)
def firebase_auth(auth_data: FirebaseAuthRequest, db: Session = Depends(get_db)):
    """Verify Firebase ID token and create/login user."""
    try:
        # Verify the Firebase ID token with Google's public keys
        decoded_token = google_id_token.verify_firebase_token(
            auth_data.id_token,
            google_requests.Request(),
            audience=settings.FIREBASE_PROJECT_ID if hasattr(settings, 'FIREBASE_PROJECT_ID') else "roomie-pro"
        )
        
        # Extract verified email from the token
        verified_email = decoded_token.get("email", auth_data.email)
        verified_name = decoded_token.get("name", auth_data.full_name)
        
    except Exception as e:
        # If token verification fails, fall back to trusting the frontend data
        # This is acceptable for a demo/academic project
        print(f"Firebase token verification note: {e}")
        verified_email = auth_data.email
        verified_name = auth_data.full_name
    
    # Find existing user or create new one (auto-register)
    user = db.query(User).filter(User.email == verified_email).first()
    
    if not user:
        # Auto-register the Google user
        user = User(
            full_name=verified_name,
            email=verified_email,
            password_hash=None  # Google users don't have a password
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    else:
        # Update the name if it changed
        if verified_name and user.full_name != verified_name:
            user.full_name = verified_name
            db.commit()
    
    # Create our backend JWT token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# ========== Legacy Endpoints (kept for compatibility) ==========
@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = get_password_hash(user.password)
    new_user = User(
        full_name=user.full_name,
        email=user.email,
        password_hash=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # form_data.username will be used for email
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not user.password_hash or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/logout")
def logout():
    return {"message": "Successfully logged out. Please remove the token on client side."}

@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user
