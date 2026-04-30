const Koa = require('koa');
const bodyParser = require('koa-bodyparser');
const cors = require('@koa/cors');
const Router = require('koa-router');
const userRoutes = require('./routes/users');
const coolRefugeRoutes = require('./routes/coolRefuges');

// Create a Koa application
const app = new Koa();
const router = new Router();
const PORT = process.env.PORT || 3000;

// Middleware setup
app.use(cors()); // Handle requests from different origins
app.use(bodyParser()); // Parse request bodies

// Route registration
app.use(router.routes());
app.use(userRoutes.routes()).use(userRoutes.allowedMethods());
app.use(coolRefugeRoutes.routes()).use(coolRefugeRoutes.allowedMethods());

// Error handling middleware
app.use(async (ctx, next) => {
  try {
    await next();
  } catch (err) {
    ctx.status = err.status || 500;
    ctx.body = {
      success: false,
      message: err.message || 'Server error occurred'
    };
  }
});

// Start the server
app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
  console.log(`User API endpoint: http://localhost:${PORT}/api/users`);
  console.log(`Cool refuge API endpoint: http://localhost:${PORT}/api/cool-refuges`);
  console.log(`View database with Prisma Studio: npx prisma studio`);
});

module.exports = app;
    