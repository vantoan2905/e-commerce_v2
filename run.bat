call conda deactivate
call conda activate zifarm

fastapi dev e_server\c_con\src\main.py --port 5001  --reload 
