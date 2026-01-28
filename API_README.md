# Handwriting Synthesis API

A FastAPI backend that converts text to realistic handwriting using a neural network.

## Quick Start

### Installation

```bash
# Install dependencies
uv sync
```

### Running the Server

```bash
uv run uvicorn app:app --reload
```

The API will be available at `http://localhost:8000`

## API Usage

### Interactive Documentation

Visit `http://localhost:8000/docs` for interactive API documentation.

### Endpoint: POST /synthesize

Convert text to handwriting SVG.

**Request Body:**
```json
{
  "text": "Your text here",
  "bias": 0.75,
  "style": 9,
  "stroke_color": "black",
  "stroke_width": 2
}
```

**Parameters:**
- `text` (required): Text to convert (max 75 chars per line, use `\n` for multiple lines)
- `bias` (optional, default 0.75): Controls neatness (0.0-1.0, higher = neater)
- `style` (optional, default 9): Handwriting style (0-27)
- `stroke_color` (optional, default "black"): SVG stroke color
- `stroke_width` (optional, default 2): SVG stroke width (1-10)

**Response:** SVG image with `image/svg+xml` content type

### Examples

**cURL:**
```bash
curl -X POST http://localhost:8000/synthesize \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello World!", "bias": 0.75, "style": 9}' \
  -o handwriting.svg
```

**Python:**
```python
import requests

response = requests.post(
    "http://localhost:8000/synthesize",
    json={
        "text": "Beautiful handwriting!",
        "bias": 0.8,
        "style": 12
    }
)

with open("output.svg", "w") as f:
    f.write(response.text)
```

**JavaScript:**
```javascript
fetch('http://localhost:8000/synthesize', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    text: 'Hello from JavaScript!',
    bias: 0.75,
    style: 9
  })
})
.then(res => res.text())
.then(svg => console.log(svg));
```

## Testing

Run the test suite:
```bash
# Start the server first
uv run uvicorn app:app --reload

# In another terminal, run tests
uv run python test_api.py
```

## Technical Details

- Built with FastAPI and TensorFlow 2.x
- Uses a pre-trained RNN with LSTM attention cells
- Supports 28 different handwriting styles
- Generates SVG paths from stroke sequences

## Original Project

Based on [sjvasquez/handwriting-synthesis](https://github.com/sjvasquez/handwriting-synthesis)
