from fastapi import APIRouter, UploadFile, File, HTTPException

router = APIRouter()

@router.post("/document")
async def upload_document(file: UploadFile = File(...)):
    """Upload document for AI processing"""
    
    if not file.filename.endswith(('.txt', '.pdf', '.docx', '.md')):
        raise HTTPException(
            status_code=400, 
            detail="Unsupported file format. Use: .txt, .pdf, .docx, .md"
        )
    
    # In real implementation, save and process file
    return {
        "status": "success",
        "filename": file.filename,
        "content_type": file.content_type,
        "message": "Document uploaded for processing"
    }