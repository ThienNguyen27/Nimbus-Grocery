import express from 'express';
import path from 'path';
import { fileURLToPath } from 'url';
import signupRoute from './signupRoute.js';
import dotenv from 'dotenv';

dotenv.config();

const app = express();
const PORT = process.env.PORT || 3000;

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

app.use(express.json());
app.use('/api', signupRoute);
app.use(express.static(path.join(__dirname, '../public')));

app.get('/', (_, res) => {
  res.redirect('/signup.html');
});

app.listen(PORT, () => {
  console.log(`🚀 Server running at http://localhost:${PORT}`);
});
