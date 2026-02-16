# 🏆 Hackathon Dashboard

A full-stack hackathon dashboard platform built with Nuxt 3 (frontend) and FastAPI (backend). Users can authenticate with GitHub, create projects, browse hackathons, vote on projects, and engage with community comments.

## ✨ Features

- **GitHub OAuth Authentication**: Secure login using GitHub accounts with JWT token management
- **Project Management**: Create, browse, edit, and manage hackathon projects with rich markdown descriptions
- **Hackathon Discovery**: View upcoming and past hackathon events with interactive maps and registration
- **Voting System**: Upvote/downvote projects and comments with real-time vote tracking
- **Comment System**: Nested comment threads with reply functionality and user mentions
- **Responsive Dashboard**: Modern UI with Tailwind CSS, fully responsive across all viewports
- **Interactive Maps**: OpenStreetMap integration for hackathon location visualization
- **User Profiles**: Personal dashboards showing projects, votes, and activity statistics
- **Email Notifications**: Automated email service for user notifications
- **RESTful API**: FastAPI backend with SQLAlchemy ORM and automatic OpenAPI documentation
- **Database**: SQLite for development (PostgreSQL ready for production)

## 🛠️ Tech Stack

### Frontend (`frontend3/`)
- **Nuxt 3** (v4.3.1) - Vue.js framework with SSR and file-based routing
- **Vue 3** (v3.5.28) - Composition API with `<script setup>` syntax
- **TypeScript** (v5.3.0) - Type safety and modern JavaScript features
- **Tailwind CSS** (v3.4.0) - Utility-first CSS framework with responsive design
- **Pinia** (v3.0.4) - State management with stores for auth, UI, voting, and themes
- **Axios** (v1.6.0) - HTTP client for API communication
- **date-fns** (v3.6.0) - Modern date utility library
- **pnpm** - Fast, disk space efficient package manager

### Backend (`backend/`)
- **FastAPI** (v0.104.1) - Modern Python web framework with automatic API docs
- **SQLAlchemy** (v2.0.23) - ORM for database operations with async support
- **SQLite** - Development database (PostgreSQL production-ready)
- **JWT** (python-jose v3.3.0) - JSON Web Tokens for authentication
- **Pydantic** (v2.5.0) - Data validation and settings management
- **Alembic** (v1.13.1) - Database migration tool
- **httpx** (v0.25.2) - Async HTTP client for external API calls
- **OpenStreetMap/Nominatim** - Geocoding and map integration

## 📁 Project Structure

```
hackathon-dashboard/
├── backend/                    # FastAPI backend
│   ├── main.py                # FastAPI application with all endpoints
│   ├── models.py              # SQLAlchemy models (User, Project, Hackathon, Comment, Vote)
│   ├── schemas.py             # Pydantic schemas for request/response validation
│   ├── crud.py                # Database operations and business logic
│   ├── auth.py                # Authentication logic and JWT token management
│   ├── github_oauth.py        # GitHub OAuth integration
│   ├── geocoding.py           # OpenStreetMap geocoding service
│   ├── email_service.py       # Email notification service
│   ├── database.py            # Database configuration and session management
│   ├── requirements.txt       # Python dependencies
│   ├── Dockerfile             # Backend Docker configuration
│   ├── .env                   # Environment variables (gitignored)
│   ├── .gitignore             # Python-specific gitignore
│   └── hackathon.db           # SQLite database (gitignored)
├── frontend3/                  # Nuxt 3 frontend
│   ├── app/
│   │   ├── app.vue            # Root layout and global components
│   │   ├── pages/             # File-based routing pages
│   │   │   ├── index.vue      # Homepage with featured projects
│   │   │   ├── about.vue      # About page
│   │   │   ├── create.vue     # Project creation form
│   │   │   ├── profile.vue    # User profile dashboard
│   │   │   ├── my-projects.vue # User's projects
│   │   │   ├── my-votes.vue   # User's voting history
│   │   │   ├── hackathons/    # Hackathon-related pages
│   │   │   │   ├── index.vue  # Hackathon listing
│   │   │   │   └── [id]/      # Dynamic hackathon pages
│   │   │   └── projects/      # Project-related pages
│   │   │       ├── index.vue  # Project listing
│   │   │       └── [id]/      # Dynamic project pages
│   │   ├── components/        # Reusable Vue components
│   │   │   ├── AppHeader.vue  # Navigation header
│   │   │   ├── AppFooter.vue  # Site footer
│   │   │   ├── VoteButtons.vue # Upvote/downvote buttons
│   │   │   └── NotificationContainer.vue # Toast notifications
│   │   ├── stores/            # Pinia state stores
│   │   │   ├── auth.ts        # Authentication state
│   │   │   ├── ui.ts          # UI state and notifications
│   │   │   ├── voting.ts      # Voting state
│   │   │   └── theme.ts       # Theme preferences
│   │   ├── assets/css/        # Global CSS styles
│   │   │   └── main.css       # Tailwind imports and custom styles
│   │   └── plugins/           # Nuxt plugins
│   │       └── click-outside.ts # Click outside directive
│   ├── nuxt.config.ts         # Nuxt configuration
│   ├── tailwind.config.js     # Tailwind CSS configuration
│   ├── tsconfig.json          # TypeScript configuration
│   ├── package.json           # Frontend dependencies
│   ├── pnpm-lock.yaml         # Lockfile for pnpm
│   ├── .env                   # Frontend environment variables
│   └── .gitignore             # Frontend-specific gitignore
├── docker-compose.yml         # Docker Compose configuration for full stack
├── package-lock.json          # Root package lock (legacy)
├── test_setup.sh              # Test setup script
└── README.md                  # This file
```

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- GitHub OAuth App (for authentication)
- pnpm (optional, for local frontend development)

### 1. Clone the repository
```bash
git clone <repository-url>
cd hackathon-dashboard
```

### 2. Set up GitHub OAuth
1. Go to [GitHub Developer Settings](https://github.com/settings/developers)
2. Create a new OAuth App
3. Set Homepage URL: `http://localhost:3001`
4. Set Authorization callback URL: `http://localhost:8000/api/auth/github/callback`
5. Copy Client ID and Client Secret

### 3. Configure environment variables

**Backend configuration:**
```bash
cd backend
cp .env.example .env  # If you have an example file
# Or create manually:
echo "GITHUB_CLIENT_ID=your-client-id" >> .env
echo "GITHUB_CLIENT_SECRET=your-client-secret" >> .env
echo "SECRET_KEY=your-secret-key-here" >> .env
echo "DATABASE_URL=sqlite:///./hackathon.db" >> .env
```

**Frontend configuration:**
```bash
cd frontend3
echo "NUXT_PUBLIC_API_URL=http://localhost:8000" >> .env
```

### 4. Start with Docker Compose
```bash
# Build and start all services
docker-compose up --build -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

The application will be available at:
- **Frontend**: http://localhost:3001
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs (Swagger UI)
- **Alternative Docs**: http://localhost:8000/redoc (ReDoc)

## 💻 Development Setup

### Backend Development
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Run backend with hot reload
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Development
```bash
cd frontend3

# Install dependencies with pnpm (recommended)
pnpm install

# Or with npm
npm install

# Run frontend with hot reload
pnpm dev  # or npm run dev
```

## 📡 API Endpoints

### Authentication
- `GET /api/auth/github` - Initiate GitHub OAuth flow
- `GET /api/auth/github/callback` - GitHub OAuth callback
- `GET /api/users/me` - Get current user info (authenticated)
- `GET /api/users/me/projects` - Get current user's projects
- `GET /api/users/me/votes` - Get current user's votes
- `GET /api/users/me/stats` - Get current user's statistics

### Projects
- `GET /api/projects` - List all projects with pagination
- `POST /api/projects` - Create a new project (authenticated)
- `GET /api/projects/{id}` - Get project details
- `PUT /api/projects/{id}` - Update a project (owner only)
- `DELETE /api/projects/{id}` - Delete a project (owner only)
- `POST /api/projects/{id}/view` - Increment project view count
- `GET /api/projects/{id}/vote-stats` - Get project vote statistics

### Voting
- `POST /api/projects/{id}/vote` - Vote on a project (upvote/downvote)
- `DELETE /api/projects/{id}/vote` - Remove vote from a project
- `POST /api/comments/{id}/vote` - Vote on a comment
- `DELETE /api/comments/{id}/vote` - Remove vote from a comment

### Comments
- `GET /api/projects/{id}/comments` - Get comments for a project (with nested replies)
- `POST /api/projects/{id}/comments` - Add a comment to a project
- `PUT /api/comments/{id}` - Update a comment (author only)
- `DELETE /api/comments/{id}` - Delete a comment (author only)

### Hackathons
- `GET /api/hackathons` - List all hackathons
- `POST /api/hackathons` - Create a new hackathon (authenticated)
- `GET /api/hackathons/{id}` - Get hackathon details
- `PUT /api/hackathons/{id}` - Update a hackathon
- `GET /api/hackathons/{id}/projects` - Get projects for a hackathon
- `GET /api/hackathons/{id}/participants` - Get participants for a hackathon
- `POST /api/hackathons/{id}/register` - Register for a hackathon
- `DELETE /api/hackathons/{id}/unregister` - Unregister from a hackathon

### Health & Utility
- `GET /` - API welcome message
- `GET /api/health` - Health check endpoint

## 🐳 Docker Deployment

### Production Deployment
```bash
# Build and run with Docker Compose
docker-compose up --build -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Remove volumes (including database)
docker-compose down -v
```

### Production Considerations
1. **Database**: Use PostgreSQL in production by updating `DATABASE_URL` in backend `.env`
2. **Security**: Set strong `SECRET_KEY` for JWT tokens and use HTTPS
3. **CORS**: Configure proper CORS origins for your production domain
4. **Environment Variables**: Use environment variables for all sensitive data
5. **Monitoring**: Set up logging, monitoring, and alerting
6. **Backups**: Implement regular database backups
7. **Scaling**: Consider container orchestration (Kubernetes) for high traffic

## 🔧 Environment Variables

### Backend (`backend/.env`)
```env
# Database
DATABASE_URL=sqlite:///./hackathon.db  # Development
# DATABASE_URL=postgresql://user:password@localhost/hackathon_db  # Production

# JWT Authentication
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# GitHub OAuth
GITHUB_CLIENT_ID=your-client-id
GITHUB_CLIENT_SECRET=your-client-secret
GITHUB_CALLBACK_URL=http://localhost:8000/api/auth/github/callback

# Frontend URL for CORS
FRONTEND_URL=http://localhost:3001

# Email Configuration (optional)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
EMAIL_FROM=noreply@hackathondashboard.com
```

### Frontend (`frontend3/.env`)
```env
# API Base URL
NUXT_PUBLIC_API_URL=http://localhost:8000
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

### Development Guidelines
- Follow existing code style and conventions
- Write tests for new functionality
- Update documentation for API changes
- Use meaningful commit messages
- Ensure responsive design for all UI components

## 📄 License

MIT License - see LICENSE file for details

## 🆘 Support

For issues and questions:
1. Check the [API documentation](http://localhost:8000/docs) for endpoint details
2. Review the browser console and network tabs for frontend errors
3. Check Docker logs: `docker-compose logs -f`
4. Open an issue on the GitHub repository with detailed reproduction steps

## 🎯 Roadmap & Future Features

- [ ] Real-time notifications with WebSockets
- [ ] Project search and filtering
- [ ] Advanced analytics dashboard
- [ ] Team collaboration features
- [ ] Project submission deadlines
- [ ] Hackathon judging system
- [ ] Mobile app with PWA support
- [ ] Internationalization (i18n)
- [ ] Dark/light theme toggle
- [ ] Export data functionality