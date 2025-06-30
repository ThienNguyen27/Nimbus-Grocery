import express from 'express';
import bcrypt from 'bcrypt';
import { pool } from './db.js';

const router = express.Router();

router.post('/signup', async (req, res) => {
  console.log('📨 Signup request received:', req.body); // 👈 ADD THIS

  const { name, email, password } = req.body;

  if (!name || !email || !password) {
    console.log('Missing fields');
    return res.status(400).json({ error: 'All fields are required' });
  }

  try {
    const existing = await pool.query('SELECT id FROM users WHERE email = $1', [email]);
    console.log(' Existing user:', existing.rows);

    if (existing.rows.length > 0) {
      return res.status(400).json({ error: 'Email already registered' });
    }

    const hashed = await bcrypt.hash(password, 10);
    console.log(' Password hashed');

    const result = await pool.query(
      'INSERT INTO users (name, email, password_hash) VALUES ($1, $2, $3) RETURNING id, name, email, created_at',
      [name, email, hashed]
    );

    console.log('✅ User inserted:', result.rows[0]);
    res.status(201).json({ user: result.rows[0] });

  } catch (err: any) {
    console.error(' Signup error:', err); // 👈 CRITICAL LINE
    res.status(500).json({ error: 'Internal server error' });
  }
});


export default router;
