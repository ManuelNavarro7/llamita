# Document Processing Feature

Llamita now supports document processing! You can upload documents and ask questions about their content.

## Features

- **Multiple Format Support**: PDF, DOCX, TXT, CSV, Excel files
- **Smart Chunking**: Documents are split into manageable chunks for better context
- **Relevant Retrieval**: AI finds the most relevant document sections for your questions
- **Easy Upload**: Simple GUI for uploading and managing documents
- **Persistent Storage**: Documents are saved and available across sessions

## Installation

### 1. Install Dependencies

Run the installation script:

```bash
./scripts/install_document_deps.sh
```

Or install manually:

```bash
pip3 install PyPDF2>=3.0.0 python-docx>=0.8.11 pandas>=2.0.0 openpyxl>=3.1.0
```

### 2. Test Installation

```bash
python3 scripts/test_document_feature.py
```

## Usage

### Uploading Documents

1. Start Llamita
2. Click the "📄 Upload Documents" button
3. Select your document file
4. Click "Upload Document"
5. The document will be processed and stored

### Supported Formats

- **Text Files** (.txt)
- **PDF Documents** (.pdf)
- **Word Documents** (.docx)
- **Spreadsheets** (.csv, .xlsx, .xls)

### Asking Questions

Once you've uploaded documents, simply ask questions like:

- "What does the document say about [topic]?"
- "Summarize the main points from the document"
- "What are the key findings in the report?"
- "Can you explain the data in the spreadsheet?"

## How It Works

### Document Processing

1. **Text Extraction**: Documents are converted to plain text
2. **Chunking**: Text is split into overlapping chunks (~1000 characters each)
3. **Storage**: Chunks and metadata are saved locally
4. **Indexing**: Simple keyword indexing for retrieval

### Context Retrieval

When you ask a question:

1. **Query Analysis**: Your question is analyzed for keywords
2. **Relevance Scoring**: Document chunks are scored based on keyword matches
3. **Context Building**: Most relevant chunks are selected
4. **AI Response**: Llamita uses the document context to answer your question

## File Storage

Documents are stored in the `documents/` directory:

```
documents/
├── metadata.json          # Document metadata
├── [doc_id]_chunks.json  # Document chunks for each file
└── ...
```

## Troubleshooting

### Dependencies Not Available

If you see "Document processing not available":

```bash
pip3 install PyPDF2 python-docx pandas openpyxl
```

### PDF Processing Issues

Some PDFs may not extract text properly if they're image-based or have complex layouts.

### Large Documents

Very large documents (>10MB) may take longer to process. The system will show progress updates.

## Advanced Usage

### Document Management

- **Remove Documents**: Select a document in the upload dialog and click "Remove Selected"
- **View Documents**: See all uploaded documents in the upload dialog
- **Clear All**: Documents persist until manually removed

### Performance Tips

- **Optimal Chunk Size**: Default 1000 characters with 200 character overlap
- **Memory Usage**: Large documents use more memory during processing
- **Storage**: Each document creates metadata and chunk files

## Future Enhancements

Planned improvements:

- **Semantic Search**: Better relevance using embeddings
- **Document Summaries**: Automatic document summarization
- **Multiple Document Queries**: Ask questions across multiple documents
- **Document Categories**: Organize documents by type or topic
- **Export Features**: Export processed documents or summaries

## Technical Details

### Architecture

```
DocumentProcessor
├── Text Extraction (PDF, DOCX, CSV, Excel)
├── Chunking Algorithm
├── Storage Management
└── Context Retrieval

VoiceAssistant
├── Document Upload UI
├── Context Integration
└── AI Response Enhancement
```

### Dependencies

- **PyPDF2**: PDF text extraction
- **python-docx**: Word document processing
- **pandas**: Spreadsheet data handling
- **openpyxl**: Excel file support

## Contributing

To contribute to the document processing feature:

1. Fork the repository
2. Create a feature branch
3. Add tests in `scripts/test_document_feature.py`
4. Submit a pull request

## Support

If you encounter issues:

1. Check the console output for error messages
2. Verify dependencies are installed correctly
3. Test with a simple text file first
4. Check file permissions and storage space
