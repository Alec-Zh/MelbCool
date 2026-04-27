const { PrismaClient } = require('@prisma/client');

const prisma = new PrismaClient();

async function deleteAllData() {
  try {
    console.log('Fetching record count...');
    
    // First, fetch the total count of records in the database table
    const count = await prisma.coolRefuge.count();
    
    if (count === 0) {
      console.log('No records found in the database, nothing to delete.');
      return;
    }
    
    console.log(`Deleting ${count} records...`);
    console.log('⚠️  Warning: This action is irreversible!');
    
    // Delete all records in the database table coolRefuge
    const result = await prisma.coolRefuge.deleteMany({});
    
    console.log('========== Delete completed ==========');
    console.log(`Deleted: ${result.count} records`);
    
  } catch (error) {
    console.error('Delete process error:', error);
  } finally {
    await prisma.$disconnect();
  }
}

// Run the delete all data script
deleteAllData();
