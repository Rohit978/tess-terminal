"""
Converter Skill - Convert between file formats.
"""

import os
from pathlib import Path
from typing import Union, List, Optional


class ConverterSkill:
    """
    Converts files between formats (images to PDF, etc.).
    """
    
    def run(self, sub_action: str, source_paths: Union[str, List[str]], 
            output_filename: Optional[str] = None) -> str:
        """
        Run conversion.
        
        Args:
            sub_action: Conversion type
            source_paths: Input file(s)
            output_filename: Output file name
            
        Returns:
            Status message
        """
        if isinstance(source_paths, str):
            source_paths = [source_paths]
        
        if sub_action in ["images_to_pdf", "image_to_pdf"]:
            return self._images_to_pdf(source_paths, output_filename)
        elif sub_action == "docx_to_pdf":
            return self._docx_to_pdf(source_paths[0], output_filename)
        else:
            return f"Unknown conversion: {sub_action}"
    
    def _images_to_pdf(self, image_paths: List[str], output: Optional[str]) -> str:
        """Convert images to PDF."""
        try:
            from PIL import Image
            
            if not output:
                output = "output.pdf"
            
            if not output.endswith('.pdf'):
                output += '.pdf'
            
            # Open first image
            images = []
            for path in image_paths:
                if os.path.exists(path):
                    img = Image.open(path)
                    if img.mode != 'RGB':
                        img = img.convert('RGB')
                    images.append(img)
            
            if not images:
                return "No valid images found"
            
            # Save as PDF
            first = images[0]
            rest = images[1:] if len(images) > 1 else []
            
            first.save(output, "PDF", resolution=100.0, save_all=True, append_images=rest)
            
            return f"Created PDF: {output} ({len(images)} pages)"
            
        except ImportError:
            return "PIL not installed. Run: pip install pillow"
        except Exception as e:
            return f"Conversion error: {e}"
    
    def _docx_to_pdf(self, docx_path: str, output: Optional[str]) -> str:
        """Convert DOCX to PDF."""
        try:
            from docx2pdf import convert
            
            if not output:
                output = docx_path.replace('.docx', '.pdf')
            
            convert(docx_path, output)
            return f"Converted: {output}"
            
        except ImportError:
            return "docx2pdf not installed. Run: pip install docx2pdf"
        except Exception as e:
            return f"Conversion error: {e}"
