# Contributing to RoadVision AI

Thank you for your interest in contributing to **RoadVision: AI-Powered Intelligent Road Damage Detection & Monitoring System**.

## Development Workflow

1. **Fork & Clone Repository**:
   ```bash
   git clone https://github.com/mubeenah-collab/AI-powered-roadcare.git
   cd AI-powered-roadcare
   ```
2. **Setup Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate     # Windows
   pip install -r requirements.txt
   ```
3. **Branching Model**:
   - Create a feature branch: `git checkout -b feature/your-feature-name`
   - Make atomic, tested commits following standard commit conventions: `feat:`, `fix:`, `docs:`, `ci:`.
4. **Code Quality**:
   - Format Python code with `black` / `flake8`.
   - Ensure all API endpoints compile and unit tests pass (`pytest`).
5. **Submit Pull Request**:
   - Push branch to origin and open a PR with detailed context.
