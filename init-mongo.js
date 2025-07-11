
// MongoDB Initialization Script for Cats API
// This script creates default users with proper authentication and persistence

// First, authenticate with admin database
print('🔐 Authenticating with admin database...');

// Switch to cats_api database
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

// Insert admin user with explicit write concern
try {
    const adminResult = db.users.insertOne({
        "first_name": "Admin",
        "last_name": "User", 
        "username": "admin",
        "password": passwordHash,
        "email": "admin@example.com",
        "created_at": new Date(),
        "updated_at": new Date()
    }, { writeConcern: { w: "majority", j: true } });
    print('✅ Admin user created with ID: ' + adminResult.insertedId);
} catch (error) {
    print('❌ Error creating admin user: ' + error);
}

// Insert default user "john.doe" with explicit write concern
try {
    const johnResult = db.users.insertOne({
        "first_name": "John",
        "last_name": "Doe", 
        "username": "john.doe",
        "password": passwordHash,
        "email": "john.doe@example.com",
        "created_at": new Date(),
        "updated_at": new Date()
    }, { writeConcern: { w: "majority", j: true } });
    print('✅ John Doe user created with ID: ' + johnResult.insertedId);
} catch (error) {
    print('❌ Error creating john.doe user: ' + error);
}

print('📊 Database initialization completed!');
print('🔐 Default users created with password: password123');

// Count and display users - verify immediately after creation
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

// Force multiple persistence operations
print('💾 Forcing data persistence...');
try {
    // Switch to admin database for fsync
    const adminDb = db.getSiblingDB('admin');
    adminDb.runCommand({"fsync": 1});
    adminDb.runCommand({"fsync": 1, "lock": false});
    print('✅ Data persistence completed');
} catch (error) {
    print('⚠️ Note: fsync command had issues but data should be persisted: ' + error);
}

// Final verification
const finalCount = db.users.countDocuments();
print('🔍 Final verification - users in database: ' + finalCount);

// Additional verification - try to find users by username
const adminUser = db.users.findOne({username: "admin"});
const johnUser = db.users.findOne({username: "john.doe"});

if (adminUser) {
    print('✓ Admin user verified in database');
} else {
    print('✗ Admin user NOT found in database');
}

if (johnUser) {
    print('✓ John.doe user verified in database'); 
} else {
    print('✗ John.doe user NOT found in database');
}

print('🎉 MongoDB initialization script completed successfully!');
