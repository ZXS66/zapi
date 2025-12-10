import json
import sys

import requests

API_TOKEN = "I'm blind, not dead."

# Sample knowledge points for programming topics
SAMPLE_KNOWLEDGE_POINTS = [
    {
        "stem": "What is the time complexity of binary search?",
        "answer": "O(log n)",
        "explanation": "Binary search divides the search space in half with each iteration, leading to logarithmic time complexity.",
        "tags": ["algorithms", "search", "complexity"],
        "topic": "Computer Science",
    },
    {
        "stem": "Explain the concept of 'immutability' in programming",
        "answer": "Immutability means an object's state cannot be changed after creation",
        "explanation": "Immutable objects are thread-safe and help prevent unintended side effects in functional programming.",
        "tags": ["programming", "functional", "concepts"],
        "topic": "Programming Concepts",
    },
    {
        "stem": "What is the difference between HTTP GET and POST?",
        "answer": "GET requests data, POST submits data",
        "explanation": "GET is idempotent and should not change server state, while POST is non-idempotent and typically creates or updates resources.",
        "tags": ["web", "http", "api"],
        "topic": "Web Development",
    },
    {
        "stem": "What is a primary key in database design?",
        "answer": "A unique identifier for each record in a table",
        "explanation": "Primary keys enforce entity integrity and are used to establish relationships between tables.",
        "tags": ["database", "sql", "design"],
        "topic": "Database",
    },
    {
        "stem": "Explain the concept of 'closure' in JavaScript",
        "answer": "A function that has access to variables in its outer scope",
        "explanation": "Closures allow functions to remember and access their lexical scope even when executed outside that scope.",
        "tags": ["javascript", "functions", "scope"],
        "topic": "JavaScript",
    },
    {
        "stem": "What is the purpose of the 'virtual DOM' in React?",
        "answer": "To optimize rendering performance by minimizing direct DOM manipulation",
        "explanation": "The virtual DOM is a lightweight copy of the real DOM that React uses to calculate the most efficient way to update the browser's DOM.",
        "tags": ["react", "frontend", "performance"],
        "topic": "Frontend Development",
    },
    {
        "stem": "What is the difference between synchronous and asynchronous programming?",
        "answer": "Synchronous executes sequentially, asynchronous allows concurrent execution",
        "explanation": "Synchronous code blocks until completion, while asynchronous code continues execution and handles results via callbacks, promises, or async/await.",
        "tags": ["programming", "concurrency", "async"],
        "topic": "Programming Concepts",
    },
    {
        "stem": "What is the CAP theorem in distributed systems?",
        "answer": "Consistency, Availability, Partition tolerance - can only achieve two at once",
        "explanation": "The CAP theorem states that in a distributed system, you can only guarantee two out of three: consistency, availability, and partition tolerance.",
        "tags": ["distributed-systems", "theory", "database"],
        "topic": "System Design",
    },
    {
        "stem": "What is dependency injection?",
        "answer": "A design pattern where dependencies are provided to objects rather than created internally",
        "explanation": "Dependency injection promotes loose coupling, testability, and maintainability by externalizing dependency management.",
        "tags": ["design-patterns", "architecture", "testing"],
        "topic": "Software Architecture",
    },
    {
        "stem": "What is the difference between SQL and NoSQL databases?",
        "answer": "SQL uses structured schema, NoSQL uses flexible schema",
        "explanation": "SQL databases are relational and use structured query language, while NoSQL databases are non-relational and offer flexible data models like document, key-value, graph, or column-family.",
        "tags": ["database", "sql", "nosql"],
        "topic": "Database",
    },
]


def import_sample_data(base_url: str):
    """Import sample knowledge points into the system."""
    # First, create a user or get existing user token
    user_token = "_n1LdwPkoqtOSAijbkN4tG4Ee8ixXcG3r_V40nBX4-g"

    # Use both global token and user bearer token
    headers = {
        "x-token": API_TOKEN,
        "Authorization": f"Bearer {user_token}"
    }
    imported_count = 0

    print(
        f"Starting import of {len(SAMPLE_KNOWLEDGE_POINTS)} sample knowledge points..."
    )

    for i, kp in enumerate(SAMPLE_KNOWLEDGE_POINTS, 1):
        try:
            response = requests.post(
                f"{base_url}/knowledge-points/", json=kp, headers=headers
            )
            if response.status_code == 200:
                print(
                    f"✅ [{i}/{len(SAMPLE_KNOWLEDGE_POINTS)}] Imported: {kp['stem'][:60]}..."
                )
                imported_count += 1
            else:
                print(
                    f"❌ [{i}/{len(SAMPLE_KNOWLEDGE_POINTS)}] Failed to import: {kp['stem'][:60]}..."
                )
                print(f"   Error: {response.status_code} - {response.text}")
        except requests.exceptions.RequestException as e:
            print(
                f"❌ [{i}/{len(SAMPLE_KNOWLEDGE_POINTS)}] Request failed: {kp['stem'][:60]}..."
            )
            print(f"   Exception: {e}")

    print(
        f"\nImport completed: {imported_count}/{len(SAMPLE_KNOWLEDGE_POINTS)} knowledge points imported successfully"
    )
    return imported_count


def main():
    if len(sys.argv) != 3:
        print("Usage: python import_sample_data.py <base_url> <global_token>")
        print(
            "Example: python import_sample_data.py http://localhost:8000 your_global_token_here"
        )
        print("\nNote: This script requires the global API token (ZAPI_TOKEN)")
        print("      It will create a 'sample_user' account for the import")
        sys.exit(1)

    base_url = sys.argv[1]
    token = sys.argv[2]

    print("Knowledge Review System - Sample Data Import")
    print("=" * 50)

    # Test connection first
    try:
        test_response = requests.get(
            f"{base_url}/", timeout=5, headers={"x-token": token}
        )
        if test_response.status_code != 200:
            print(f"❌ Cannot connect to API at {base_url}")
            sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot connect to API at {base_url}: {e}")
        sys.exit(1)

    # Import sample data
    imported_count = import_sample_data(base_url)

    if imported_count > 0:
        print(f"\n🎉 Successfully imported {imported_count} knowledge points!")
        print(
            f"📚 You can now use the preview and review features at {base_url}/preview/"
        )
    else:
        print(
            "\n❌ No knowledge points were imported. Please check your token and try again."
        )


if __name__ == "__main__":
    main()
