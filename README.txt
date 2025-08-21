Requirements:
    - Python 3.13.3

Setup:
    1. Ensure all the required files are downloaded
        -   Template_Folder
        -   app.py
        -   requirements.txt (optional)

    2. Create a virtual environment
        -  python -m venv .venv

    3. Install dependencies 

        pip install -r requirements.txt
        OR 
        Import the packages individually 
        (this is based on the Run a Server Manually page
        and the virtual environment page from fastapi)
            pip install "fastapi[standard]"
            AND
            pip install "uvicorn[standard]"

Running the application
    1. Start the FastAPI server
    uvicorn app:app --reload

    2. Access the application
    -   In the terminal, Ctrl + click the http link provided 
    which will direct you to application
        - Example: Uvicorn running on http://127.0.0.1:8000