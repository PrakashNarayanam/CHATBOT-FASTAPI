from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi import Request

import google.generativeai as genai
import os 
from dotenv import load_dotenv


GEMINI_API_KEY="AIzaSyAo6_URktbs6rmc2Mr4sXqk4c1nht6wXPs"

genai.configure(api_key=GEMINI_API_KEY)
try:
    model=genai.GenerativeModel('gemini-2.0-flash')
    print("Gemini model initiliazed")
except Exception as e:
    print(f"Error initializng model:{e}")
    print("Available models")
    for m in genai.list_models():
        print(f"- {m.name}")
    # raise 
app=FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static",StaticFiles(directory="static"),name="static")
templates=Jinja2Templates(directory="templates")
@app.get("/")
async def serve_index(request:Request):
    return templates.TemplateResponse("index.html", {"request": request})
@app.post("/get")
async def get_response(data:dict):
    print("Recieved data",data)
    message=data.get("msg")
    try:
        response=model.generate_content(f"you are a helpful assistant {message}",
        generation_config={
            "max_output_tokens":150,
            "temperature":0.7,
        }
    )
        if hasattr(response,'parts'):
            reply=''.join(part.text for part in response.parts if hasattr(part,'text'))
        elif hasattr(response,'text'):
            reply=response.text
        else:
            reply="I'm sorry.I could not generate a response"
        print("reply:",reply)
        return JSONResponse({"reply":reply})
    except Exception as e :
        print("Error in generate_content",str(e))
        return JSONResponse({"reply": "I'm sorry, I encountered an error"})

    except Exception as e:
        print("Error:",str(e))