call conda deactivate
call conda activate My_ai_env

@REM call fastapi dev c_con\src\main.py --port 5001  --reload 
uvicorn src.main:app --port 5001 --reload
