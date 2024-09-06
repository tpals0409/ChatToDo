import extractCategory
import ToDoCreate
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

question_category = "NONE"


class UserInput(BaseModel):
    user_input: str

@app.post("/chat/")
async def process_message(input_data: UserInput):
    global question_category
    try:
        user_input = input_data.user_input
        if question_category == "NONE":
            response, question_category = extractCategory.run(user_input)
            if question_category == "생성":
                create = ToDoCreate.run(response)
                question_category = "NONE"
                return {"response": create}
            elif question_category == "조회":
                question_category = "NONE"
                return {"response": "조회"}
            elif question_category == "수정":
                question_category = "NONE"
                return {"response": "수정"}
            elif question_category == "삭제":
                question_category = "NONE"
                return {"response": "삭제"}
            else:
                return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
