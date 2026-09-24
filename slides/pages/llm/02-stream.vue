<script setup lang="ts">
// The same conversation as the model reads it, in three clicks: the words as
// discrete tokens, then a marker where each role begins, then the system
// prompt the user never typed. The user's and the reply's tokens keep the
// view-transition-names they had in the chat bubbles, so they fly here as
// bare words; the boxes and ids fade in afterwards, one token at a time,
// and fade out again before the deck steps back to the chat.
import { computed } from 'vue'
import { useSlideContext } from '@slidev/client'
import Stage from '../../components/Stage.vue'
import TokenStream, { type Chip } from '../../components/TokenStream.vue'
import { useMorphBoxes } from '../../composables/morphBoxes'
import data from '../../assets/llm/stream.json'

const STEP = 25     // between consecutive chips, the writing pace
const { $clicks } = useSlideContext()

const marker: Record<string, string> = { system: '[system]', user: '[user]', assistant: '[agent]' }
const prefix: Record<string, string> = { system: 's', user: 'u', assistant: 'a' }
const roles = data.recorded ? data.stream : [...data.stream, { role: 'assistant', tokens: [] }]

const chips = computed<Chip[]>(() => {
  const out: Chip[] = []
  let n = 0
  for (const m of roles) {
    if (m.role === 'system' && $clicks.value < 2) continue
    if ($clicks.value >= 1) out.push({ key: `mark-${m.role}`, kind: 'mark', text: marker[m.role] })
    for (const [i, t] of m.tokens.entries())
      out.push({ key: `${m.role}-${i}`, kind: 'tok', text: t.token.trim() || '␣', id: t.id, vt: `tok-${prefix[m.role]}-${i}`, delay: `${(n++) * STEP}ms` })
    if (m.role === 'assistant' && !m.tokens.length) out.push({ key: 'typing', kind: 'typing', vt: 'tok-a-typing' })
  }
  return out
})

const boxed = useMorphBoxes()
</script>

<template>
  <Stage>
    <TokenStream :chips="chips" :boxed="boxed" />
  </Stage>
</template>
