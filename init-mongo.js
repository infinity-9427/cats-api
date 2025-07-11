
db = db.getSiblingDB('cats_api');
print('📍 Switched to database: ' + db.getName());

try {
    db.users.drop();
    print('🗑️ Dropped existing users collection');
} catch (error) {
    print('ℹ️ No existing users collection to drop');
}

// Create users collection with proper indexes
db.createCollection('users');
print('✅ Created users collection');

// Create indexes
db.users.createIndex({ "username": 1 }, { unique: true });
db.users.createIndex({ "email": 1 });
print('📇 Created indexes on username (unique) and email');

print('👥 Inserting default users...');

// Fresh bcrypt hash for "password123" - verified working hash
const passwordHash = "$2b$12$R7d1kkqQgJI68HitAnD4pODo8ij6wqF3c4Q8DTy75n1BtiuuBAhay";

// Insert admin user
try {
    const adminResult = db.users.insertOne({
        "first_name": "Admin",
        "last_name": "User", 
        "username": "admin",
        "password": passwordHash,
        "email": "admin@example.com",
        "created_at": new Date(),
        "updated_at": new Date()
    });
    print('✅ Admin user created with ID: ' + adminResult.insertedId);
} catch (error) {
    print('❌ Error creating admin user: ' + error);
}

// Insert default user "john.doe" 
try {
    const johnResult = db.users.insertOne({
        "first_name": "John",
        "last_name": "Doe", 
        "username": "john.doe",
        "password": passwordHash,
        "email": "john.doe@example.com",
        "created_at": new Date(),
        "updated_at": new Date()
    });
    print('✅ John Doe user created with ID: ' + johnResult.insertedId);
} catch (error) {
    print('❌ Error creating john.doe user: ' + error);
}

print('📊 Database initialization completed!');
print('🔐 Default users created with password: password123');

// Count and display users
const userCount = db.users.countDocuments();
print('👤 Total users in database: ' + userCount);

if (userCount > 0) {
    print('📋 User list:');
    // Show created users (without passwords)
    db.users.find({}, {password: 0}).forEach(user => {
        print('   - ' + user.username + ' (' + user.email + ') - ID: ' + user._id);
    });
} else {
    print('⚠️ Warning: No users found in database after initialization!');
}

print('🎉 MongoDB initialization script completed successfully!');
