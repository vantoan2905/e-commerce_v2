
@REM @echo off
@REM mkdir database\migrations
@REM type nul > database\__init__.py
@REM type nul > database\db_router.py
@REM type nul > database\models.py
@REM type nul > database\queries.py
@REM type nul > database\config.py



@echo off


if not exist "database_v2" mkdir "database_v2"

if not exist "database_v2\models" mkdir "database_v2\models"
if not exist "database_v2\models\__init__.py" (
    type nul > "database_v2\models\__init__.py"
)
if not exist "database_v2\models\user.py" (
    echo  "database_v2\models\user.py"
)
if not exist "database_v2\models\camera.py" (
    echo  "database_v2\models\camera.py"
)

if not exist "database_v2\dao" mkdir "database_v2\dao"
if not exist "database_v2\dao\__init__.py" (
    type nul > "database_v2\dao\__init__.py"
)
if not exist "database_v2\dao\base_dao.py" (
    echo  "database_v2\dao\base_dao.py"
)
if not exist "database_v2\dao\user_dao.py" (
    echo  "database_v2\dao\user_dao.py"
)
if not exist "database_v2\dao\camera_dao.py" (
    echo "database_v2\dao\camera_dao.py"
)

if not exist "database_v2\config" mkdir "database_v2\config"
if not exist "database_v2\config\config.py" (
    echo  "database_v2\config\config.py"
)

if not exist "database_v2\migrations" mkdir "database_v2\migrations"

pause
