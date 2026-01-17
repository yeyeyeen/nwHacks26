# Simple FastAPI REST Controller

A minimal FastAPI application with basic CRUD operations.

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the server:**
   ```bash
   python main.py
   ```
   
   Or use uvicorn directly:
   ```bash
   uvicorn main:app --reload
   ```

3. **Access the API:**
   - API: http://localhost:8000
   - Documentation: http://localhost:8000/docs

## Endpoints

- `GET /` - Root endpoint
- `GET /items` - Get all items
- `GET /items/{id}` - Get specific item
- `POST /items` - Create new item
- `PUT /items/{id}` - Update item
- `DELETE /items/{id}` - Delete item

## Example Usage

```bash
# Get all items
curl http://localhost:8000/items

# Create an item
curl -X POST "http://localhost:8000/items" \
     -H "Content-Type: application/json" \
     -d '{"name": "New Item", "description": "Test item", "price": 15.99}'

# Get specific item
curl http://localhost:8000/items/1
```

