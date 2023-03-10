import os, uuid, shutil

import uvicorn
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from config import PORT, MAX_IMAGE_SIZE, ALLOWED_CONTENT_TYPES
from nsfw_detector import predict


MODEL = predict.load_model('nsfw_detector/nsfw_model.h5')

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/api/internal/nsfw-check")
async def nsfw_check(input_file: UploadFile = File()):
    max_size = MAX_IMAGE_SIZE * 1024 * 1024
    image_size_bytes = input_file.size
    if image_size_bytes > max_size:
        raise HTTPException(status_code=413, detail="Payload too large")

    if input_file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(status_code=400, detail="Invalid document type")

    file_name = os.path.join("images", str(uuid.uuid4()) + input_file.filename)
    with open(file_name, "wb+") as f:
        shutil.copyfileobj(input_file.file, f)

    result = predict.classify(MODEL, file_name)
    os.remove(file_name)

    is_safe = False
    if result["data"]["neutral"] > 87:
        is_safe = True

    return {
        "results": result["data"],
        "is_safe": is_safe
    }


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=PORT, log_level="info")
