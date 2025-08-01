import face_recognition
from fastapi import UploadFile
import io

async def encode_face_image(file: UploadFile):
    image_bytes = await file.read()
    image = face_recognition.load_image_file(io.BytesIO(image_bytes))
    encodings = face_recognition.face_encodings(image)
    return encodings[0] if encodings else None
