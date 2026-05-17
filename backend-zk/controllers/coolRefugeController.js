const { PrismaClient, Prisma } = require('@prisma/client');
const prisma = new PrismaClient();

// Get all the summer resort locations, and support searching by name and type.
exports.getAllCoolRefuges = async (ctx) => {
  try {
    const { name, type } = ctx.query;
    let whereClause = {};
    
    // If a name query parameter is provided, add a name search condition.
    if (name && typeof name === 'string' && name.trim() !== '') {
      whereClause.name = {
        contains: name.trim()
        // SQLite does not support mode: 'insensitive', but LIKE operation defaults to case-insensitive
      };
    }
    
    // If a type query parameter is provided, add a type search condition.
    if (type && typeof type === 'string' && type.trim() !== '') {
      const allowedTypes = ['library', 'museum', 'park', 'community', 'shopping'];
      const normalizedType = type.trim().toLowerCase();
      
      if (allowedTypes.includes(normalizedType)) {
        whereClause.type = normalizedType;
      }
    }
    
    const coolRefuges = await prisma.coolRefuge.findMany({
      where: whereClause,
      orderBy: {
        createdAt: 'desc'
      }
    });
    
    ctx.body = {
      success: true,
      data: coolRefuges,
      count: coolRefuges.length,
      searchName: name || null,
      searchType: type || null
    };
  } catch (error) {
    console.error('Failed to get all summer resort locations:', error);
    ctx.throw(500, `Failed to get all summer resort locations: ${error.message}`);
  }
};

// Get summer resort location by ID
exports.getCoolRefugeById = async (ctx) => {
  try {
    const { id } = ctx.params;
    
    // Validate the ID is a valid number
    if (isNaN(parseInt(id))) {
      ctx.throw(400, 'Summer resort location ID must be a number');
    }
    
    const coolRefuge = await prisma.coolRefuge.findUnique({
      where: { id: parseInt(id) }
    });
    
    if (!coolRefuge) {
      ctx.throw(404, `Summer resort location with ID ${id} does not exist`);
    }
    
    ctx.body = {
      success: true,
      data: coolRefuge
    };
  } catch (error) {
    console.error(`Failed to get summer resort location with ID ${id}:`, error);
    if (error instanceof Prisma.PrismaClientKnownRequestError) {
      ctx.throw(400, `Invalid ID for summer resort location: ${error.message}`);
    }
    ctx.throw(500, `Failed to get summer resort location: ${error.message}`);
  }
};

// Create new summer resort location
exports.createCoolRefuge = async (ctx) => {
  try {
    const { 
      photo, 
      longitude, 
      latitude, 
      name, 
      type,
      openingHours, 
      phone, 
      city, 
      street, 
      website, 
      facilities, 
      notes 
    } = ctx.request.body;
    
    // Validate input data is valid
    if (typeof name !== 'string' || name.trim() === '') {
      ctx.throw(400, 'Name must be a valid string');
    }
    
    if (typeof type !== 'string' || type.trim() === '') {
      ctx.throw(400, 'Type must be a valid string');
    }
    
    // Validate the type is within the allowed values
    const allowedTypes = ['library', 'museum', 'park', 'community', 'shopping'];
    if (!allowedTypes.includes(type.trim())) {
      ctx.throw(400, `Type must be one of: ${allowedTypes.join(', ')}`);
    }
    
    if (typeof longitude !== 'number' || isNaN(longitude)) {
      ctx.throw(400, 'Longitude must be a valid number');
    }
    
    if (typeof latitude !== 'number' || isNaN(latitude)) {
      ctx.throw(400, 'Latitude must be a valid number');
    }
    
    if (typeof city !== 'string' || city.trim() === '') {
      ctx.throw(400, 'City must be a valid string');
    }
    
    if (typeof street !== 'string' || street.trim() === '') {
      ctx.throw(400, 'Street must be a valid string');
    }
    
    const newCoolRefuge = await prisma.coolRefuge.create({
      data: {
        photo: photo ? photo.trim() : null,
        longitude,
        latitude,
        name: name.trim(),
        type: type.trim(),
        openingHours: openingHours ? openingHours.trim() : null,
        phone: phone ? phone.trim() : null,
        city: city.trim(),
        street: street.trim(),
        website: website ? website.trim() : null,
        facilities: facilities ? facilities.trim() : null,
        notes: notes ? notes.trim() : null
      }
    });
    
    ctx.status = 201; // Created
    ctx.body = {
      success: true,
      message: 'Cool refuge created successfully!',
      data: newCoolRefuge
    };
  } catch (error) {
    console.error('Failed to create cool refuge:', error);
    
    // Detailed error classification handling
    if (error instanceof Prisma.PrismaClientKnownRequestError) {
      ctx.throw(400, `Database error: ${error.message}`);
    } 
    // Koa throws errors (e.g., parameter validation failures)
    else if (error.status) {
      ctx.throw(error.status, error.message);
    }
    // Other unknown errors or exceptions
    else {
      ctx.throw(500, `Failed to create cool refuge: ${error.message}`);
    }
  }
};

// Update a summer resort location
exports.updateCoolRefuge = async (ctx) => {
  try {
    const { id } = ctx.params;
    const { 
      photo, 
      longitude, 
      latitude, 
      name, 
      type,
      openingHours, 
      phone, 
      city, 
      street, 
      website, 
      facilities, 
      notes 
    } = ctx.request.body;
    
    // Validate the ID is a valid number
    if (isNaN(parseInt(id))) {
      ctx.throw(400, 'Summer resort location ID must be a number');
    }
    
    // Validate input data is valid
    if (name !== undefined && (typeof name !== 'string' || name.trim() === '')) {
      ctx.throw(400, 'Name must be a valid string');
    }
    
    if (type !== undefined) {
      if (typeof type !== 'string' || type.trim() === '') {
        ctx.throw(400, 'Type must be a valid string');
      }
      // Validate the type is within the allowed values
      const allowedTypes = ['library', 'museum', 'park', 'community', 'shopping'];
      if (!allowedTypes.includes(type.trim())) {
        ctx.throw(400, `Type must be one of: ${allowedTypes.join(', ')}`);
      }
    }
    
    if (longitude !== undefined && (typeof longitude !== 'number' || isNaN(longitude))) {
      ctx.throw(400, 'Longitude must be a valid number');
    }
    
    if (latitude !== undefined && (typeof latitude !== 'number' || isNaN(latitude))) {
      ctx.throw(400, 'Latitude must be a valid number');
    }
    
    if (city !== undefined && (typeof city !== 'string' || city.trim() === '')) {
      ctx.throw(400, 'City must be a valid string');
    }
    
    if (street !== undefined && (typeof street !== 'string' || street.trim() === '')) {
      ctx.throw(400, 'Street must be a valid string');
    }
    
    const updatedCoolRefuge = await prisma.coolRefuge.update({
      where: { id: parseInt(id) },
      data: {
        ...(photo !== undefined && { photo: photo ? photo.trim() : null }),
        ...(longitude !== undefined && { longitude }),
        ...(latitude !== undefined && { latitude }),
        ...(name !== undefined && { name: name.trim() }),
        ...(type !== undefined && { type: type.trim() }),
        ...(openingHours !== undefined && { openingHours: openingHours ? openingHours.trim() : null }),
        ...(phone !== undefined && { phone: phone ? phone.trim() : null }),
        ...(city !== undefined && { city: city.trim() }),
        ...(street !== undefined && { street: street.trim() }),
        ...(website !== undefined && { website: website ? website.trim() : null }),
        ...(facilities !== undefined && { facilities: facilities ? facilities.trim() : null }),
        ...(notes !== undefined && { notes: notes ? notes.trim() : null })
      }
    });
    
    ctx.body = {
      success: true,
      message: 'Cool refuge updated successfully!',
      data: updatedCoolRefuge
    };
  } catch (error) {
    console.error(`Failed to update cool refuge with ID ${id}:`, error);
    
    if (error instanceof Prisma.PrismaClientKnownRequestError) {
      if (error.code === 'P2025') {
        ctx.throw(404, 'Cool refuge not found');
      }
      ctx.throw(400, `Database error: ${error.message}`);
    } else if (error.status) {
      ctx.throw(error.status, error.message);
    } else {
      ctx.throw(500, `Failed to update cool refuge: ${error.message}`);
    }
  }
};

// Delete a summer resort
exports.deleteCoolRefuge = async (ctx) => {
  try {
    const { id } = ctx.params;
    
    // Validate the ID is a valid number
    if (isNaN(parseInt(id))) {
      ctx.throw(400, 'Summer resort location ID must be a number');
    }
    
    await prisma.coolRefuge.delete({
      where: { id: parseInt(id) }
    });
    
    ctx.body = {
      success: true,
      message: `Cool refuge with ID ${id} deleted successfully!`
    };
  } catch (error) {
    console.error(`Failed to delete cool refuge with ID ${id}:`, error);
    
    if (error instanceof Prisma.PrismaClientKnownRequestError) {
      if (error.code === 'P2025') {
        ctx.throw(404, 'Cool refuge not found');
      }
      ctx.throw(400, `Database error: ${error.message}`);
    } else if (error.status) {
      ctx.throw(error.status, error.message);
    } else {
      ctx.throw(500, `Failed to delete cool refuge: ${error.message}`);
    }
  }
};

// Delete all summer resorts
exports.deleteAllCoolRefuges = async (ctx) => {
  try {
    // First, obtain the total amount
    const count = await prisma.coolRefuge.count();
    
    // Then, delete all records from the database
    await prisma.coolRefuge.deleteMany({});
    
    ctx.body = {
      success: true,
      message: `Deleted all ${count} summer resorts successfully!`
    };
  } catch (error) {
    console.error('Failed to delete all summer resorts:', error);
    
    if (error instanceof Prisma.PrismaClientKnownRequestError) {
      ctx.throw(400, `Database error: ${error.message}`);
    } else {
      ctx.throw(500, `Failed to delete all summer resorts: ${error.message}`);
    }
  }
};
