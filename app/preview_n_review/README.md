
## Preview & Review System Features

- **Preview Sessions**: Get new knowledge points to study in the morning
- **Review Sessions**: Reinforce previously learned material in the afternoon/evening
- **Knowledge Management**: Create, search, import, and export knowledge points
- **Progress Tracking**: Track learning progress with confidence levels
- **Tag-based Organization**: Organize knowledge points by topics and tags
- **Bearer Token Authentication**: Simple user identification system

## Using the Preview & Review System

1. **Access the API**: All preview-review endpoints are under `/api/preview-review/`
2. **Register a user**:
   ```bash
   curl -X POST "http://localhost:8000/api/preview-review/users/" \
     -H "Content-Type: application/json" \
     -d '{"username": "your_username"}'
   ```
3. **Import sample data**:
   ```bash
   python app/preview_n_review/scripts/import_sample_data.py \
     http://localhost:8000 YOUR_TOKEN
   ```


## Preview & Review System API Endpoints

### Users & Sessions

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/preview-review/users/` | Register new user |
| GET | `/api/preview-review/preview/` | Get morning preview session |
| GET | `/api/preview-review/review/` | Get evening review session |

### Knowledge Management

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/preview-review/knowledge-points/` | Get user's knowledge points |
| POST | `/api/preview-review/knowledge-points/` | Create new knowledge point |
| GET | `/api/preview-review/knowledge-points/search/` | Search knowledge points |
| POST | `/api/preview-review/knowledge-points/import/` | Batch import knowledge points |
| GET | `/api/preview-review/knowledge-points/export/` | Export user's knowledge points |

### Progress & Learning

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/preview-review/progress/` | Record review progress |

## Usage Examples (Preview & Review System)

### 1. Register a User (Preview & Review System)

```bash
curl -X POST "http://localhost:8000/api/preview-review/users/" \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser"}'
```

Response:
```json
{
  "id": 1,
  "username": "testuser",
  "token": "your-authentication-token",
  "created_at": "2024-01-01T10:00:00"
}
```

### 2. Import Sample Data (Preview & Review System)

```bash
python app/preview_n_review/scripts/import_sample_data.py http://localhost:8000 your-token-here
```

### 3. Get Preview Session (Preview & Review System)

```bash
curl -X GET "http://localhost:8000/api/preview-review/preview/" \
  -H "Authorization: Bearer your-token-here"
```

### 4. Record Progress (Preview & Review System)

```bash
curl -X POST "http://localhost:8000/api/preview-review/progress/?knowledge_point_id=1&confidence_level=4" \
  -H "Authorization: Bearer your-token-here"
```

## Knowledge Point Structure (Preview & Review System)

Each knowledge point contains:

- **stem**: The question or concept
- **answer**: The correct answer
- **explanation**: Detailed explanation (optional)
- **tags**: List of tags for categorization
- **topic**: Main topic/category

Example:
```json
{
  "stem": "What is the time complexity of binary search?",
  "answer": "O(log n)",
  "explanation": "Binary search divides the search space in half with each iteration...",
  "tags": ["algorithms", "search", "complexity"],
  "topic": "Computer Science"
}
```

## Database Schema (Preview & Review System)

- **users**: User accounts and authentication tokens
- **knowledge_points**: Knowledge content with metadata
- **user_progress**: Learning progress and spaced repetition scheduling
