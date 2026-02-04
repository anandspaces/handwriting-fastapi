import io
import os
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from pydantic import BaseModel, Field, field_validator

from demo import Hand


app = FastAPI(
    title="Handwriting Synthesis API",
    description="Generate handwritten text as SVG using neural networks",
    version="1.0.0"
)

# Add CORS middleware for browser access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class SynthesizeRequest(BaseModel):
    text: str = Field(..., description="Text to convert to handwriting (max 75 characters per line)")
    bias: Optional[float] = Field(0.75, description="Controls neatness (0.0-1.0, higher is neater)", ge=0.0, le=1.0)
    style: Optional[int] = Field(9, description="Handwriting style (0-27)", ge=0, le=27)
    stroke_color: Optional[str] = Field("black", description="SVG stroke color")
    stroke_width: Optional[int] = Field(2, description="SVG stroke width", ge=1, le=10)
    font_size: Optional[float] = Field(1.5, description="Font size scaling factor (0.5-3.0, default 1.5)", ge=0.5, le=3.0)
    
    @field_validator('text')
    @classmethod
    def validate_text(cls, v):
        if not v or not v.strip():
            raise ValueError("Text cannot be empty")
        # Split into lines and check each line length
        lines = v.split('\n')
        for i, line in enumerate(lines):
            if len(line) > 75:
                raise ValueError(f"Line {i+1} exceeds 75 characters (has {len(line)})")
        return v


# Initialize the Hand model once at startup
hand = None

@app.on_event("startup")
async def startup_event():
    global hand
    print("Loading handwriting synthesis model...")
    hand = Hand()
    print("Model loaded successfully!")


@app.get("/")
async def root():
    return {
        "message": "Handwriting Synthesis API",
        "docs": "/docs",
        "endpoint": "POST /synthesize"
    }


@app.post("/synthesize", response_class=Response)
async def synthesize_handwriting(request: SynthesizeRequest):
    """
    Generate handwritten text as SVG.
    
    - **text**: The text to convert (max 75 chars per line, use \\n for multiple lines)
    - **bias**: Controls neatness (0.0-1.0, default 0.75)
    - **style**: Handwriting style 0-27 (default 9)
    - **stroke_color**: SVG stroke color (default "black")
    - **stroke_width**: SVG stroke width (default 2)
    - **font_size**: Font size scaling factor (0.5-3.0, default 1.5)
    
    Returns SVG image data.
    """
    try:
        # Split text into lines
        lines = request.text.split('\n')
        
        # Prepare parameters for each line
        biases = [request.bias] * len(lines)
        styles = [request.style] * len(lines)
        stroke_colors = [request.stroke_color] * len(lines)
        stroke_widths = [request.stroke_width] * len(lines)
        font_sizes = [request.font_size] * len(lines)
        
        # Generate temporary filename
        temp_filename = f"/tmp/handwriting_{os.getpid()}.svg"
        
        # Generate handwriting
        hand.write(
            filename=temp_filename,
            lines=lines,
            biases=biases,
            styles=styles,
            stroke_colors=stroke_colors,
            stroke_widths=stroke_widths,
            font_sizes=font_sizes
        )
        
        # Read the SVG file
        with open(temp_filename, 'r') as f:
            svg_content = f.read()
        
        # Clean up temporary file
        os.remove(temp_filename)
        
        # Return SVG with proper content type
        return Response(content=svg_content, media_type="image/svg+xml")
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating handwriting: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
