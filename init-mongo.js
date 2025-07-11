// MongoDB initialization script for cats_api database
// This script runs automatically when MongoDB starts with an empty database
// Creates default users: admin and john.doe (both with password: password123)
// DO NOT MODIFY unless you understand MongoDB initialization process

print('Starting MongoDB initialization...');

// Switch to cats_api database
db = db.getSiblingDB('cats_api');

print('Creating users collection...');
// Create users collection with indexes
db.createCollection('users');
db.users.createIndex({ "username": 1 }, { unique: true });
db.users.createIndex({ "email": 1 });

print('Inserting default users...');

// Insert default user "john.doe" 
// Password hash for "password123" using bcrypt
const johnResult = db.users.insertOne({
  "first_name": "John",
  "last_name": "Doe", 
  "username": "john.doe",
  "password": "$2b$12$l8PQqVquzyMRLlKZwbpwZ.Ww7a29VJhJIo4OrhoanrwloR0VyJ8qm", // password123
  "email": "john.doe@example.com",
  "created_at": new Date(),
  "updated_at": new Date()
});

print('John Doe user created with ID: ' + johnResult.insertedId);

// Insert admin user
const adminResult = db.users.insertOne({
  "first_name": "Admin",
  "last_name": "User", 
  "username": "admin",
  "password": "$2b$12$l8PQqVquzyMRLlKZwbpwZ.Ww7a29VJhJIo4OrhoanrwloR0VyJ8qm", // password123
  "email": "admin@example.com",
  "created_at": new Date(),
  "updated_at": new Date()
});

print('Admin user created with ID: ' + adminResult.insertedId);

print('Database initialization completed successfully!');
print('Default users created:');
print('- john.doe (password: password123)');
print('- admin (password: password123)');
print('Total users in database: ' + db.users.countDocuments());
