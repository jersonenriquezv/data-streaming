# Stream Project

A Dockerized microservice project for streaming and processing transactions using Python, RabbitMQ, MongoDB, and FastAPI.

## Project Structure

```
.
├── api/         # FastAPI service for querying transactions
├── consumer/    # Consumes transactions from RabbitMQ and stores in MongoDB
├── producer/    # Produces fake transactions and sends to RabbitMQ
├── models/      # Shared Pydantic models
├── docker-compose.yml
└── README.md
```

## Features

- **Producer:** Generates and sends fake transactions to RabbitMQ.
- **Consumer:** Listens to RabbitMQ, processes transactions, and stores them in MongoDB.
- **API:** FastAPI service to query and analyze stored transactions.

## Prerequisites

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/)

## Getting Started

1. **Clone the repository:**
   ```sh
   git clone <your-repo-url>
   cd stream-project
   ```

2. **Set up environment variables:**
   - Create a `.env` file in the root directory:
     ```
     rabbit_user=guest
     rabbit_pass=guest
     mongo_user=admin
     mongo_pass=password
     ```
   - **Note:** `.env` is in `.gitignore` and will not be committed.

3. **Build and start the services:**
   ```sh
   docker-compose up --build
   ```

4. **Access the services:**
   - **API:** [http://localhost:8000](http://localhost:8000)
   - **API Docs:** [http://localhost:8000/docs](http://localhost:8000/docs)
   - **RabbitMQ UI:** [http://localhost:15672](http://localhost:15672) (user/pass from `.env`)
   - **MongoDB:** localhost:27017 (user/pass from `.env`)

## Usage

- The **producer** will continuously generate and send transactions.
- The **consumer** will process and store them in MongoDB.
- Use the **API** to:
  - Get latest transactions: `/transactions/latest`
  - Get transaction stats: `/transactions/stats`
  - Get transactions by category: `/transactions/by-category`

## Development

- Shared models are in the `models/` directory.
- To add new endpoints or logic, edit the respective service directory.

## Security

- **Never commit your real `.env` file!**
- All sensitive credentials are loaded from environment variables.

## License

MIT License

---

**Feel free to modify this README to fit your needs!** 