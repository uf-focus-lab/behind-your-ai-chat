<script setup lang="ts">
// The picture conversation as the model reads it: the 49 tiles spread out
// into the stream as tokens, between the user marker and the question, and
// the reply follows. Tiles get a box but no id: a patch token is not a row
// of the vocabulary, it is 768 numbers computed from the pixels.
import { computed } from 'vue'
import Stage from '../../components/Stage.vue'
import TokenStream, { type Chip } from '../../components/TokenStream.vue'
import { useMorphBoxes } from '../../composables/morphBoxes'
import data from '../../assets/vlfm/stream-vision.json'
import photo from '../../assets/vlfm/dog_a-square.webp'

const GRID = 7
const STEP = 25
const boxed = useMorphBoxes()

const chips = computed<Chip[]>(() => {
  let n = 0
  const tok = (t: { token: string; id: number }, i: number, p: string): Chip =>
    ({ key: `${p}-${i}`, kind: 'tok', text: t.token.trim() || '␣', id: t.id, vt: `tok-${p}-${i}`, delay: `${(n++) * STEP}ms` })
  return [
    { key: 'mark-s', kind: 'mark', text: '[system]' },
    { key: 'sys', kind: 'tok', text: '…', tone: 'dim' },
    { key: 'mark-u', kind: 'mark', text: '[user]' },
    ...Array.from({ length: GRID * GRID }, (_, i): Chip => ({
      key: `img-${i}`, kind: 'img', vt: `img-${i}`, tone: 'accent', delay: `${(n++) * STEP}ms`,
      tile: {
        backgroundImage: `url(${photo})`,
        backgroundSize: `${GRID * 34}px ${GRID * 34}px`,
        backgroundPosition: `${-(i % GRID) * 34}px ${-Math.floor(i / GRID) * 34}px`,
      },
    })),
    ...data.question.map((t, i) => tok(t, i, 'q')),
    { key: 'mark-a', kind: 'mark', text: '[agent]' },
    ...data.reply.map((t, i) => tok(t, i, 'r')),
  ]
})
</script>

<template>
  <Stage>
    <TokenStream :chips="chips" :boxed="boxed" class="vlfm-vision-stream" />
  </Stage>
</template>

<style scoped>
.vlfm-vision-stream { --ts-size: 19px; --ts-id-size: 12px; --ts-pad: 5px 8px 3px; --ts-gap: 7px 5px; --ts-mark-size: 18px; --ts-mark-pad: 7px 9px; --ts-tile: 34px; }
</style>
