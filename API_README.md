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

## Running with multiple workers (parallel requests)

To handle many frontend or external clients in parallel, run the API with **multiple Uvicorn workers**. Each worker can process a request at the same time.

### Docker (recommended)

The `docker-compose` setup runs with **4 workers** by default. Uvicorn distributes incoming requests across workers so parallel calls get faster responses.

```bash
docker compose up --build
```

**Tuning workers**

- **More workers** = more concurrent requests, but **higher RAM** (each worker loads the TensorFlow model).
- Set the `WORKERS` env in `docker-compose.yml` or override when starting:

```bash
# Use 2 workers (e.g. if the host has limited RAM)
WORKERS=2 docker compose up --build

# Or in docker-compose.yml under app.environment:
# - WORKERS=2
```

### Local (without Docker)

Run Uvicorn with `--workers`:

```bash
uv run uvicorn app:app --host 0.0.0.0 --port 8000 --workers 4
```

Use fewer workers (e.g. `--workers 2`) if you run out of memory, since each process loads the model.

## Technical Details

- Built with FastAPI and TensorFlow 2.x
- Uses a pre-trained RNN with LSTM attention cells
- Supports 28 different handwriting styles
- Generates SVG paths from stroke sequences

## Original Project

Based on [sjvasquez/handwriting-synthesis](https://github.com/sjvasquez/handwriting-synthesis)
