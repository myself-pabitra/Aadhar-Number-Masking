import tempfile
from fastapi import FastAPI, UploadFile
from fastapi.responses import FileResponse, JSONResponse
from aadhar_masker import AadharMasker
from pan_masker import PanMasker

app = FastAPI()

@app.get("/")
def api_usage():
    return {
        "/mask_aadhaar" : "upload aadhar image for masking"
    }


@app.post("/mask_aadhar/")
def mask_image(file: UploadFile):
    with open(tempfile.NamedTemporaryFile(suffix=".jpeg").name, 'w') as f:
        m = AadharMasker(file.file)
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

@app.post("/mask_pan/")
def mask_image(file: UploadFile):
    with open(tempfile.NamedTemporaryFile(suffix=".jpeg").name, 'w') as f:
        m = PanMasker(file.file)
        try:
            success = m.mask_pan(f)
            if success:
                return FileResponse(path=f.name, media_type="image/png")
            else:
                return JSONResponse(
                    status_code=400,
                    content="Unable to mask PAN numbers. Make sure the PAN numbers are detected in the image."
                )
        except Exception as e:
            return JSONResponse(
                status_code=500,
                content=f"Internal Server Error: {str(e)}"
            )


