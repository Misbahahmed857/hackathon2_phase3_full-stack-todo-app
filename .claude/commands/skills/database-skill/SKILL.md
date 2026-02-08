# Database Skill

## Purpose
Design schemas, manage relationships, optimize queries with SQLModel and Neon Serverless PostgreSQL.

## Capabilities
- **Schema Design**: SQLModel models with proper types and relationships
- **Relationships**: Foreign keys, one-to-many, many-to-many with proper constraints
- **Migrations**: SQLModel create_all or migration tools compatible with Neon
- **Query Optimization**: Indexes, efficient joins, connection pooling for serverless
- **Data Integrity**: Constraints, cascading deletes, validation at database level
- **Neon Features**: Database branching, autoscaling, serverless connection management

## Core Patterns
**User Table**: id (UUID/Integer), email (unique, indexed), password_hash, created_at, updated_at
**Multi-tenancy**: All tables include user_id foreign key with index
**Indexing**: Index on frequently queried fields (user_id, email, created_at)
**Timestamps**: All tables include created_at and updated_at columns

## Best Practices for Neon
- Use UUID for primary keys (security) or auto-incrementing integers (performance)
- Add timestamps (created_at, updated_at) with timezone awareness
- Define cascading rules for deletes (CASCADE, SET NULL, RESTRICT)
- Use database constraints for data integrity (UNIQUE, NOT NULL, CHECK)
- Implement connection pooling (PgBouncer or Neon's built-in pooling)
- Use Neon branches for testing schema changes before production
- Optimize for serverless: minimize connection overhead, use connection pooling
- Store connection strings in environment variables
- Design with autoscaling in mind (efficient queries for variable load)

## Neon-Specific Considerations
- **Connection Management**: Use pooled connections to handle serverless cold starts
- **Branching**: Create database branches for safe schema testing
- **Autoscaling**: Design queries that perform well under variable compute resources
- **Instant Provisioning**: Leverage quick database creation for development/testing
- **Connection Strings**: Use Neon's pooled connection strings for production

## Migration Strategy
- Use SQLModel's `create_all()` for initial schema creation
- For complex migrations, use compatible tools or manual SQL scripts
- Test all migrations in Neon development branches first
- Document schema changes for team coordination