import PyPDF2
import pdfplumber
from pathlib import Path
import json
from typing import Dict, List, Any

class PDFAnalyzer:
    def __init__(self, data_dir: str = "medical_data"):
        self.data_dir = Path(data_dir)
    
    def analyze_pdf_quality(self, pdf_path: Path) -> Dict[str, Any]:
        """Analyze a single PDF for RAG suitability"""
        analysis = {
            "filename": pdf_path.name,
            "file_size_mb": 0,
            "text_extractable": False,
            "text_quality": "unknown",
            "structure_quality": "unknown",
            "rag_ready": False,
            "recommendations": []
        }
        
        # Handle file size safely
        try:
            analysis["file_size_mb"] = round(pdf_path.stat().st_size / (1024 * 1024), 2)
        except Exception as e:
            analysis["recommendations"].append(f"⚠️ Could not get file size: {e}")
            analysis["file_size_mb"] = 0
        
        try:
            # Try pdfplumber first
            with pdfplumber.open(pdf_path) as pdf:
                all_text = ""
                page_count = len(pdf.pages)
                
                for i, page in enumerate(pdf.pages):
                    page_text = page.extract_text()
                    if page_text:
                        all_text += page_text + "\n"
                
                analysis["page_count"] = page_count
                analysis["total_characters"] = len(all_text)
                analysis["text_extractable"] = len(all_text) > 100
                
                if analysis["text_extractable"]:
                    # Analyze text quality
                    if len(all_text) > 5000:
                        analysis["text_quality"] = "excellent"
                    elif len(all_text) > 2000:
                        analysis["text_quality"] = "good"
                    elif len(all_text) > 500:
                        analysis["text_quality"] = "fair"
                    else:
                        analysis["text_quality"] = "poor"
                    
                    # Check for structure indicators
                    structure_indicators = [
                        "symptoms", "diagnosis", "treatment", "risk", "complication",
                        "recommendation", "guideline", "section", "chapter", "introduction"
                    ]
                    
                    structure_count = sum(1 for indicator in structure_indicators if indicator.lower() in all_text.lower())
                    
                    if structure_count > 5:
                        analysis["structure_quality"] = "excellent"
                    elif structure_count > 2:
                        analysis["structure_quality"] = "good"
                    else:
                        analysis["structure_quality"] = "basic"
                    
                    # Determine if RAG-ready
                    if analysis["text_quality"] in ["excellent", "good"] and analysis["structure_quality"] in ["excellent", "good"]:
                        analysis["rag_ready"] = True
                        analysis["recommendations"].append("✅ Ready for RAG as-is")
                    else:
                        analysis["recommendations"].append("⚠️ Consider preprocessing for better RAG performance")
                
                else:
                    analysis["recommendations"].append("❌ Text extraction failed - may need OCR")
            
            # If pdfplumber failed, try PyPDF2
            if not analysis["text_extractable"]:
                with open(pdf_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    all_text = ""
                    for page in pdf_reader.pages:
                        page_text = page.extract_text()
                        if page_text:
                            all_text += page_text + "\n"
                    
                    if len(all_text) > 100:
                        analysis["text_extractable"] = True
                        analysis["text_quality"] = "fair"
                        analysis["recommendations"].append("⚠️ Basic text extraction - consider preprocessing")
                    else:
                        analysis["recommendations"].append("❌ Text extraction failed - likely scanned PDF")
            
        except Exception as e:
            analysis["error"] = str(e)
            analysis["recommendations"].append(f"❌ Error analyzing PDF: {e}")
        
        return analysis
    
    def analyze_all_pdfs(self):
        """Analyze all PDFs in the directory"""
        print("🔍 Analyzing PDFs for RAG suitability...")
        
        pdf_files = list(self.data_dir.glob("*.pdf"))
        if not pdf_files:
            print("❌ No PDF files found!")
            return
        
        print(f"📁 Found {len(pdf_files)} PDF files to analyze")
        
        all_analyses = []
        rag_ready_count = 0
        needs_preprocessing_count = 0
        failed_count = 0
        
        for pdf_path in pdf_files:
            try:
                print(f"Analyzing: {pdf_path.name}")
                analysis = self.analyze_pdf_quality(pdf_path)
                all_analyses.append(analysis)
                
                if analysis["rag_ready"]:
                    rag_ready_count += 1
                elif analysis["text_extractable"]:
                    needs_preprocessing_count += 1
                else:
                    failed_count += 1
                    
            except Exception as e:
                print(f"❌ Error analyzing {pdf_path.name}: {e}")
                # Create a basic analysis entry for failed files
                failed_analysis = {
                    "filename": pdf_path.name,
                    "file_size_mb": 0,
                    "text_extractable": False,
                    "text_quality": "unknown",
                    "structure_quality": "unknown",
                    "rag_ready": False,
                    "recommendations": [f"❌ Analysis failed: {e}"]
                }
                all_analyses.append(failed_analysis)
                failed_count += 1
        
        # Create summary
        summary = {
            "total_pdfs": len(pdf_files),
            "rag_ready": rag_ready_count,
            "needs_preprocessing": needs_preprocessing_count,
            "failed_extraction": failed_count,
            "success_rate": f"{(rag_ready_count + needs_preprocessing_count)/len(pdf_files)*100:.1f}%"
        }
        
        # Save detailed analysis
        analysis_file = self.data_dir / "pdf_analysis_report.json"
        with open(analysis_file, 'w', encoding='utf-8') as f:
            json.dump({
                "summary": summary,
                "detailed_analyses": all_analyses
            }, f, indent=2, ensure_ascii=False)
        
        # Print results
        print("\n" + "="*60)
        print("📊 PDF ANALYSIS RESULTS")
        print("="*60)
        print(f"Total PDFs: {summary['total_pdfs']}")
        print(f"✅ RAG Ready (as-is): {summary['rag_ready']}")
        print(f"⚠️ Needs Preprocessing: {summary['needs_preprocessing']}")
        print(f"❌ Failed Extraction: {summary['failed_extraction']}")
        print(f"Success Rate: {summary['success_rate']}")
        
        print("\n" + "="*60)
        print("🎯 RECOMMENDATIONS")
        print("="*60)
        
        if rag_ready_count > len(pdf_files) * 0.7:
            print("✅ MOST PDFs are RAG-ready! You can use them as-is.")
            print("💡 Consider light preprocessing for optimal performance.")
        elif needs_preprocessing_count > len(pdf_files) * 0.5:
            print("⚠️ MANY PDFs need preprocessing for optimal RAG performance.")
            print("💡 Use the PDF processor to clean and structure the data.")
        else:
            print("❌ MANY PDFs have extraction issues.")
            print("💡 Use the PDF processor with OCR capabilities.")
        
        print(f"\n📋 Detailed analysis saved to: {analysis_file}")
        
        return summary, all_analyses

def main():
    analyzer = PDFAnalyzer()
    analyzer.analyze_all_pdfs()

if __name__ == "__main__":
    main() 