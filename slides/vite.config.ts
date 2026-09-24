import path from 'node:path'
import { fileURLToPath } from 'node:url'
import { defineConfig } from 'vite'
import svgLoader from '@zhangyx1998/svg-loader'

const dir = path.dirname(fileURLToPath(import.meta.url))

// Slidev merges this with its own Vite config.
//
// svgLoader compiles every imported .svg into an inline, style-scoped Vue
// component, so diagrams are real markup that inherits currentColor and
// follows the dark scheme.
//
// server.fs.allow opens the repository root to the dev server, which is what
// lets a slide pull a code snippet out of demo1-matching/ and friends.
//
// The two aliases exist because a lecture file lives one directory down.
// Relative paths inside lectures/*.md resolve against lectures/, not against
// the workspace root, so `@fig` and `@pages` give every lecture one spelling
// that works from any depth.
export default defineConfig({
  plugins: [svgLoader()],
  resolve: {
    alias: {
      '@fig': path.resolve(dir, 'assets'),
      '@pages': path.resolve(dir, 'pages'),
    },
  },
  server: {
    fs: { allow: [path.resolve(dir, '..')] },
  },
})
