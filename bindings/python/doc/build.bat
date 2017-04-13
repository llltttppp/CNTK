setlocal

cd /d "%~dp0"
set PYTHONPATH=%CD%\..
set PATH=%CD%\..;%CD%\..\..\..\x64\Release;%PATH%

@REM TODO better align conf.py exclude with excluded paths here
@REM TODO -T (no toc)? -M module contents first?
@REM %SPHINX_APIDOC_OPTIONS%, comma-separated, default members,undoc-members,show-inheritance
@REM parser.add_option('-e', '--separate', action='store_true', dest='separatemodules', help='Put documentation for each module on its own page')
@REM do we want undoc-members?
@REM -E 
set SPHINX_APIDOC_OPTIONS=members
sphinx-apidoc.exe ..\cntk -M -e -T -o . -f ^
  ..\cntk\blocks.py ^
  ..\cntk\cntk_py.py ^
  ..\cntk\conftest.py ^
  ..\cntk\tests ^
  ..\cntk\debugging\tests ^
  ..\cntk\eval\tests ^
  ..\cntk\internal ^
  ..\cntk\io\tests ^
  ..\cntk\layers\tests ^
  ..\cntk\learners\tests ^
  ..\cntk\logging\tests ^
  ..\cntk\losses\tests ^
  ..\cntk\metrics\tests ^
  ..\cntk\ops\tests ^
  ..\cntk\train\tests

if errorlevel 1 exit /b 1

set SPHINXOPTS=-n %SPHINXOPTS%
call .\make.bat html
if errorlevel 1 exit /b 1
@REM .\make.bat text
@REM if errorlevel 1 exit /b 1
@REM .\make.bat doctest
@REM if errorlevel 1 exit /b 1
@REM call .\make.bat linkcheck
@REM if errorlevel 1 exit /b 1

echo start _build\html\index.html
