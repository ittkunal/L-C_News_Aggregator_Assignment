# News Aggregator Architecture

## Overview

The News Aggregator system is a layered Python application with a RESTful FastAPI backend and a CLI client. It fetches news from external APIs, stores them in MySQL, and provides user/admin features.

## Layers

- **API Layer:** FastAPI endpoints for all resources.
- **Controller Layer:** Handles business logic for each resource.
- **Repository Layer:** Handles all raw SQL queries to MySQL.
- **Service Layer:** Handles external API calls, categorization, email, and notifications.
- **Client Layer:** CLI app for user/admin interaction.

## Data Flow

1. **News Fetching:**  
   - Scheduled job fetches news from APIs, categorizes, and stores in MySQL.
2. **User Actions:**  
   - CLI client sends HTTP requests to FastAPI server.
   - Server authenticates, processes, and responds.
3. **Notifications:**  
   - Users configure keywords/categories.
   - Batch job sends email and in-app notifications.

## Database

- MySQL with tables for users, articles, saved_articles, notifications, categories, likes_dislikes, external_sources, sessions.

## Security

- Passwords are hashed.
- No JWT/session tokens; session state is managed in the CLI.

## Clean Code

- Follows SOLID, Clean Code, and Layered Architecture principles.