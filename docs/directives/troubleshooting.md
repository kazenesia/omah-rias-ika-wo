# Troubleshooting: Missing Dependencies

If you encounter a `ModuleNotFoundError` when running the Django server, follow these steps.

## SOP: Dependency Resolution

1. **CRITICAL: Activate Virtual Environment:** Ensure your venv is active.
   - Windows: `.\backend\venv\Scripts\activate`
   - Linux/Mac: `source backend/venv/bin/activate`
2. **Verify Environment:** Run `pip -V` to confirm the path points to your `venv`.
3. **Sync Requirements:** Run the deterministic setup script.
   - Command: `python scripts/setup_env.py`
4. **Verify Installation:** Check if the module is listed in `pip list`.

## Common Missing Modules
- `corsheaders`: Provided by `django-cors-headers`.
- `PIL` or `Pillow`: Required for image fields.
