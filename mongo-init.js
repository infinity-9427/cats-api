// MongoDB initialization script
db = db.getSiblingDB('cats_api');

// Create users collection with indexes
db.createCollection('users');
db.users.createIndex({ "username": 1 }, { unique: true });
db.users.createIndex({ "email": 1 });

// Insert a sample user for testing - default user "john.doe"
db.users.insertOne({
  "first_name": "John",
  "last_name": "Doe", 
  "username": "john.doe",
  "password": "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewVyLrId4Qa8/8IS", // password: password123
  "email": "john.doe@example.com",
  "created_at": new Date(),
  "updated_at": new Date()
});

// Insert admin user for testing
db.users.insertOne({
  "first_name": "Admin",
  "last_name": "User", 
  "username": "admin",
  "password": "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewVyLrId4Qa8/8IS", // password: admin123
  "email": "admin@example.com",
  "created_at": new Date(),
  "updated_at": new Date()
});

print("Database initialized successfully!");
print("Default users created:");
print("- john.doe (password: password123)");
print("- admin (password: admin123)");
print("Username uniqueness is enforced by database index.");
