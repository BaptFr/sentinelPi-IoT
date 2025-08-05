from hardware.face import encode_face_image
from services.user_service import get_all_known_encodings
import face_recognition

async def validate_face(file):
    unknown_encoding = await encode_face_image(file)
    known_encodings = await get_all_known_encodings()

    for known in known_encodings:
        result = face_recognition.compare_faces([known], unknown_encoding)
        if result[0]:
            return True
    return False
