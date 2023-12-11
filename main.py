import tempfile
from fastapi import FastAPI, UploadFile
from fastapi.responses import FileResponse, JSONResponse
from masker import Masker

app = FastAPI()

@app.get("/")
def api_usage():
    return {
        "/mask_aadhaar" : "upload aadhar image for masking"
    }

# @app.post("/mask_aadhar/")
# def mask_image(file: UploadFile):

#     with open(tempfile.NamedTemporaryFile(suffix=".jpeg").name, 'w') as f:
#         m = Masker(file.file)
#         success = m.mask_aadhar(f)

#         if success:
#             return FileResponse(path=f.name, media_type="image/png")
#         else:
#             return JSONResponse(
#                 status_code=404, 
#                 content="Unable to mask image"
#             )

@app.post("/mask_aadhar/")
def mask_image(file: UploadFile):
    with open(tempfile.NamedTemporaryFile(suffix=".jpeg").name, 'w') as f:
        m = Masker(file.file)
        try:
            success = m.mask_aadhar(f)
            if success:
                return FileResponse(path=f.name, media_type="image/png")
            else:
                return JSONResponse(
                    status_code=400,
                    content="Unable to mask Aadhar numbers. Make sure the Aadhar numbers are detected in the image."
                )
        except Exception as e:
            return JSONResponse(
                status_code=500,
                content=f"Internal Server Error: {str(e)}"
            )

