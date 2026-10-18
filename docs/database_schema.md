# Database schema

No domain tables are defined yet because product entities and retention requirements have not been specified. SQLAlchemy's declarative base, engine, session factory, and Alembic migration environment are initialized. Do not interpret this as persistence being active: current API routes do not use sessions, and no initial domain migration exists.

Future schema design should define ownership, scan and provider evidence records, retention/deletion policy, indexes, and any personally identifiable information before adding models and migrations. Apply migrations explicitly with Alembic after defining them.
