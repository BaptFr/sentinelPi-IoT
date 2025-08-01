# from fastapi import APIRouter, HTTPException, UploadFile, File
# from fastapi.responses import JSONResponse
# from services.biometric_service import validate_face

# router = APIRouter(
#     prefix="/biometrics",
#     tags=["biometric-auth"]
# )

# #POST file for comparison
# @router.post("/face")
# async def authenticate_face(image: UploadFile = File(...)):
#     #Receive image? fil from rapsberry

#     #   If Ok,  
#     return JSONResponse(content={"access_granted": True})

# @router.post("/fingerprint")
# async def authenticate_fingerprint(data: UploadFile = File(...)):
#     #Idem
    
#     return JSONResponse(content={"access_granted": True})

