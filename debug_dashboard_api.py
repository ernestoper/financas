from app import create_app, db
from app.models.core import User
from flask import session

app = create_app()

def debug_dashboard():
    with app.test_request_context('/api/dashboard-data?mes=11&ano=2024'):
        # Simulate login
        user = User.query.first()
        if not user:
            print("❌ No user found")
            return
            
        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess['user_id'] = user.id
                sess['familia_id'] = user.familia_id
                
            response = client.get('/api/dashboard-data?mes=11&ano=2024')
            
            print(f"Status Code: {response.status_code}")
            if response.status_code == 200:
                data = response.get_json()
                print("✅ API Response Data:")
                for key, value in data.items():
                    print(f"  - {key}: {value}")
            else:
                print(f"❌ Error: {response.data}")

if __name__ == "__main__":
    debug_dashboard()
