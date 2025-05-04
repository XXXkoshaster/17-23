# Project of team 17-23 for mathmod
## PSB - credit scoring
* [Ресерч док по кейсу ПСБ](https://docs.google.com/document/d/1-uWhCeIS3wtv3wlk4lqF3tTfYcO5R-v2-RwjUiRDLU4/edit?usp=sharing)
* [Данные](https://www.kaggle.com/competitions/matmod-it-psb/data)

A microservices-based system for analyzing chess videos, generating commentary, and creating enhanced video content.

## Friflrex - tik-tok

The system consists of multiple microservices working together:
- **Frontend**: Streamlit-based web interface
- **API Gateway**: FastAPI service handling requests and job management
- **PGN Parser**: Analyzes chess games using Stockfish
- **LLM Worker**: Generates commentary using Qwen2.5-14B-Instruct
- **Message Broker**: RabbitMQ for inter-service communication
- **Storage**: MinIO for file storage
- **Cache**: Redis for job state managementx