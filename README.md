Modern Python Demo
==================

This project is a compact but feature-rich demonstration of advanced modern Python techniques. It is designed to be pedagogical and runnable.

Highlights
- Advanced decorators (parameterized, nested, class-attribute decorators)
- Metaclasses and __init_subclass__ hooks
- dataclasses, attrs and __slots__ for memory-efficient models
- Protocols, ABCs, Generic typing and runtime structural checks
- Asyncio-based event engine, scheduler and tasks
- Custom context managers
- Dynamic plugin discovery (importlib / pkgutil)
- Caching (functools.lru_cache + custom decorators)
- Hierarchical exceptions and advanced logging
- Serialization (JSON, Pickle, YAML) with simple versioning
- Descriptors, cached_property and dynamic properties
- Observer/event engine, signal/callback patterns
- Introspection with inspect and typing
- Generators, coroutines and pipeline decorators

Run the demo:

1. Create a virtual environment and install dependencies:

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1; python -m pip install -r requirements.txt
```

2. Run the demo:

```powershell
python -m modern_python_demo.main
```

Publishing to GitHub
--------------------

If you want to publish the project to GitHub quickly, you can use the GitHub CLI (`gh`) and the included script:

PowerShell:
```powershell
# create repo and push (requires gh auth)
.\	ools\create_repo.ps1 -Name my-repo -Visibility public -Push
```

Alternatively, initialize a git repo and push manually:

```powershell
git init
git add -A
git commit -m "Initial import"
git branch -M main
git remote add origin https://github.com/youruser/yourrepo.git
git push -u origin main
```

Bumping versions
----------------
Use the simple helper to bump the version in `pyproject.toml`:

```powershell
python tools/bump_version.py --part patch
```


Note about origin
-----------------
This project was generated programmatically by an automated coding assistant and provided as an educational example. It was created to demonstrate modern Python features and patterns; you should review, adapt, and test the code before using or publishing it as your own work.

Files of interest:
- `modern_python_demo/` package containing the core modules
- `modern_python_demo/plugins/` sample plugin(s)
- `modern_python_demo/main.py` demo orchestrator

Authors: Generated programmatically to showcase modern Python.