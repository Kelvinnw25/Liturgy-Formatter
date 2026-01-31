cd fastAPI
# Install dependencies
pip install -r requirements.txt
# Run server
uvicorn app.main:app --reload


cd react
# Install dependencies
npm install
# Run app
npm run dev