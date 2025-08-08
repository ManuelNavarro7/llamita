#!/bin/bash

echo "📄 Installing Document Processing Dependencies for Llamita..."

# Check if pip is available
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 not found. Please install Python and pip first."
    exit 1
fi

echo "📦 Installing required packages..."

# Install document processing dependencies
pip3 install PyPDF2>=3.0.0
pip3 install python-docx>=0.8.11
pip3 install pandas>=2.0.0
pip3 install openpyxl>=3.1.0

echo "✅ Document processing dependencies installed!"

# Test the installation
echo "🧪 Testing installation..."
python3 scripts/test_document_feature.py

echo ""
echo "🎉 Document processing feature is now ready!"
echo "📄 You can now upload documents (PDF, DOCX, TXT, CSV, Excel) to Llamita"
echo "💡 Start Llamita and click 'Upload Documents' to get started"
