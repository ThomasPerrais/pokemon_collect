# How to Run the Application

## Prerequisites

1. **MySQL Database**: Make sure MySQL is running and the database `poke_collect` exists
   - User: `pikachu`
   - Password: `dracaufeu2025`
   - Host: `localhost:3306`

2. **Python 3.12** with Poetry installed
3. **Flutter SDK** installed

## Step 1: Start the Backend

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Install dependencies (if not already done):
   ```bash
   poetry install
   ```

3. Make sure database migrations are applied:
   ```bash
   poetry run alembic upgrade head
   ```

4. Start the FastAPI server:
   ```bash
   poetry run uvicorn app.main:app --reload --port 8000
   ```

   The backend will be available at:
   - API: http://127.0.0.1:8000
   - GraphQL Playground: http://127.0.0.1:8000/graphql

## Step 2: Start the Flutter Frontend

1. Open a new terminal and navigate to the project root:
   ```bash
   cd /Users/thomasperrais/code/poke_collect
   ```

2. Get Flutter dependencies:
   ```bash
   flutter pub get
   ```

3. Run the Flutter app:
   ```bash
   flutter run
   ```

   Or run on a specific device:
   ```bash
   flutter run -d macos    # For macOS
   flutter run -d chrome   # For web
   flutter run -d ios       # For iOS simulator
   ```

## Quick Test

Once both are running:

1. **Test Backend**: Open http://127.0.0.1:8000/graphql in your browser
   - Try this query:
   ```graphql
   query {
     pokemons {
       id
       name
       nationalDexNumber
       types {
         name
       }
     }
   }
   ```

2. **Test Frontend**: The Flutter app should connect to the backend automatically
   - The GraphQL client is configured to use: `http://127.0.0.1:8000/graphql`
   - You should see the Pokemon list with filtering options

## Troubleshooting

- **Backend won't start**: Check that MySQL is running and the database exists
- **Flutter can't connect**: Verify the backend is running on port 8000
- **No data showing**: Make sure you have Pokemon data in your database
- **CORS errors**: The backend already has CORS enabled for all origins in dev mode

