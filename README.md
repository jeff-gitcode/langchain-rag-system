# Simple LangChain Retrieval-Augmented Generation System

This project implements a Retrieval-Augmented Generation (RAG) system using LangChain and a vector database. The architecture follows Clean Architecture principles and employs the Command Query Responsibility Segregation (CQRS) pattern.

## Project Structure

```
langchain-rag-system
├── src
│   ├── application
│   │   ├── commands
│   │   │   └── ingest_data.py
│   │   ├── queries
│   │   │   └── retrieve_data.py
│   ├── domain
│   │   ├── entities
│   │   │   └── document.py
│   │   └── repositories
│   │       └── vector_db_repository.py
│   ├── infrastructure
│   │   ├── database
│   │   │   └── vector_db.py
│   │   └── services
│   │       └── langchain_service.py
│   ├── presentation
│   │   ├── api
│   │   │   └── main.py
│   │   └── cli
│   │       └── commands.py
│   └── tests
│       ├── test_application
│       ├── test_domain
│       ├── test_infrastructure
│       └── test_presentation
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```
## Features

- **Ingestion**: Add documents to a FAISS-based vector database with metadata.
- **Retrieval**: Perform similarity searches using Sentence Transformers to retrieve relevant documents.
- **LangChain Integration**: Placeholder for LangChain-based processing and response generation.
- **Clean Architecture**: Separation of concerns with clearly defined layers (Application, Domain, Infrastructure, Presentation).
- **CQRS Pattern**: Commands for ingestion and queries for retrieval.

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone https://github.com/yourusername/langchain-rag-system.git
   cd langchain-rag-system
   ```

2. **Create a virtual environment:**
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   Create a `.env` file in the root directory and add your configuration settings, such as database connection strings and API keys.

5. **Run the Application:**

#### Start the API Server

```bash
uvicorn src.presentation.api.main:app --reload
```

Access the API documentation at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

6. **Testing:**

Run the tests using `pytest`:

```bash
pytest src/tests
```

#### Test the API Endpoints

Use the `apitest/api.http` file with the REST Client extension in Visual Studio Code to test the `/ingest` and `/retrieve` endpoints.

## Usage

### Ingesting Data

To ingest data into the vector database, use the command line interface:

```
python src/presentation/cli/commands.py ingest --file path/to/data.json
```

### Retrieving Data

To retrieve data based on specific criteria, use the following command:

```
python src/presentation/cli/commands.py retrieve --query "your search query"
```

## Testing

To run the tests, execute:

```
pytest src/tests
```

## Contributing

Feel free to submit issues or pull requests to improve the project. Please ensure that your contributions adhere to the project's coding standards and include appropriate tests.

## License

This project is licensed under the MIT License. See the LICENSE file for details.