import { Pool } from 'pg';
import dotenv from 'dotenv';
import path from 'path';
import { fileURLToPath } from 'url';

dotenv.config({
  path: path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../.env.local')
});

const connectionString = process.env.DATABASE_URL;

if (!connectionString) {
  throw new Error('DATABASE_URL not found in .env');
}

export const pool = new Pool({ connectionString });