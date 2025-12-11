function errorHandler(err, req, res, next) {
    console.error(err.stack); // Log the error stack trace for debugging
    res.status(500).json({ message: 'An unexpected error occurred.' }); // Send a 500 response with a generic error message
}

module.exports = errorHandler; // Export the error handling middleware
