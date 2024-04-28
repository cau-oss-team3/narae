from fastapi import FastAPI, Depends, HTTPException
from openai import OpenAI
from sqlalchemy.orm import Session

from app.config import Config
from app.models import Item
from app.database import setup_database
from app.schemas import InputsOfGPT, ItemCreate

app = FastAPI()
config = Config()
SessionLocal = setup_database(config)
client = OpenAI(api_key=config.get_openapi_key())

# Dependency: Database Session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Routes
@app.get("/")
def home():
    return {"Hello": "World"}

@app.post("/test-gpt/")
def test_gpt(inputs: InputsOfGPT):
    system_prompt = f"""
    I've heard that you are a world-renowned coach in the field of backend development coaching.
    I want to improve my expertise in {inputs.interest} within this field, but I'm having trouble.
    Here are the details of what I've tried so far and what hasn't worked: {inputs.session_details}

    Based on this information, could you assess my current progress, identify obstacles, and suggest next action items?
    If necessary, please provide motivational feedback.
    Additionally, please use the following details to ask me questions to enhance my API design skills and provide expert feedback on my responses. If my responses are lacking, kindly suggest areas for improvement, necessary understandings, and request further explanation.
    """
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": "Given the details I've provided, could you assess my current progress, identify obstacles, and suggest next action items?"
            }
        ],
        temperature=0.5,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    return {"response": response.choices[0].message.content}

@app.get("/items/")
def read_items(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    items = db.query(Item).offset(skip).limit(limit).all()
    return {"items": items}

@app.get("/items/{item_id}")
def read_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item": item}

@app.post("/items/")
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    db_item = Item(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return {"item": db_item}
