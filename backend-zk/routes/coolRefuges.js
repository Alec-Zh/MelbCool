const Router = require('koa-router');
const router = new Router({ prefix: '/api/cool-refuges' });
const coolRefugeController = require('../controllers/coolRefugeController');

// Obtain all places for summer vacation
router.get('/', coolRefugeController.getAllCoolRefuges);

// Obtain place for summer vacation by ID
router.get('/:id', coolRefugeController.getCoolRefugeById);

// Create new place for summer vacation
router.post('/', coolRefugeController.createCoolRefuge);

// Update place for summer vacation
router.put('/:id', coolRefugeController.updateCoolRefuge);

// Delete place for summer vacation
router.delete('/:id', coolRefugeController.deleteCoolRefuge);

// Delete all places for summer vacation
router.delete('/', coolRefugeController.deleteAllCoolRefuges);

module.exports = router;
