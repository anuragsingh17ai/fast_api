''' for now this our main file'''
from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from transformers import pipeline
from PIL import Image
from io import BytesIO
import uvicorn
from typing import Optional
from uuid import uuid4
from typing import Annotated
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost:3000/",
    "http://localhost:3000"
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
model_id = "llava-hf/llava-1.5-7b-hf"
#pipe = pipeline("image-to-text", model=model_id)

# In-memory storage for sessions and chat histories
sessions = {}
chat_histories = {}

def generate_uuid():
    return str(uuid4())

@app.post("/process")
async def process_image_and_ask(
    file: Optional[UploadFile] = File(None),
    prompt: str = Form() ,
    session_id: Annotated[str, Form()] = None
   
):
    print("**********************I ma here")
    try:
        if file and not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="Invalid file type. Only image files are accepted.")

        if not file and not session_id:
            # No file and no session ID provided
            raise HTTPException(status_code=400, detail="No image or session ID provided.")

        try:
            if file:
                # Process the new image upload
                contents = await file.read()
                image = Image.open(BytesIO(contents))
                print("Image processed")
                session_id = session_id or generate_uuid()  # Generate new UUID if not provided
                sessions[session_id] = image
                print("saved to session")
                chat_histories[session_id] = []  # Initialize chat history for the new session

            if not session_id in sessions:
                raise HTTPException(status_code=404, detail="Session ID not found or no image uploaded.")

            # Retrieve image from session storage if no new file is uploaded
            image = sessions[session_id]

            # Build the full chat prompt using the history
            chat_history = chat_histories.get(session_id, [])
            full_prompt = "\n".join([f"USER: {x['user']}\nBOT: {x['bot']}" for x in chat_history])
            full_prompt += f"\nUSER: <image>\n {prompt}\nBOT:"
            print("*****************************",full_prompt)
            
            outputs = "Test Output"#pipe(image, prompt=full_prompt, generate_kwargs={"max_new_tokens": 800})[0]
            response = "Test Output"#outputs['generated_text'].split('BOT:')[-1].strip()
            print("************response",response)
            # Update chat history for the session
            chat_history.append({"user": prompt, "bot": response})
            chat_histories[session_id] = chat_history

            return {"session_id": session_id, "response": response}

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        
    except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)