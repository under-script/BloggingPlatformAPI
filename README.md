
# Blogging Platform API

This is an example API for a blogging platform using Django REST Framework.

## Endpoints

### 1. POST /posts/
Create a new post.
#### Request:
```json
{
  "title": "My First Blog Post",
  "content": "This is the content of my first blog post.",
  "category": 1,
  "tags": [1, 2]
}
```
#### Response:
```json
{
  "id": 1,
  "createdAt": "2024-10-01T08:58:25Z",
  "updatedAt": "2024-10-01T08:58:25Z",
  "title": "My First Blog Post",
  "content": "This is the content of my first blog post.",
  "category": 1,
  "tags": [1, 2]
}
```

### 2. PUT /posts/{id}/
Update an existing post.
#### Request:
```json
{
  "title": "My Updated Blog Post",
  "content": "This is the updated content of my first blog post.",
  "category": 2,
  "tags": [1, 2]
}
```
#### Response:
```json
{
  "id": 1,
  "createdAt": "2024-10-01T08:48:53Z",
  "updatedAt": "2024-10-01T08:51:21Z",
  "title": "My Updated Blog Post",
  "content": "This is the updated content of my first blog post.",
  "category": 2,
  "tags": [1, 2]
}
```

### 3. GET /posts/{id}/
Retrieve a specific post.
#### Response:
```json
{
  "id": 1,
  "createdAt": "2024-10-01T08:48:53Z",
  "updatedAt": "2024-10-01T08:51:21Z",
  "title": "My Updated Blog Post",
  "content": "This is the updated content of my first blog post.",
  "category": 2,
  "tags": [1, 2]
}
```

### 4. GET /posts/
List all posts.
#### Response:
```json
[
  {
    "id": 1,
    "createdAt": "2024-10-01T08:58:25Z",
    "updatedAt": "2024-10-01T08:58:25Z",
    "title": "My First Blog Post",
    "content": "This is the content of my first blog post.",
    "category": 1,
    "tags": [1, 2]
  },
  {
    "id": 2,
    "createdAt": "2024-10-01T08:59:34Z",
    "updatedAt": "2024-10-01T08:59:34Z",
    "title": "My Second Blog Post",
    "content": "This is the content of my second blog post.",
    "category": 1,
    "tags": [1, 2]
  }
]
```

### 5. GET /posts?term=tech
Search for posts containing a term.
#### Response:
```json
[
  {
    "id": 1,
    "createdAt": "2024-10-01T08:58:25Z",
    "updatedAt": "2024-10-01T08:58:25Z",
    "title": "My First Blog Post",
    "content": "This is the content of my first blog post.",
    "category": 1,
    "tags": [1, 2]
  },
  {
    "id": 2,
    "createdAt": "2024-10-01T08:59:34Z",
    "updatedAt": "2024-10-01T08:59:34Z",
    "title": "My Second Blog Post",
    "content": "This is the content of my second blog post.",
    "category": 1,
    "tags": [1, 2]
  }
]
```
