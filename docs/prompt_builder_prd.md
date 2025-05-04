# Prompt Builder - Product Requirements Document

## 1. Project Overview

### 1.1 Project Information
- **Project Name**: Prompt Builder
- **Version**: 1.0.0
- **Last Updated**: May 4, 2025

### 1.2 Objective
Create an interactive web application that assists prompt engineers in generating detailed, well-structured prompts through a guided question-based interface. The system will help users create comprehensive prompts by collecting essential information such as roles, objectives, examples, and target users.

### 1.3 Target Users
Primary users are prompt engineers who need to:
- Create structured prompts for AI models
- Maintain consistency in prompt formatting
- Include all necessary context and requirements
- Generate documentation for their prompts

### 1.4 System Context
- **Application Type**: Web Application
- **Deployment**: Docker-based
- **Architecture**: Microservices
- **Primary Framework**: Streamlit (UI)
- **Backend**: Python with LangChain
- **Model Integration**: Configurable through environment variables

## 2. Functional Requirements

### 2.1 Core Features

#### 2.1.1 Prompt Template Builder
- Interactive form-based interface for prompt creation
- Dynamic question generation based on prompt type
- Template selection for different use cases
- Real-time preview of generated prompt

#### 2.1.2 Prompt Components
Required Fields:
- Role/Context
- Primary Objective
- Target Audience
- Input Format
- Output Requirements
- Constraints/Limitations

Optional Fields:
- Examples
- Reference Materials
- Success Criteria
- Error Handling
- Style Guidelines

#### 2.1.3 Model Configuration
- Environment-based model selection
- API key management
- Model-specific parameter configuration
- Usage tracking and logging

#### 2.1.4 Export and Share
- Export prompts in multiple formats (MD, JSON, TXT)
- Share prompts via URL
- Version control for prompts
- Template library management

### 2.2 User Flows

1. **Prompt Creation Flow**
   - Select prompt type/template
   - Fill required fields
   - Add optional components
   - Preview generated prompt
   - Export/Save prompt

2. **Template Management Flow**
   - Create custom templates
   - Modify existing templates
   - Share templates
   - Import templates

3. **Configuration Flow**
   - Set up environment variables
   - Configure model settings
   - Manage API keys
   - Set default parameters

## 3. Technical Specifications

### 3.1 Technology Stack

#### Frontend
- **Framework**: Streamlit
- **Features**:
  - Responsive design
  - Real-time preview
  - Form validation
  - Markdown support

#### Backend
- **Language**: Python 3.9+
- **Framework**: FastAPI
- **Libraries**:
  - LangChain
  - Pydantic
  - Python-dotenv
  - SQLAlchemy

#### Infrastructure
- **Containerization**: Docker
- **Orchestration**: Docker Compose
- **Database**: PostgreSQL
- **Cache**: Redis

### 3.2 System Architecture

```
├── Docker Environment
│   ├── Frontend Container (Streamlit)
│   ├── Backend Container (FastAPI)
│   ├── Database Container (PostgreSQL)
│   └── Cache Container (Redis)
```

### 3.3 API Structure

#### REST API Endpoints
- `/api/v1/prompts`: CRUD operations for prompts
- `/api/v1/templates`: Template management
- `/api/v1/config`: System configuration
- `/api/v1/models`: Model management

#### WebSocket Endpoints
- `/ws/preview`: Real-time prompt preview
- `/ws/validation`: Live validation feedback

### 3.4 Data Models

```python
class Prompt:
    id: UUID
    title: str
    type: PromptType
    components: Dict[str, Any]
    metadata: Dict[str, Any]
    version: str
    created_at: datetime
    updated_at: datetime

class Template:
    id: UUID
    name: str
    structure: Dict[str, Any]
    required_fields: List[str]
    optional_fields: List[str]
```

### 3.5 Docker Compose Requirements

Specify the docker-compose setup for all services:

```yaml
version: '3.8'
services:
  frontend:
    build: ./frontend
    ports:
      - "8501:8501"
    environment:
      - MODEL_PROVIDER
      - OPENAI_API_KEY
    depends_on:
      - backend
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8501/_stcore/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    logging:
      driver: "json-file"
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL
      - REDIS_URL
    depends_on:
      - db
      - redis
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    logging:
      driver: "json-file"
  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=prompt_builder
      - POSTGRES_USER=admin
      - POSTGRES_PASSWORD=secret
    volumes:
      - db_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U admin"]
      interval: 30s
      timeout: 10s
      retries: 5
  redis:
    image: redis:7
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 30s
      timeout: 10s
      retries: 5
volumes:
  db_data:
  redis_data:
```

### 3.6 .env File Usage

- All sensitive and environment-specific variables must be set in a `.env` file at the project root.
- Each service loads only the variables it needs.
- Example variables:
  - `OPENAI_API_KEY`, `MODEL_PROVIDER`, `MODEL_NAME`, `DATABASE_URL`, `REDIS_URL`, `DEBUG`, `LOG_LEVEL`, `MAX_TOKENS`
- Do not commit `.env` to version control.

### 3.7 Healthcheck and Logging

- Each service must implement a Docker healthcheck endpoint.
- All logs should be output to stdout/stderr for Docker compatibility and aggregated using the default logging driver.

### 3.8 Automated Initialization

- Database initialization scripts should be placed in `/docker/initdb/` and mounted to the db container.
- Backend should check and run migrations on startup.

### 3.9 AI Model Selection

- Model selection is controlled by environment variables (`MODEL_PROVIDER`, `MODEL_NAME`).
- If not set, the backend must return a clear error and not start.
- Fallbacks or defaults should be documented.

### 3.10 Security Best Practices

- Never store sensitive keys in the repository.
- Use Docker secrets or environment variables for production deployments.
- Ensure all API endpoints are protected as required.

### 3.11 Testing in Docker

- Provide a test target in docker-compose:
  - Example: `docker-compose run backend pytest`
- All tests should be runnable in the containerized environment.

### 3.12 API Versioning

- All API endpoints must be versioned (e.g., `/api/v1/`).
- Future versions should not break existing clients.

### 3.13 Documentation Build and Access

- API documentation (Swagger/OpenAPI) should be available at `/api/docs`.
- User and developer documentation should be built as static files and served from `/docs` or included in the repo.

### 3.14 CI/CD Pipeline

- Implement a basic CI/CD pipeline for:
  - Linting and static analysis
  - Building and testing Docker images
  - Running tests
  - Deploying to staging/production
- Example tools: GitHub Actions, GitLab CI, or similar.

## 4. Non-Functional Requirements

### 4.1 Performance
- Page load time: < 2 seconds
- Prompt generation: < 1 second
- API response time: < 500ms
- Support for 100 concurrent users

### 4.2 Security
- Environment-based secrets management
- API key encryption
- Rate limiting
- Input sanitization
- CORS configuration
- Authentication and authorization

### 4.3 Reliability
- System uptime: 99.9%
- Automated backups
- Error logging and monitoring
- Failover mechanisms

### 4.4 Scalability
- Horizontal scaling support
- Load balancing
- Database sharding capability
- Caching strategy

## 5. Documentation Requirements

### 5.1 API Documentation
- OpenAPI/Swagger documentation
- API endpoint descriptions
- Request/response examples
- Authentication details
- Rate limiting information

### 5.2 User Documentation
- Getting started guide
- Prompt creation tutorial
- Template management guide
- Configuration instructions
- Troubleshooting guide

### 5.3 Developer Documentation
- System architecture overview
- Setup instructions
- Development guidelines
- Testing procedures
- Deployment process
- Contributing guidelines

## 6. Development and Deployment

### 6.1 Development Environment
```bash
# Directory Structure
prompt_builder/
├── frontend/          # Streamlit application
├── backend/           # FastAPI service
├── docker/           # Docker configurations
├── docs/             # Documentation
├── tests/            # Test suites
└── scripts/          # Utility scripts
```

### 6.2 Environment Variables
```plaintext
# Required Environment Variables
OPENAI_API_KEY=xxx
MODEL_PROVIDER=openai
MODEL_NAME=gpt-4
DATABASE_URL=postgresql://...
REDIS_URL=redis://...

# Optional Environment Variables
DEBUG=false
LOG_LEVEL=INFO
MAX_TOKENS=2000
```

### 6.3 Deployment Process
1. Environment configuration
2. Docker image building
3. Container orchestration
4. Database migrations
5. Health checks
6. Monitoring setup

## 7. Testing Requirements

### 7.1 Test Types
- Unit tests
- Integration tests
- End-to-end tests
- Performance tests
- Security tests

### 7.2 Test Coverage
- Minimum 80% code coverage
- Critical path testing
- Edge case validation
- Error handling verification

## 8. Maintenance and Support

### 8.1 Monitoring
- System health metrics
- Usage statistics
- Error tracking
- Performance monitoring
- Resource utilization

### 8.2 Updates and Versioning
- Semantic versioning
- Changelog maintenance
- Update documentation
- Migration guides

## 9. Success Metrics

### 9.1 Technical Metrics
- System uptime
- Response times
- Error rates
- API usage statistics

### 9.2 User Metrics
- User engagement
- Prompt quality scores
- Template usage statistics
- User satisfaction ratings

## 10. Timeline and Milestones

### Phase 1: Core Development (4 weeks)
- Basic UI implementation
- Core prompt building functionality
- Database setup
- Docker configuration

### Phase 2: Enhanced Features (3 weeks)
- Template system
- Export functionality
- API documentation
- User documentation

### Phase 3: Testing and Optimization (2 weeks)
- Testing implementation
- Performance optimization
- Security hardening
- Documentation completion

### Phase 4: Deployment and Launch (1 week)
- Production deployment
- Monitoring setup
- Final testing
- Launch preparation