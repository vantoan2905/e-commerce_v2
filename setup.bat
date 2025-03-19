@echo off
mkdir pastAPI
cd pastAPI
mkdir app
(
    echo # FastAPI Project
) > README.md
(
    echo # Python dependencies
) > requirements.txt
(
    echo # Environment variables
) > .env
(
    echo # Git ignore
) > .gitignore
(
    echo from fastapi import FastAPI
    echo app = FastAPI()
    echo(
    echo @app.get("/")
    echo def read_root():
    echo     return {"message": "Welcome to FastAPI"}
) > app\main.py
(
    echo import uvicorn
    echo if __name__ == "__main__":
    echo     uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
) > run.py

mkdir app\models
mkdir app\schemas
mkdir app\api
mkdir app\api\routes
mkdir app\services
mkdir app\tests
mkdir app\migrations
mkdir app\utils

(
    echo # Init file
) > app\__init__.py
(
    echo # Configurations
) > app\config.py
(
    echo # Database setup
) > app\database.py

(
    echo # Models init
) > app\models\__init__.py
(
    echo # User model
) > app\models\user.py

(
    echo # Schemas init
) > app\schemas\__init__.py
(
    echo # User schema
) > app\schemas\user.py

(
    echo # API init
) > app\api\__init__.py
(
    echo # API routes init
) > app\api\routes\__init__.py
(
    echo # User routes
) > app\api\routes\user.py

(
    echo # Services init
) > app\services\__init__.py
(
    echo # User service
) > app\services\user_service.py

(
    echo # Test init
) > app\tests\__init__.py
(
    echo # Sample test
) > app\tests\test_main.py

(
    echo # Utility functions
) > app\utils\__init__.py

echo "Project structure created successfully!"
