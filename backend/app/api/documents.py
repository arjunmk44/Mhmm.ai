from typing import List
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status, BackgroundTasks
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.crud.document import create_document, get_document, get_documents
from app.crud.audit import create_audit_entry
from app.schemas.document import DocumentSchema, DocumentUploadResponse
from app.services.ingestion_service import process_ingestion

router = APIRouter(prefix="/documents", tags=["documents"])


@router.post(
    "/upload",
    response_model=DocumentUploadResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
async def upload_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    if not file or not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be provided.",
        )

    content = await file.read()
    if not content or len(content) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file is empty.",
        )

    # 1. Insert database row with status='pending'
    doc = create_document(
        db,
        filename=file.filename,
        document_type=file.content_type or "application/octet-stream",
        status="pending",
    )

    create_audit_entry(
        db,
        action="document_upload_received",
        details={"document_id": str(doc.id), "filename": file.filename},
    )

    # 2. Add non-blocking background ingestion task
    background_tasks.add_task(
        process_ingestion,
        document_id=str(doc.id),
        file_content=content,
        filename=file.filename,
        db=db,
    )

    # 3. Immediately return 202 Accepted
    return DocumentUploadResponse(
        id=str(doc.id),
        status="pending",
        message="Upload successful, ingestion started.",
    )


@router.get("", response_model=List[DocumentSchema], status_code=status.HTTP_200_OK)
@router.get("/", response_model=List[DocumentSchema], status_code=status.HTTP_200_OK)
def list_documents(db: Session = Depends(get_db)):
    docs = get_documents(db)
    return [DocumentSchema.model_validate(doc) for doc in docs]


@router.get("/{id}", response_model=DocumentSchema, status_code=status.HTTP_200_OK)
def get_document_by_id(id: str, db: Session = Depends(get_db)):
    doc = get_document(db, id)
    if not doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Document with id '{id}' not found.",
        )
    return DocumentSchema.model_validate(doc)

