const { PrismaClient } = require('@prisma/client');
const fs = require('fs');
const path = require('path');

const prisma = new PrismaClient();

// Type mapping to normalize all types to lowercase
const typeMapping = {
  'Library': 'library',
  'library': 'library',
  'Museum': 'museum',
  'museum': 'museum',
  'Park': 'park',
  'park': 'park',
  'Community': 'community',
  'community': 'community',
  'Shopping Centre': 'shopping',
  'Shopping Centre\u00a0': 'shopping',
  'shopping': 'shopping',
  '': 'library', // Empty value defaults to library
};

// Normalize type
function normalizeType(type) {
  const normalized = typeMapping[type];
  if (normalized) {
    return normalized;
  }
  // Try lowercase
  const lowerType = type.toLowerCase();
  if (['library', 'museum', 'park', 'community', 'shopping'].includes(lowerType)) {
    return lowerType;
  }
  // Default to library
  return 'library';
}

async function importData() {
  try {
    // Read JSON file
    const jsonPath = path.join(__dirname, '..', 'tableConvert.com_92s4yj.json');
    const jsonData = fs.readFileSync(jsonPath, 'utf-8');
    const data = JSON.parse(jsonData);

    console.log(`Preparing to import ${data.length} records...`);

    let successCount = 0;
    let errorCount = 0;
    const errors = [];

    for (let i = 0; i < data.length; i++) {
      const item = data[i];
      
      try {
        // Validate and convert data
        const longitude = parseFloat(item.longitude);
        const latitude = parseFloat(item.latitude);

        if (isNaN(longitude) || isNaN(latitude)) {
          throw new Error(`Invalid coordinates: ${item.longitude}, ${item.latitude}`);
        }

        if (!item.name || item.name.trim() === '') {
          throw new Error('Name cannot be empty');
        }

        if (!item.city || item.city.trim() === '') {
          throw new Error('City cannot be empty');
        }

        if (!item.street || item.street.trim() === '') {
          throw new Error('Street cannot be empty');
        }

        // Create record in the database table coolRefuge
        await prisma.coolRefuge.create({
          data: {
            name: item.name.trim(),
            type: normalizeType(item.type || ''),
            longitude: longitude,
            latitude: latitude,
            city: item.city.trim(),
            street: item.street.trim(),
            openingHours: item.openingHours ? item.openingHours.trim() : null,
            facilities: item.facilities ? item.facilities.trim() : null,
            photo: null, // JSON does not have a photo field
            phone: null, // JSON does not have a phone field
            website: null, // JSON does not have a website field
            notes: null, // JSON does not have a notes field
          },
        });

        successCount++;
        
        // Log progress every 50 records
        if ((i + 1) % 50 === 0) {
          console.log(`Imported ${i + 1} / ${data.length} records...`);
        }
      } catch (error) {
        errorCount++;
        errors.push({
          index: i,
          name: item.name,
          error: error.message,
        });
        console.error(`Record ${i + 1} import failed:`, error.message);
      }
    }

    console.log('\n========== Import completed ==========');
    console.log(`Success: ${successCount} records`);
    console.log(`Failed: ${errorCount} records`);
    console.log(`Total: ${data.length} records`);

    if (errors.length > 0) {
      console.log('\n========== Error Details ==========');
      errors.slice(0, 10).forEach((err) => {
        console.log(`  - ${err.name || 'Unnamed'}: ${err.error}`);
      });
      if (errors.length > 10) {
        console.log(`  ... More ${errors.length - 10} errors`);
      }
    }

  } catch (error) {
    console.error('Import process error:', error);
  } finally {
    await prisma.$disconnect();
  }
}

// Run the import data script
importData();
