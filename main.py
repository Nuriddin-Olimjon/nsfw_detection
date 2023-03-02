import os, uuid, shutil

import uvicorn
from fastapi import FastAPI, File, UploadFile, Depends, HTTPException

from app.auth import get_current_username
from config import PORT, MAX_IMAGE_SIZE, ALLOWED_CONTENT_TYPES
from nsfw_detector import predict


MODEL = predict.load_model('nsfw_detector/nsfw_model.h5')

app = FastAPI()


@app.post("/api/nsfw-check")
async def nsfw_check(input_file: UploadFile = File(), _: str = Depends(get_current_username)):
    max_size = MAX_IMAGE_SIZE * 1024 * 1024
    image_size_bytes = input_file.size
    if image_size_bytes > max_size:
        raise HTTPException(status_code=413, detail="Payload too large")

    content_type = input_file.content_type
    if content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(status_code=400, detail="Invalid document type")

    file_name = os.path.join("images", str(uuid.uuid4()) + input_file.filename)
    with open(file_name, "wb+") as f:
        shutil.copyfileobj(input_file.file, f)

    result = predict.classify(MODEL, file_name)
    os.remove(file_name)

    return {
        "result": result["data"]
    }


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=PORT, log_level="debug")
