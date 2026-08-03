# RoadVision
> **AI-Powered Intelligent Road Damage Detection & Monitoring System**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Flutter](https://img.shields.io/badge/Flutter-3.x-02569B?logo=flutter)](https://flutter.dev)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-009688?logo=fastapi)](https://fastapi.tiangolo.com)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.x-EE4C2C?logo=pytorch)](https://pytorch.org)
[![PostGIS](https://img.shields.io/badge/PostGIS-3.3-336791?logo=postgis)](https://postgis.net)

## Overview
**RoadVision** is a mobile-first Smart City application that leverages Computer Vision to automatically detect and monitor road damage from dual sources:
- **Citizen reports**: Crowdsourced camera captures with automated location.
- **Government vehicle-mounted cameras**: Continuous dashcam streaming from municipal buses and service trucks.

The system identifies potholes and cracks, estimates metric severity, resolves human-readable locations, and empowers authorities to prioritize maintenance.

## ✨ Key Features
- 🤖 **AI Road Damage Detection**: YOLOv11 classification with MiDaS 3D depth metrics.
- 📱 **Citizen & Fleet Channels**: Mobile crowdsourcing and vehicle dashcam stream ingestion.
- 📊 **Severity & Health Score**: Multi-factor priority matrix and 0–100% pavement rating.
- 📍 **GPS & Spatial Deduplication**: PostGIS 10-meter spatial buffer deduplication.
- 👨‍💼 **Admin Dashboard & Maps**: Complaint lifecycle dispatch, heatmaps, and analytics.

## 🛠 Tech Stack
**Flutter** • **FastAPI** • **Python** • **YOLOv11** • **OpenCV** • **MiDaS** • **PostgreSQL** • **PostGIS** • **Docker**

## 📂 Project Structure
```
RoadVision/
├── flutter_app/     # Flutter mobile client (Citizen & Admin roles)
├── backend/         # FastAPI REST APIs and schemas
├── ai/              # YOLOv11 detector, MiDaS depth, & vision pipeline
├── database/        # PostgreSQL schema DDL and PostGIS ORM layer
├── docker/          # Dockerfile and Docker Compose stack
└── docs/            # Architecture diagrams and system specs
```

## 🚀 Getting Started
```bash
git clone https://github.com/mubeenah-collab/AI-powered-roadcare.git
cd AI-powered-roadcare
docker compose up
```
