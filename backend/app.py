from fastapi import FastAPI
try:
    from src.routers.chatbot import chatbot_router
except ImportError:
    from backend.src.routers.chatbot import chatbot_router

app = FastAPI(
    title="PDF Chatbot App API",
    description="""FastAPI documentation for PDF Chatbot App""",
    contact={
        'name': 'Demo App',
        'url': 'http://localhost:8501'
    },
    version="0.1.0",
)
app.include_router(chatbot_router)

tags_metadata = [
    {
        'name': 'PDF Chatbot',
        'descriptions': ' PDF Chatbot for answering to the questions, which releated to PDF files.'
    }
]


# TODO: delete when correct tests will be added
@app.get("/example")
async def example():
    # print(os.environ['TEST_SECRET']) # now not in env var
    return {"message": 'Hello'}
