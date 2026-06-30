# LeetCode Interview Intelligence

A data-driven interview preparation platform for company-wise LeetCode problem search, progress tracking, and analytics.

---

## Overview

Preparing for coding interviews usually involves solving hundreds of problems across multiple companies and topics.  
The main challenges are:

- Finding company-specific important questions
- Prioritizing frequently asked interview problems
- Tracking solved vs unsolved questions
- Identifying weak areas for improvement

LeetCode Interview Intelligence solves this by providing structured problem retrieval, filtering, and progress tracking in one platform.

This is the **Version 1 (V1)** release focused on:
- large-scale data ingestion
- structured retrieval
- user progress tracking

---

## Features (V1)

### Authentication
- User signup
- User login

### Problem Search
- Company-wise problem search
- Topic filtering
- Difficulty filtering
- Result limiting

### Problem Ranking
- Frequency-based ranking
- High-priority problems shown first

### Progress Tracking
- Mark problems as solved
- Track solved vs unsolved problems
- Hide solved questions from results

### Data Pipeline
- Automated CSV ingestion pipeline
- Handles large-scale company datasets
- Supports missing/inconsistent CSV data

---

## Tech Stack

- Python
- postgresql
- Pandas
- Gradio

---

## Project Structure

```bash
leetcode-interview-intelligence/
│
├── app.py
├── requirements.txt
│
├── auth/
│   └── auth.py
│
├── database/
│   ├── db.py
│   └── schema.py
│
├── scripts/
│   └── ingest.py
│
├── search/
│   └── search_engine.py
│
├── tracker/
│   └── progress.py
│
└── stats.py
```

---

## Architecture

```text
Raw CSV Dataset
      ↓
Data Ingestion Pipeline
      ↓
SQLite Database
      ↓
Search Engine
      ↓
Gradio UI
```

---

## Database Schema

The project uses a normalized relational database design.

### Core Tables
- users
- problems
- companies
- topics

### Mapping Tables
- problem_companies
- problem_topics
- user_solved_problems

This enables efficient many-to-many relationships:
- One problem can belong to multiple companies
- One problem can belong to multiple topics

---

## Search Workflow

1. User selects filters:
   - Company
   - Topic
   - Difficulty

2. Dynamic SQL query is generated

3. Matching problems are ranked by frequency

4. Results displayed via Gradio UI

---

## Engineering Challenges Solved

- Large-scale CSV ingestion across hundreds of companies
- Handling inconsistent dataset formats
- Database normalization for scalable retrieval
- Efficient SQL joins for filtering and ranking
- User progress tracking

---

## Future Roadmap

### V2
- Analytics dashboard
- Topic distribution insights
- Company trend analysis

### V3
- Semantic search using embeddings
- Similar problem recommendations

### V4
- RAG-powered intelligent retrieval
- Personalized interview preparation

### V5
- Agentic AI Interview Coach using LangChain / LangGraph

Planned capabilities:
- Readiness score prediction
- Weak topic analysis
- Personalized preparation roadmap
- AI-powered interview guidance

---

## Note

This project is still in progress, so the current files in this repository are incomplete and may not run properly if cloned.

If you want to test the current version, please use the live link below:

**Project Link:** https://huggingface.co/spaces/TrailBlazer108/leetcode-interview-intelligence

Full source code and setup instructions will be added once development is complete.


---

## Current Status

Version: **V1 Release**

Current focus:
- Stable search
- Efficient retrieval
- Progress tracking

Next milestone:
- AI-powered interview intelligence
