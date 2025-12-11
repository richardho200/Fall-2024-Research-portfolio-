const express = require('express');
const { getResponses, addQuestionResponse, addSurveyResponse } = require('../controllers/responseController');
const router = express.Router();

router.get('/get-responses', getResponses);
router.post('/question', addQuestionResponse);
router.post('/survey', addSurveyResponse);

module.exports = router;
