# Scalability and Growth Notes – VeriCourt System

This document explains how the VeriCourt system can handle more users, more evidence, and future growth without breaking.

## Stateless Backend Design

The evidence registration and verification services are stateless.
This means they do not store user data in memory.

Because of this:
- Multiple backend instances can run at the same time
- Load can be shared easily
- The system can handle more requests without changing logic

## Hashing and Verification Scalability

Hash generation and verification are independent operations.
Each evidence file is processed separately.

Because of this:
- Hashing can be done in parallel
- One slow request does not block others
- Verification can scale with demand

## Event-Based Processing for Growth

After evidence is registered, the system can trigger internal events.
Examples include risk evaluation and integrity checks.

This allows:
- Heavy tasks to run in the background
- Faster user responses
- Easy addition of new processing steps in the future

## Database Growth Strategy

The system starts with SQLite for simplicity.
As usage increases, the database can be migrated to a stronger system.

Possible future upgrades:
- PostgreSQL for larger datasets
- Separate read and write operations
- Indexed access for faster searches

## Optimizing Court and Judge Access

Court reports are read more often than they are written.
This allows:
- Caching of reports
- Faster access for judges
- Reduced load on core services

These scalability choices ensure that VeriCourt can grow from a small prototype into a reliable, court-ready system.
