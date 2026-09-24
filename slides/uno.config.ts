import { defineConfig } from 'unocss'

// Every page styles itself with scoped CSS, so the only utility the deck
// relies on is the cover's text-center. Safelisting it keeps the generated
// CSS complete from the first request, which `slidev export` needs.
export default defineConfig({
  safelist: ['text-center'],
})
