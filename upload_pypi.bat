@echo off
REM ShenBi - Build and upload to PyPI
setlocal enabledelayedexpansion
cd /d "%~dp0"

set PYTHON=python
set VERSION_FILE=shenbi\__init__.py

echo === ShenBi PyPI Upload ===

echo [1/5] Bumping patch version...
%PYTHON% -c "import re, sys; p = '%VERSION_FILE%'; t = open(p,encoding='utf-8').read(); m = re.search(r'(__version__\s*=\s*\"(\d+\.\d+\.)(\d+)\")', t); old_v = m.group(2) + m.group(3) if m else '0.0.0'; new_v = m.group(2) + str(int(m.group(3)) + 1) if m else '0.0.1'; open(p,'w',encoding='utf-8').write(t.replace(m.group(1), '__version__ = \"' + new_v + '\"')); print(f'  {old_v} -> {new_v}')"

echo [2/5] Cleaning old builds...
if exist dist\ rmdir /s /q dist
if exist build\ rmdir /s /q build
for /d %%i in (*.egg-info) do rmdir /s /q "%%i"
if exist shenbi.egg-info rmdir /s /q shenbi.egg-info

echo [3/5] Installing build tools...
%PYTHON% -m pip install --upgrade build twine -q

echo [4/5] Building package...
%PYTHON% -m build
%PYTHON% -m twine check dist\*

echo [5/5] Uploading to PyPI...
%PYTHON% -m twine upload dist\*

echo === Done! ===
endlocal
