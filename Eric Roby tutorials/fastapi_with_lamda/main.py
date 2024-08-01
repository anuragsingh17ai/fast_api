'''
pip install fastapi uvicorn mangum
pip freeze> requirements.txt
pip install -t dependencies -r requirements.txt
cd dependencies; zip ../aws_lambda_artifact. zip -r .)
zip aws_lambda_artifact.zip -u main.py  #adding main to aws lambda zip file


Now.......................
1. go to aws console
2. search aws lambda than on "create a function"
Then a form type will arise now in author from scratch part
3. IN Function name write name of function eg. "a fastapi application"
4. change Runtime to python
5. keep Architecture x86_64
6.  in Advance setting
    --->  Enable function url
        ---> choose auth type 
7. Now at lower right most part click on create a function

at right of test click on "upload "than on "from zip" now upload "aws lambda artifact" that you made with above code

now under runtime setting click on "Edit"
 --> you will see Handler info input box here just mention location of mangum in our case it is "main.handler"

 now you can use url (Happy day)
'''

from fastapi import FastAPI
from mangum import Mangum

app = FastAPI()
handler = Mangum(app)

@app.get("/")
async def hello():
    return {"message": "Hello from coding"}

