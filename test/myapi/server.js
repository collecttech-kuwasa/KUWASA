const express = require('express');
const { Pool } = require('pg');
const app = express();
const port = 3000;

// PostgreSQL connection configuration
const pool = new Pool({
  user: 'nact',
  host: 'localhost',
  database: 'kuwasaDB',
  password: 'nact',
  port: 5432,
});

// Middleware to parse JSON bodies
app.use(express.json());

// Endpoint to get all customers
app.get('/customers', async (req, res) => {
  try {
    const result = await pool.query('SELECT * FROM customers');
    res.json(result.rows);
  } catch (err) {
    console.error(err);
    res.status(500).send('Server error');
  }
});

// Start the server
app.listen(port, () => {
  console.log(`Server running on http://localhost:${port}`);
});
