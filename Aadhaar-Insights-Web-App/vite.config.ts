
import { defineConfig } from 'vite';

export default defineConfig({
  build: {
    outDir: 'dist',
    rollupOptions: {
      input: {
        main: './index.html'
      }
    }
  },
  define: {
    'process.env.API_KEY': JSON.stringify(process.env.API_KEY)
  }
});
