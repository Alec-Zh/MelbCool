const { PrismaClient, Prisma } = require('@prisma/client');
const prisma = new PrismaClient();

// Get all users
exports.getAllUsers = async (ctx) => {
  try {
    const users = await prisma.user.findMany({
      orderBy: {
        createdAt: 'desc'
      }
    });
    
    ctx.body = {
      success: true,
      data: users,
      count: users.length
    };
  } catch (error) {
    console.error('Failed to get user list:', error);
    ctx.throw(500, `Failed to get user list: ${error.message}`);
  }
};

// Get user by ID
exports.getUserById = async (ctx) => {
  try {
    const { id } = ctx.params;
    
    // Validate the ID is a valid number
    if (isNaN(parseInt(id))) {
      ctx.throw(400, 'User ID must be a number');
    }
    
    const user = await prisma.user.findUnique({
      where: { id: parseInt(id) }
    });
    
    if (!user) {
      ctx.throw(404, `User with ID ${id} does not exist`);
    }
    
    ctx.body = {
      success: true,
      data: user
    };
  } catch (error) {
    console.error(`Failed to get user with ID ${id}:`, error);
    if (error instanceof Prisma.PrismaClientKnownRequestError) {
      ctx.throw(400, `Invalid user ID for user: ${error.message}`);
    }
    ctx.throw(500, `Failed to get user: ${error.message}`);
  }
};

// Create new user
exports.createUser = async (ctx) => {
  try {
    const { name, email, age } = ctx.request.body;
    
    // Validate input data is valid
    if (typeof name !== 'string' || name.trim() === '') {
      ctx.throw(400, 'Name must be a valid string');
    }
    
    if (typeof email !== 'string' || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      ctx.throw(400, 'Email must be a valid email address');
    }
    
    if (age !== undefined && (isNaN(age) || age < 0 || age > 150)) {
      ctx.throw(400, 'Age must be between 0-150');
    }
    
    const newUser = await prisma.user.create({
      data: {
        name: name.trim(),
        email: email.trim(),
        age: age !== undefined ? parseInt(age) : null
      }
    });
    
    ctx.status = 201; // User created successfully with status code 201
    ctx.body = {
      success: true,
      message: 'User created successfully!',
      data: newUser
    };
  } catch (error) {
    console.error('Failed to create user:', error);
    
    // Detailed error classification handling
    if (error instanceof Prisma.PrismaClientKnownRequestError) {
      // Unique constraint violation (email already registered)
      if (error.code === 'P2002') {
        ctx.throw(409, 'Email already registered');
      }
      // Other Prisma known errors
      ctx.throw(400, `Database error: ${error.message}`);
    } 
    // Koa throws errors (e.g., parameter validation failures)
    else if (error.status) {
      ctx.throw(error.status, error.message);
    }
    // Other unknown errors or exceptions
    else {
      ctx.throw(500, `Failed to create user: ${error.message}`);
    }
  }
};

// Update user information
exports.updateUser = async (ctx) => {
  try {
    const { id } = ctx.params;
    const { name, email, age } = ctx.request.body;
    
    // Verify the ID is a valid number
    if (isNaN(parseInt(id))) {
      ctx.throw(400, 'User ID must be a number');
    }
    
    // Validate input data is valid
    if (name !== undefined && (typeof name !== 'string' || name.trim() === '')) {
      ctx.throw(400, 'Name must be a valid string');
    }
    
    if (email !== undefined && (typeof email !== 'string' || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email))) {
      ctx.throw(400, 'Email must be a valid email address');
    }
    
    if (age !== undefined && (isNaN(age) || age < 0 || age > 150)) {
      ctx.throw(400, 'Age must be between 0-150');
    }
    
    const updatedUser = await prisma.user.update({
      where: { id: parseInt(id) },
      data: {
        ...(name !== undefined && { name: name.trim() }),
        ...(email !== undefined && { email: email.trim() }),
        ...(age !== undefined && { age: parseInt(age) })
      }
    });
    
    ctx.body = {
      success: true,
      message: 'User updated successfully!',
      data: updatedUser
    };
  } catch (error) {
    console.error(`Failed to update user with ID ${id}:`, error);
    
    if (error instanceof Prisma.PrismaClientKnownRequestError) {
      if (error.code === 'P2002') {
        ctx.throw(409, 'Email already registered');
      }
      if (error.code === 'P2025') {
        ctx.throw(404, 'User does not exist');
      }
      ctx.throw(400, `Database error: ${error.message}`);
    } else if (error.status) {
      ctx.throw(error.status, error.message);
    } else {
      ctx.throw(500, `Failed to update user: ${error.message}`);
    }
  }
};

// 删除用户
exports.deleteUser = async (ctx) => {
  try {
    const { id } = ctx.params;
    
    // Verify whether the ID is a valid number
    if (isNaN(parseInt(id))) {
      ctx.throw(400, 'User ID must be a number');
    }
    
    await prisma.user.delete({
      where: { id: parseInt(id) }
    });
    
    ctx.body = {
      success: true,
      message: `User with ID ${id} deleted successfully!`
    };
  } catch (error) {
    console.error(`Failed to delete user with ID ${id}:`, error);
    
    if (error instanceof Prisma.PrismaClientKnownRequestError) {
      if (error.code === 'P2025') {
        ctx.throw(404, 'User does not exist');
      }
      ctx.throw(400, `Database error: ${error.message}`);
    } else if (error.status) {
      ctx.throw(error.status, error.message);
    } else {
      ctx.throw(500, `Failed to delete user: ${error.message}`);
    }
  }
};
    