# IGNIS Frontend

A premium React-based competitive programming IDE with a dark gold theme.

## Quick Start

```bash
# Install dependencies
cd frontend
npm install

# Start development server
npm run dev

# Build for production
npm run build
```

Open http://localhost:5173

## Tech Stack

- React 18
- Vite
- Tailwind CSS
- Monaco Editor
- Framer Motion
- Zustand

## Features

- Dark gold circuit theme
- Resizable panels
- Monaco code editor with C++ syntax highlighting
- AI integration with self-verification
- Real-time code execution

## API Connection

The frontend expects a backend running on port 5000 (Flask/Python).
Configure the proxy in `vite.config.ts` if using a different port.

For AI features, ensure LM Studio is running at `http://localhost:1234`.
