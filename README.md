# How to run DeskMate

Setup Instructions
🚀 Backend Setup
Clone the Repository

bash
Copy
Edit
git clone https://github.com/LukeJohnson02/DeskMate.git
cd DeskMate/backend
Create a Virtual Environment (Optional but Recommended)

bash
Copy
Edit
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install Dependencies

bash
Copy
Edit
pip install -r requirements.txt
Run the Backend Server

bash
Copy
Edit
uvicorn main:app --reload
Access API Docs
Visit: http://127.0.0.1:8000/docs

💻 Frontend Setup
Navigate to Frontend Folder

bash
Copy
Edit
cd ../frontend

Start running the frontend.
npm start


# User Details
## admin
### Email: admin1@example.com
### Password: adminpass123
## user
### Email: user1@example.com
### Password: password123