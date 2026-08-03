# Changelog

All notable changes to the RoadVision project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-08-03

### Added
- **AI Core**: Integrated YOLOv11 / YOLOv8 multi-damage object detector for 6 pavement defect classes.
- **Monocular Depth Engine**: Integrated MiDaS (v3.0 DPT) depth estimator for physical 3D width, length, area, depth (cm), and road occupancy % calculation.
- **Severity Matrix**: 0–100 Priority Scoring formula combining area, depth, class risk, and spatial verification counts.
- **Backend & PostGIS**: FastAPI service with JWT authentication, PostGIS 10m spatial buffer deduplication (`ST_DWithin`), citizen complaint endpoints, and admin dispatch routing.
- **Frontend**: React + Tailwind + Leaflet GIS Admin Dashboard & Citizen Mobile Reporting Portal.
- **Fleet Integration**: Continuous government vehicle 4G/5G ingestion pipeline for automated road surveillance.
- **MLOps & DevOps**: Docker Compose multi-container deployment, NGINX config, and GitHub Actions CI/CD workflows.
