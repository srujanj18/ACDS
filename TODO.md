# ACDS Fix: ModuleNotFoundError for online_model
## Plan Steps:
- [x] 1. Ensure __init__.py exists in backend/online_learning/
- [x] 2. Edit update.py: Change absolute import to relative `from .online_model import OnlineModel`
- [x] 3. Test: python scripts/run_backend.py
- [x] 4. If models missing: python models/generate_models.py
- [x] 5. Complete task
