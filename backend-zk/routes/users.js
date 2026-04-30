const Router = require('koa-router');
const router = new Router({ prefix: '/api/users' });
const userController = require('../controllers/userController');

// Obtain all users
router.get('/', userController.getAllUsers);

// Obtain user by ID
router.get('/:id', userController.getUserById);

// Create new user
router.post('/', userController.createUser);

// Update user
router.put('/:id', userController.updateUser);

// Delete user
router.delete('/:id', userController.deleteUser);

module.exports = router;
    