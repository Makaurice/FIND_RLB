#!/usr/bin/env node
// Quick verification script for lucide-react installation

const fs = require('fs');
const path = require('path');

try {
  // Check if lucide-react is in node_modules
  const lucidePath = path.join(__dirname, 'node_modules', 'lucide-react');
  
  if (fs.existsSync(lucidePath)) {
    console.log('✅ lucide-react is installed in node_modules');
    
    // Try to require it
    try {
      const lucideReact = require('lucide-react');
      console.log('✅ lucide-react module can be imported');
      console.log('✅ All dependencies are ready!');
      process.exit(0);
    } catch (e) {
      console.log('⚠️  lucide-react directory exists but cannot be imported:', e.message);
      process.exit(1);
    }
  } else {
    console.log('❌ lucide-react not found in node_modules');
    console.log('Run: npm install');
    process.exit(1);
  }
} catch (e) {
  console.error('Error checking dependencies:', e);
  process.exit(1);
}
